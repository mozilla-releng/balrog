import functools
from random import randint

try:
    from urlparse import urlparse
except ImportError:  # pragma: no cover
    from urllib.parse import urlparse

import logging

from auslib.global_state import dbo, cache


class ForceResult(object):
    """Enumerated "result" class that represents a non-random result chosen by a caller."""
    def __init__(self, name, query_value):
        self.name = name
        self.query_value = query_value


# Magic constants that callers can use to choose a specific "random" result.
SUCCEED = ForceResult('succeed', '1')
FAIL = ForceResult('fail', '-1')


def isSpecialURL(url, specialForceHosts):
    if not specialForceHosts:
        return False
    for s in specialForceHosts:
        if url.startswith(s):
            return True
    return False


def isForbiddenUrl(url, product, whitelistedDomains):
    if whitelistedDomains is None:
        whitelistedDomains = []
    domain = urlparse(url)[1]
    if domain not in whitelistedDomains:
        logging.warning("Forbidden domain: %s", domain)
        return True
    if product not in whitelistedDomains[domain]:
        logging.warning("Forbidden domain for product %s: %s", product, domain)
        return True
    return False


def getFallbackChannel(channel):
    return channel.split('-cck-')[0]


class AUS:

    def __init__(self):
        self.specialForceHosts = None
        self.rand = functools.partial(randint, 0, 99)
        self.log = logging.getLogger(self.__class__.__name__)

    def updates_are_disabled(self, product, channel, transaction=None):
        cache_key = (product, channel)
        v = cache.get('updates_disabled', cache_key)
        if v is not None:
            return v

        where = dict(product=product, channel=channel)
        emergency_shutoffs = dbo.emergencyShutoffs.select(where=where, transaction=transaction)
        v = bool(emergency_shutoffs)
        cache.put('updates_disabled', cache_key, v)
        return v

    def evaluateRules(self, updateQuery, transaction=None):
        self.log.debug("Looking for rules that apply to:")
        self.log.debug(updateQuery)

        if self.updates_are_disabled(updateQuery['product'], updateQuery['channel'], transaction) or \
           self.updates_are_disabled(updateQuery['product'], getFallbackChannel(updateQuery['channel']), transaction):
            log_message = 'Updates are disabled for {}/{}.'.format(
                updateQuery['product'], updateQuery['channel'])
            self.log.debug(log_message)
            return None, None

        rules = dbo.rules.getRulesMatchingQuery(
            updateQuery,
            fallbackChannel=getFallbackChannel(updateQuery['channel']),
            transaction=transaction,
        )

        # TODO: throw any N->N update rules and keep the highest priority remaining one?
        if len(rules) < 1:
            return None, None

        rules = sorted(rules, key=lambda rule: rule['priority'], reverse=True)
        rule = rules[0]
        self.log.debug("Matching rule: %s" % rule)

        # There's a few cases where we have a matching rule but don't want
        # to serve an update:
        # 1) No mapping.
        if not rule['mapping']:
            self.log.debug("Matching rule points at null mapping.")
            return None, None

        # 2) For background checks (force=1 missing from query), we might not
        # serve every request an update
        # backgroundRate=100 means all requests are served
        # backgroundRate=25 means only one quarter of requests are served
        if not updateQuery['force'] == SUCCEED and rule['backgroundRate'] < 100:
            self.log.debug("backgroundRate < 100, rolling the dice")
            if updateQuery['force'] == FAIL or self.rand() >= rule['backgroundRate']:
                fallbackReleaseName = rule['fallbackMapping']
                if fallbackReleaseName:
                    release = dbo.releases.getReleases(name=fallbackReleaseName, limit=1, transaction=transaction)[0]
                    blob = release['data']
                    if not blob.shouldServeUpdate(updateQuery):
                        return None, None
                    self.log.debug("Returning fallback release %s", release['name'])
                    return blob, rule['update_type']

                self.log.debug("No fallback releases. Request was dropped")
                return None, None

        # 3) Incoming release is older than the one in the mapping, defined as one of:
        #    * version decreases
        #    * version is the same and buildID doesn't increase
        release = dbo.releases.getReleases(name=rule['mapping'], limit=1, transaction=transaction)[0]
        blob = release['data']
        if not blob.shouldServeUpdate(updateQuery):
            return None, None

        self.log.debug("Returning release %s", release['name'])
        return blob, rule['update_type']
