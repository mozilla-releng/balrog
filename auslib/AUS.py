from random import randint
from urlparse import urlparse

import logging

from auslib.global_state import dbo


class ForceResult(object):
    """Enumerated "result" class that represents a non-random result chosen by a caller."""
    def __init__(self, name):
        self.name = name


# Magic constants that callers can use to choose a specific "random" result.
SUCCEED = ForceResult('succeed')
FAIL = ForceResult('fail')


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


class AUSRandom:
    """Abstract getting a randint to make it easier to test the range of
    possible values"""
    min = 0
    max = 99

    def getInt(self):
        return randint(self.min, self.max)


class AUS:

    def __init__(self, rand=None):
        self.specialForceHosts = None
        self.rand = rand or AUSRandom().getInt
        self.log = logging.getLogger(self.__class__.__name__)

    def evaluateRules(self, updateQuery):
        self.log.debug("Looking for rules that apply to:")
        self.log.debug(updateQuery)
        rules = dbo.rules.getRulesMatchingQuery(
            updateQuery,
            fallbackChannel=getFallbackChannel(updateQuery['channel'])
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
                    release = dbo.releases.getReleases(name=fallbackReleaseName, limit=1)[0]
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
        release = dbo.releases.getReleases(name=rule['mapping'], limit=1)[0]
        blob = release['data']
        if not blob.shouldServeUpdate(updateQuery):
            return None, None

        self.log.debug("Returning release %s", release['name'])
        return blob, rule['update_type']
