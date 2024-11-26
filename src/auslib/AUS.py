import functools
import logging
import re
from random import randint
from urllib.parse import urlparse

from auslib.blobs.base import ServeUpdate, createBlob
from auslib.global_state import cache, dbo
from auslib.services import releases
from auslib.util.versions import PinVersion


class ForceResult(object):
    """Enumerated "result" class that represents a non-random result chosen by a caller."""

    def __init__(self, name, query_value):
        self.name = name
        self.query_value = query_value


# Magic constants that callers can use to choose a specific "random" result.
FORCE_MAIN_MAPPING = ForceResult("succeed", "1")
FORCE_FALLBACK_MAPPING = ForceResult("fail", "-1")


def isSpecialURL(url, specialForceHosts):
    if not specialForceHosts:
        return False
    for s in specialForceHosts:
        if url.startswith(s):
            return True
    return False


def isForbiddenUrl(url, product, allowlistedDomains):
    if allowlistedDomains is None:
        allowlistedDomains = []
    parsedUrl = urlparse(url)
    domain = parsedUrl.netloc
    if domain not in allowlistedDomains:
        logging.warning("Forbidden domain: %s", domain)
        return True
    allowlistedDomain = allowlistedDomains[domain]
    if isinstance(allowlistedDomain, tuple):
        if product in allowlistedDomain:
            return False
        logging.warning("Forbidden domain for product %s: %s", product, domain)
    elif isinstance(allowlistedDomain, dict):
        path = parsedUrl.path
        for pathRegex in allowlistedDomain:
            if not re.fullmatch(pathRegex, path):
                continue
            if product in allowlistedDomain[pathRegex]:
                return False
            logging.warning("Forbidden domain/path for product %s: %s (%s)", product, domain, path)
            return True
        logging.warning("Forbidden domain/path: %s (%s)", domain, path)
    else:
        logging.warning("Forbidden domain, malformed entry: %s", domain)
    return True


def getFallbackChannel(channel):
    return channel.split("-cck-")[0]


class AUS:
    def __init__(self):
        self.specialForceHosts = None
        self.rand = functools.partial(randint, 0, 99)
        self.log = logging.getLogger(self.__class__.__name__)

    def updates_are_disabled(self, product, channel, transaction=None):
        cache_key = (product, channel)
        v = cache.get("updates_disabled", cache_key)
        if v is not None:
            return v

        where = dict(product=product, channel=channel)
        emergency_shutoffs = dbo.emergencyShutoffs.select(where=where, transaction=transaction)
        v = bool(emergency_shutoffs)
        cache.put("updates_disabled", cache_key, v)
        return v

    def evaluateRules(self, updateQuery, transaction=None):
        self.log.debug("Looking for rules that apply to:")
        self.log.debug(updateQuery)

        eval_metadata = dict(rule_id="unknown", rule_data_version="unknown")

        if self.updates_are_disabled(updateQuery["product"], updateQuery["channel"], transaction) or self.updates_are_disabled(
            updateQuery["product"], getFallbackChannel(updateQuery["channel"]), transaction
        ):
            log_message = "Updates are disabled for {}/{}.".format(updateQuery["product"], updateQuery["channel"])
            self.log.debug(log_message)
            return None, None, eval_metadata

        rules = dbo.rules.getRulesMatchingQuery(updateQuery, fallbackChannel=getFallbackChannel(updateQuery["channel"]), transaction=transaction)

        # TODO: throw any N->N update rules and keep the highest priority remaining one?
        if len(rules) < 1:
            return None, None, eval_metadata

        rules = sorted(rules, key=lambda rule: rule["priority"], reverse=True)
        rule = rules[0]

        eval_metadata["rule_id"] = rule["rule_id"]
        eval_metadata["rule_data_version"] = rule["data_version"]

        self.log.debug("Matching rule: %s" % rule)

        # There's a few cases where we have a matching rule but don't want
        # to serve an update:
        # 1) No mapping.
        if not rule["mapping"]:
            self.log.debug("Matching rule points at null mapping.")
            return None, None, eval_metadata
        mapping = rule["mapping"]

        # 2) For background checks (force=1 missing from query), we might not
        # serve every request an update
        # backgroundRate=100 means all requests are served
        # backgroundRate=25 means only one quarter of requests are served
        if not updateQuery["force"] == FORCE_MAIN_MAPPING and rule["backgroundRate"] < 100:
            self.log.debug("backgroundRate < 100, rolling the dice")
            if updateQuery["force"] == FORCE_FALLBACK_MAPPING or self.rand() >= rule["backgroundRate"]:
                fallbackReleaseName = rule["fallbackMapping"]
                if not fallbackReleaseName:
                    self.log.debug("No fallback releases. Request was dropped")
                    return None, None, eval_metadata

                self.log.debug("Using fallback release %s", fallbackReleaseName)
                mapping = fallbackReleaseName

        # 3) Incoming release is older than the one in the mapping, defined as one of:
        #    * version decreases
        #    * version is the same and buildID doesn't increase
        def get_blob(mapping):
            release = releases.get_release(mapping, transaction, include_sc=False)
            blob = None
            if release:
                blob = createBlob(release["blob"])
            # TODO: remove me when old releases table dies
            else:
                release = dbo.releases.getReleases(name=mapping, limit=1, transaction=transaction)[0]
                blob = release["data"]
            return blob

        blob = get_blob(mapping)
        if not blob:
            return None, None, eval_metadata
        candidate = blob.shouldServeUpdate(updateQuery)
        if not candidate:
            return None, None, eval_metadata

        if candidate == ServeUpdate.Maybe:
            version_pin = PinVersion(updateQuery.get("pin"))
            pin_mapping = dbo.pinnable_releases.getPinMapping(updateQuery["product"], getFallbackChannel(updateQuery["channel"]), str(version_pin))
            # Note that we fall back to serving the original update if the pin is not found
            # in the pin table, even if the version that we will serve is past the pinned
            # version. This is because, if there is something wrong with the update pin,
            # we would rather default to keeping the user up-to-date.
            # The alternative would mean that setting invalid pin would be a subtle problem
            # that would potentially be difficult to recognize. For example:
            #  - A sysadmin installs Firefox ESR 120.0 and sets the pin to '120.15.'.
            #  - Every time that a new minor version of 120 is available, the sysadmin
            #    updates to it promptly.
            #  - Eventually, the sysadmin updates to 120.14, but 120.15 is never released.
            #    The next version is ESR 134.0.
            #  - The relevant update rule now points to ESR 134, but it isn't returned as
            #    an available update so, as far as the sysadmin knows, the pin is working
            #    as expected.
            #  - A loaner laptop is given out that still has ESR 120.0 installed.
            #  - When the loaner laptop asks for updates, Balrog sees that the newest
            #    version is ESR 134.0, but that would be newer than the '120.15' pin,
            #    so no update is returned.
            #  - The loaner laptop never updates and stays at ESR 120.0.
            # This situation hides the problem from the sysadmin and leaves some
            # installations vulnerable.
            if pin_mapping is not None:
                mapping = pin_mapping
                blob = get_blob(mapping)
                if not blob or not blob.shouldServeUpdate(updateQuery):
                    return None, None, eval_metadata

        self.log.debug("Returning release %s", mapping)
        return blob, rule["update_type"], eval_metadata
