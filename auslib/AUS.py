import copy
from collections import defaultdict
from random import randint

import logging
log = logging.getLogger(__name__)

from auslib.db import AUSDatabase

class AUSRandom:
    """Abstract getting a randint to make it easier to test the range of
    possible values"""
    def __init__(self, min=0, max=99):
        self.min = min
        self.max = max

    def getInt(self):
        return randint(self.min, self.max)

    def getRange(self):
        return range(self.min, self.max+1)

class AUS3:
    def __init__(self, dbname=None):
        self.setDb(dbname)
        self.rand = AUSRandom()

    def setDb(self, dbname):
        if dbname == None:
            dbname = "sqlite:///update.db"
        self.db = AUSDatabase(dbname)
        self.releases = self.db.releases
        self.rules = self.db.rules

    def setSpecialHosts(self, specialForceHosts):
        self.specialForceHosts = specialForceHosts

    def createTables(self):
        self.db.createTables()

    def identifyRequest(self, updateQuery):
        log.debug("AUS.identifyRequest: got updateQuery: %s", updateQuery)
        buildTarget = updateQuery['buildTarget']
        buildID = updateQuery['buildID']
        locale = updateQuery['locale']

        for release in self.releases.getReleases(product=updateQuery['product'], version=updateQuery['version']):
            log.debug("AUS.identifyRequest: Trying to match request to %s", release['name'])
            if buildTarget in release['data']['platforms']:
                releaseBuildID = release['data'].getBuildID(buildTarget, locale)
                log.debug("AUS.identifyRequest: releasePlat buildID is: %s", releaseBuildID)
                if buildID == releaseBuildID:
                    log.debug("AUS.identifyRequest: Identified query as %s", release['name'])
                    return release['name']
        log.debug("AUS.identifyRequest: Couldn't identify query")
        return None

    def evaluateRules(self, updateQuery):
        log.debug("AUS.evaluateRules: Looking for rules that apply to:")
        log.debug("AUS.evaluateRules: %s", updateQuery)
        rules = self.rules.getRulesMatchingQuery(
            updateQuery,
            fallbackChannel=self.getFallbackChannel(updateQuery['channel'])
        )

        ### XXX throw any N->N update rules and keep the highest priority remaining one
        if len(rules) >= 1:
            rules = sorted(rules,key=lambda rule: rule['priority'], reverse=True)
            rule = rules[0]

            # for background checks (force=1 missing from query), we might not
            # serve every request an update
            # throttle=100 means all requests are served
            # throttle=25 means only one quarter of requests are served
            if not updateQuery['force'] and rule['throttle'] < 100:
                log.debug("AUS.evaluateRules: throttle < 100, rolling the dice")
                if self.rand.getInt() >= rule['throttle']:
                    log.debug("AUS.evaluateRules: request was dropped")
                    rule = None

            log.debug("AUS.evaluateRules: Returning rule:")
            log.debug("AUS.evaluateRules: %s", rule)
            return rule
        return None

    def getFallbackChannel(self, channel):
        return channel.split('-cck-')[0]

    def expandRelease(self, updateQuery, rule):
        if not rule or not rule['mapping']:
            log.debug("AUS.expandRelease: Couldn't find rule or mapping for %s" % rule)
            return None
        # read data from releases table
        try:
            res = self.releases.getReleases(name=rule['mapping'], limit=1)[0]
        except IndexError:
            # need to log some sort of data inconsistency error here
            log.debug("AUS.expandRelease: Failed to get release data from db for:")
            log.debug("AUS.expandRelease: %s", rule['mapping'])
            return None
        relData = res['data']
        updateData = defaultdict(list)

        # platforms may be aliased to another platform in the case
        # of identical data, minimizing the json size
        buildTarget = updateQuery['buildTarget']
        relDataPlat = relData.getPlatformData(buildTarget)
        locale = updateQuery['locale']

        # return early if we don't have an update for this platform
        if buildTarget not in relData['platforms']:
            log.debug("AUS.expandRelease: No platform %s in release %s", buildTarget, rule['mapping'])
            return updateData

        # return early if we don't have an update for this locale
        if locale not in relDataPlat['locales']:
            log.debug("AUS.expandRelease: No update to %s for %s/%s", rule['mapping'], buildTarget, locale)
            return updateData
        else:
            relDataPlatLoc = relDataPlat['locales'][locale]

        # this is for the properties AUS2 can cope with today
        if relData['schema_version'] == 1:
            updateData['type'] = rule['update_type']
            updateData['appv'] = relData.getAppv(buildTarget, locale)
            updateData['extv'] = relData.getExtv(buildTarget, locale)
            updateData['schema_version'] = relData['schema_version']
            if 'detailsUrl' in relData:
                updateData['detailsUrl'] = relData['detailsUrl'].replace('%LOCALE%',updateQuery['locale'])
            updateData['build'] = relData.getBuildID(buildTarget, locale)

            # evaluate types of updates and see if we can use them
            for patchKey in relDataPlatLoc:
                if patchKey not in ('partial','complete'):
                    log.debug("AUS.expandRelease: Skipping patchKey '%s'", patchKey)
                    continue
                patch = relDataPlatLoc[patchKey]
                if patch['from'] == updateQuery['name'] or patch['from'] == '*':
                    if 'fileUrl' in patch:
                        url = patch['fileUrl']
                    else:
                        # When we're using a fallback channel it's unlikely
                        # we'll have a fileUrl specifically for it, but we
                        # should try nonetheless. Non-fallback cases shouldn't
                        # be hitting any exceptions here.
                        try:
                            url = relData['fileUrls'][updateQuery['channel']]
                        except KeyError:
                            url = relData['fileUrls'][self.getFallbackChannel(updateQuery['channel'])]
                        url = url.replace('%LOCALE%', updateQuery['locale'])
                        url = url.replace('%OS_FTP%', relDataPlat['OS_FTP'])
                        url = url.replace('%FILENAME%', relData['ftpFilenames'][patchKey])
                        url = url.replace('%PRODUCT%', relData['bouncerProducts'][patchKey])
                        url = url.replace('%OS_BOUNCER%', relDataPlat['OS_BOUNCER'])
                    # pass on forcing for special hosts (eg download.m.o for mozilla metrics)
                    if updateQuery['force'] and url.startswith(self.specialForceHosts):
                        if '?' in url:
                            url += '&force=1'
                        else:
                            url += '?force=1'

                    updateData['patches'].append({
                        'type': patchKey,
                        'URL':  url,
                        'hashFunction': relData['hashFunction'],
                        'hashValue': patch['hashValue'],
                        'size': patch['filesize']
                    })
                else:
                    log.debug("AUS.expandRelease: Didn't add patch for patchKey '%s'; from is '%s', updateQuery name is '%s'", patchKey, patch['from'], updateQuery['name'])

            # older branches required a <partial> in the update.xml, which we
            # used to fake by repeating the complete data.
            if 'fakePartials' in relData and relData['fakePartials'] and len(updateData['patches']) == 1 and \
              updateData['patches'][0]['type'] == 'complete':
                patch = copy.copy(updateData['patches'][0])
                patch['type'] = 'partial'
                updateData['patches'].append(patch)

        log.debug("AUS.expandRelease: Returning %s", updateData)
        return updateData

    def createSnippet(self, updateQuery, release):
        rel = self.expandRelease(updateQuery, release)
        if not rel:
            # handle this better, both for prod and debugging
            log.debug("AUS.createSnippet: Couldn't expand rule for update target")
            # XXX: Not sure we should be specifying patch types here, but it's
            # required for tests that have null snippets in them at the time
            # of writing.
            return {"partial": "", "complete": ""}

        snippets = {}
        for patch in rel['patches']:
            snippet  = ["version=1",
                        "type=%s" % patch['type'],
                        "url=%s" % patch['URL'],
                        "hashFunction=%s" % patch['hashFunction'],
                        "hashValue=%s" % patch['hashValue'],
                        "size=%s" % patch['size'],
                        "build=%s" % rel['build'],
                        "appv=%s" % rel['appv'],
                        "extv=%s" % rel['extv']]
            if rel['detailsUrl']:
                snippet.append("detailsUrl=%s" % rel['detailsUrl'])
            if rel['type'] == 'major':
                snippets.append('updateType=major')
            # AUS2 snippets have a trailing newline, add one here for easy diffing
            snippets[patch['type']] = "\n".join(snippet) + '\n'
        # XXX: need to handle old releases needing completes duplicating partials
        # add another parameter in the rule table and use it here
        return snippets

    def createXML(self, updateQuery, release):
        rel = self.expandRelease(updateQuery, release)

        # this will fall down all sorts of interesting ways by hardcoding fields
        xml = ['<?xml version="1.0"?>']
        xml.append('<updates>')
        if rel:
            if rel['schema_version'] == 1:
                xml.append('    <update type="%s" version="%s" extensionVersion="%s" buildID="%s"' % \
                           (rel['type'], rel['appv'], rel['extv'], rel['build']))
                if rel['detailsUrl']:
                    xml.append(' detailsURL="%s"' % rel['detailsUrl'])
                xml.append('>')
                for patch in sorted(rel['patches']):
                    xml.append('        <patch type="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s"/>' % \
                               (patch['type'], patch['URL'], patch['hashFunction'], patch['hashValue'], patch['size']))
                xml.append('    </update>')
        xml.append('</updates>')
        return '\n'.join(xml)
