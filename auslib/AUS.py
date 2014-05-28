import copy, re
from collections import defaultdict
from random import randint
from urlparse import urlparse

import logging

from auslib.db import AUSDatabase
from auslib.log import cef_event, CEF_ALERT
from auslib.util.versions import MozillaVersion

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

class AUS:
    def __init__(self, dbname=None):
        self.specialForceHosts = None
        self.setDb(dbname)
        self.rand = AUSRandom()
        self.log = logging.getLogger(self.__class__.__name__)

    def setDb(self, dbname):
        if dbname == None:
            dbname = "sqlite:///update.db"
        self.db = AUSDatabase(dbname)
        self.releases = self.db.releases
        self.rules = self.db.rules

    def setSpecialHosts(self, specialForceHosts):
        self.specialForceHosts = specialForceHosts

    def isSpecialURL(self, url):
        if not self.specialForceHosts:
            return False
        for s in self.specialForceHosts:
            if url.startswith(s):
                return True
        return False

    def containsForbiddenDomain(self, updateData):
        for patch in updateData['patches']:
            domain = urlparse(patch['URL'])[1]
            if domain not in self.db.domainWhitelist:
                cef_event('Forbidden domain', CEF_ALERT, domain=domain, updateData=updateData)
                return True
        return False

    def queryMatchesRelease(self, updateQuery, release):
        """Check if the updateQuery given is the same as the release."""
        self.log.debug("Trying to match update query to %s" % release['name'])
        buildTarget = updateQuery['buildTarget']
        buildID = updateQuery['buildID']
        locale = updateQuery['locale']

        if buildTarget in release['data']['platforms']:
            try:
                releaseBuildID = release['data'].getBuildID(buildTarget, locale)
            # Platform doesn't exist in release, clearly it's not a match!
            except KeyError:
                return False
            self.log.debug("releasePlat buildID is: %s", releaseBuildID)
            if buildID == releaseBuildID:
                self.log.debug("Query matched!")
                return True

    def evaluateRules(self, updateQuery):
        self.log.debug("Looking for rules that apply to:")
        self.log.debug(updateQuery)
        rules = self.rules.getRulesMatchingQuery(
            updateQuery,
            fallbackChannel=self.getFallbackChannel(updateQuery['channel'])
        )

        ### XXX throw any N->N update rules and keep the highest priority remaining one
        if len(rules) < 1:
            return None, None

        rules = sorted(rules,key=lambda rule: rule['priority'], reverse=True)
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
        if not updateQuery['force'] and rule['backgroundRate'] < 100:
            self.log.debug("backgroundRate < 100, rolling the dice")
            if self.rand.getInt() >= rule['backgroundRate']:
                self.log.debug("request was dropped")
                return None, None

        # 3) Incoming release is older than the one in the mapping, defined as one of:
        #    * version decreases
        #    * version is the same and buildID doesn't increase
        release = self.releases.getReleases(name=rule['mapping'], limit=1)[0]
        buildTarget = updateQuery['buildTarget']
        locale = updateQuery['locale']
        releaseVersion = release['data'].getApplicationVersion(buildTarget, locale)
        if not releaseVersion:
            self.log.debug("Matching rule has no extv, ignoring rule.")
            return None, None
        releaseVersion = MozillaVersion(releaseVersion)
        queryVersion = MozillaVersion(updateQuery['version'])
        if queryVersion > releaseVersion:
            self.log.debug("Matching rule has older version than request, ignoring rule.")
            return None, None
        elif releaseVersion == queryVersion:
            if updateQuery['buildID'] >= release['data'].getBuildID(updateQuery['buildTarget'], updateQuery['locale']):
                self.log.debug("Matching rule has older buildid than request, ignoring rule.")
                return None, None

        self.log.debug("Returning release %s", release['name'])
        return release['data'], rule['update_type']

    def getFallbackChannel(self, channel):
        return channel.split('-cck-')[0]

    def expandRelease(self, updateQuery, relData, update_type):
        updateData = defaultdict(list)

        buildTarget = updateQuery['buildTarget']
        locale = updateQuery['locale']
        # return early if we don't have an update for this platform
        if buildTarget not in relData.get('platforms', {}):
            self.log.debug("No platform %s in release %s", buildTarget, relData['name'])
            return updateData

        # platforms may be aliased to another platform in the case
        # of identical data, minimizing the json size
        relDataPlat = relData.getPlatformData(buildTarget)

        # return early if we don't have an update for this locale
        if locale not in relDataPlat['locales']:
            self.log.debug("No update to %s for %s/%s", relData['name'], buildTarget, locale)
            return updateData
        else:
            relDataPlatLoc = relDataPlat['locales'][locale]

        if relData['schema_version'] == 1:
            updateData['appv'] = relData.getAppv(buildTarget, locale)
            updateData['extv'] = relData.getExtv(buildTarget, locale)
        elif relData['schema_version'] == 2:
            updateData['displayVersion'] = relData.getDisplayVersion(buildTarget, locale)
            updateData['appVersion'] = relData.getAppVersion(buildTarget, locale)
            updateData['platformVersion'] = relData.getPlatformVersion(buildTarget, locale)
            for attr in relData.optional_:
                if attr in relData:
                    updateData[attr] = relData[attr]
            updateData['optional'] = relData.optional_

        # general properties
        updateData['type'] = update_type
        updateData['schema_version'] = relData['schema_version']
        updateData['build'] = relData.getBuildID(buildTarget, locale)
        if 'detailsUrl' in relData:
            updateData['detailsUrl'] = relData['detailsUrl'].replace('%LOCALE%',updateQuery['locale'])
        if 'licenseUrl' in relData:
            updateData['licenseUrl'] = relData['licenseUrl'].replace('%LOCALE%',updateQuery['locale'])

        # evaluate types of updates and see if we can use them
        for patchKey in relDataPlatLoc:
            if patchKey not in ('partial','complete'):
                self.log.debug("Skipping patchKey '%s'", patchKey)
                continue
            patch = relDataPlatLoc[patchKey]
            # This is factored out to avoid querying the db when from is '*'
            def hasAPartial():
                try:
                    release = self.releases.getReleases(name=patch['from'], limit=1)[0]
                    return self.queryMatchesRelease(updateQuery, release)
                except IndexError:
                    return False

            if patch['from'] == '*' or hasAPartial():
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
                if updateQuery['force'] and self.isSpecialURL(url):
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
                self.log.debug("Didn't add patch for patchKey '%s'; from is '%s'", patchKey, patch['from'])

        # older branches required a <partial> in the update.xml, which we
        # used to fake by repeating the complete data.
        if 'fakePartials' in relData and relData['fakePartials'] and len(updateData['patches']) == 1 and \
          updateData['patches'][0]['type'] == 'complete':
            patch = copy.copy(updateData['patches'][0])
            patch['type'] = 'partial'
            updateData['patches'].append(patch)

        self.log.debug("Returning %s", updateData)
        return updateData

    def createSnippet(self, updateQuery, release, update_type):
        if not release:
            # XXX: Not sure we should be specifying patch types here, but it's
            # required for tests that have null snippets in them at the time
            # of writing.
            return {"partial": "", "complete": ""}

        rel = self.expandRelease(updateQuery, release, update_type)

        if self.containsForbiddenDomain(rel):
            self.log.debug("Forbidden domain found, refusing to create snippets.")
            return {"partial": "", "complete": ""}

        if rel['schema_version'] == 1:
            return self.createSnippetV1(updateQuery, rel, update_type)
        elif rel['schema_version'] == 2:
            return self.createSnippetV2(updateQuery, rel, update_type)
        else:
            return {"partial": "", "complete": ""}

    def createSnippetV1(self, updateQuery, rel, update_type):
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
            if rel['licenseUrl']:
                snippet.append("licenseUrl=%s" % rel['licenseUrl'])
            if rel['type'] == 'major':
                snippet.append('updateType=major')
            # AUS2 snippets have a trailing newline, add one here for easy diffing
            snippets[patch['type']] = "\n".join(snippet) + '\n'

        for s in snippets.keys():
            self.log.debug('%s\n%s' % (s, snippets[s].rstrip()))
        return snippets

    def createSnippetV2(self, updateQuery, rel, update_type):
        snippets = {}
        for patch in rel['patches']:
            snippet  = ["version=2",
                        "type=%s" % patch['type'],
                        "url=%s" % patch['URL'],
                        "hashFunction=%s" % patch['hashFunction'],
                        "hashValue=%s" % patch['hashValue'],
                        "size=%s" % patch['size'],
                        "build=%s" % rel['build'],
                        "displayVersion=%s" % rel['displayVersion'],
                        "appVersion=%s" % rel['appVersion'],
                        "platformVersion=%s" % rel['platformVersion']
                        ]
            if rel['detailsUrl']:
                snippet.append("detailsUrl=%s" % rel['detailsUrl'])
            if rel['licenseUrl']:
                snippet.append("licenseUrl=%s" % rel['licenseUrl'])
            if rel['type'] == 'major':
                snippet.append('updateType=major')
            for attr in rel['optional']:
                if attr in rel:
                    snippet.append('%s=%s' % (attr, rel[attr]))
            # AUS2 snippets have a trailing newline, add one here for easy diffing
            snippets[patch['type']] = "\n".join(snippet) + '\n'

        for s in snippets.keys():
            self.log.debug('%s\n%s' % (s, snippets[s].rstrip()))
        return snippets

    def createXML(self, updateQuery, release, update_type):
        # this will fall down all sorts of interesting ways by hardcoding fields
        xml = ['<?xml version="1.0"?>']
        xml.append('<updates>')
        if release:
            rel = self.expandRelease(updateQuery, release, update_type)
            if rel and not self.containsForbiddenDomain(rel):
                if rel['schema_version'] == 1:
                    updateLine='    <update type="%s" version="%s" extensionVersion="%s" buildID="%s"' % \
                               (rel['type'], rel['appv'], rel['extv'], rel['build'])
                    if rel['detailsUrl']:
                        updateLine += ' detailsURL="%s"' % rel['detailsUrl']
                    if rel['licenseUrl']:
                        updateLine += ' licenseURL="%s"' % rel['licenseUrl']
                    updateLine += '>'
                    xml.append(updateLine)

                if rel['schema_version'] == 2:
                    updateLine='    <update type="%s" displayVersion="%s" appVersion="%s" platformVersion="%s" buildID="%s"' % \
                                (rel['type'], rel['displayVersion'], rel['appVersion'], rel['platformVersion'], rel['build'])
                    if rel['detailsUrl']:
                        updateLine += ' detailsURL="%s"' % rel['detailsUrl']
                    if rel['licenseUrl']:
                        updateLine += ' licenseURL="%s"' % rel['licenseUrl']
                    for attr in rel['optional']:
                        if attr in rel:
                            updateLine += ' %s="%s"' % (attr, rel[attr])
                    updateLine += '>'
                    xml.append(updateLine)

                for patch in sorted(rel['patches']):
                    xml.append('        <patch type="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s"/>' % \
                               (patch['type'], patch['URL'], patch['hashFunction'], patch['hashValue'], patch['size']))
                xml.append('    </update>')
        xml.append('</updates>')
        # ensure valid xml by using the right entity for ampersand
        payload = re.sub('&(?!amp;)','&amp;', '\n'.join(xml))
        return payload
