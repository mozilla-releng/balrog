import sqlite3, re, copy
from collections import defaultdict
# the json module in python 2.6 is really slow in comparison to simplejson
import simplejson as json

import logging
log = logging.getLogger(__name__)

class AUS3:
    def __init__(self, dbname=None):
        if dbname == None:
            dbname = "update.db"
        self.db = sqlite3.connect(dbname)
        # so we can get the key,value pairs out of query results,
        # instead of just values
        self.db.row_factory = sqlite3.Row
        
        self.initSchema()
        pass

    def close(self):
        self.db.close()

    def initSchema(self):
        self.db.execute("""
        CREATE TABLE IF NOT EXISTS update_paths (
          rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
          priority INTEGER,
          mapping TEXT,
          throttle INTEGER,
          update_type TEXT,
          product TEXT,
          version TEXT,
          channel TEXT,
          buildTarget TEXT,
          buildID TEXT,
          locale TEXT,
          osVersion TEXT,
          distribution TEXT,
          distVersion TEXT,
          headerArchitecture TEXT,
          comment TEXT
        )
        """)

        self.db.execute("""
        CREATE TABLE IF NOT EXISTS releases (
          name TEXT,
          product TEXT,
          version TEXT,
          data TEXT
        )
        """)

    def getRules(self):
        return self.db.execute("SELECT * FROM update_paths ORDER BY priority,version,mapping;")

    def getReleases(self):
        return self.db.execute("SELECT * FROM releases;")

    def identifyRequest(self, updateQuery):
        buildTarget = updateQuery['buildTarget']
        buildID = updateQuery['buildID']

        res = self.db.execute("SELECT * FROM releases WHERE product=? AND version=?",
                         (updateQuery['product'],updateQuery['version']))
        release = self.convertRelease(res.fetchone())
        while release:
            if buildTarget in release['data']['platforms']:
                releasePlat = release['data']['platforms'][buildTarget]
                if 'alias' in releasePlat:
                    alternateTarget = releasePlat['alias']
                    releasePlat = release['data']['platforms'][alternateTarget]

                if buildID == releasePlat['buildID']:
                    return release['name']
            # otherwise, try the next match
            release = self.convertRelease(res.fetchone())
        return None

    def convertRow(self, row):
        # takes a sqlite3.Row and turns it into a dict
        dict = {}
        for key in row.keys():
            dict[key] = row[key]
        return dict

    def convertRule(self, rule):
        return self.convertRow(rule)

    def convertRelease(self, release):
        # takes a sqlite3.Row of a release and returns a dict w/ json 'data'
        if release:
            r = self.convertRow(release)
            r['data'] = json.loads(r['data'])
            return r
        return None

    def matchesRegex(self, foo, bar):
        # Expand wildcards and use ^/$ to make sure we don't succeed on partial
        # matches.
        test = foo.replace('.','\.').replace('*','.*')
        test = '^%s$' % test
        if re.match(test, bar):
            return True
        return False

    def _versionMatchesRule(self, ruleVersion, queryVersion):
        """Decides whether a version from the rules matches an incoming version.
           If the ruleVersion is null, we match any queryVersion. If it's not
           null, we must either match exactly, or match a potential wildcard."""
        if ruleVersion == None:
            return True
        if self.matchesRegex(ruleVersion, queryVersion):
            return True

    def _channelMatchesRule(self, ruleChannel, queryChannel):
        """Decides whether a channel from the rules matchs an incoming one.
           If the ruleChannel is null, we match any queryChannel. We also match
           if the channels match exactly, or match after wildcards in ruleChannel
           are resolved. Channels may have a fallback specified, too, so we must
           check if the fallback version of the queryChannel matches the ruleChannel."""
        if ruleChannel == None:
            return True
        if self.matchesRegex(ruleChannel, queryChannel):
            return True
        if self.matchesRegex(ruleChannel, self.getFallbackChannel(queryChannel)):
            return True

    def getMatchingRules(self, updateQuery):
        log.debug("AUS.getMatchingRules: Looking for rules that apply to:")
        log.debug("AUS.getMatchingRules: %s", updateQuery)
        # get anything that must match or is undefined in rules
        res = self.db.execute("""
            SELECT * from update_paths
            WHERE throttle > 0
              AND (product=? OR product IS NULL)
              AND (buildTarget=? OR buildTarget IS NULL)
              AND (buildID=? OR buildID IS NULL)
              AND (locale=? OR locale IS NULL)
              AND (osVersion=? OR osVersion IS NULL)
              AND (distribution=? OR distribution IS NULL)
              AND (distVersion=? OR distVersion IS NULL)
              AND (headerArchitecture=? OR headerArchitecture IS NULL)
            """, (updateQuery['product'],
                  updateQuery['buildTarget'],
                  updateQuery['buildID'],
                  updateQuery['locale'],
                  updateQuery['osVersion'],
                  updateQuery['distribution'],
                  updateQuery['distVersion'],
                  updateQuery['headerArchitecture']
                  ))
        # evaluate wildcard parameters
        rules = []
        log.debug("AUS.getMatchingRules: Raw matches:")
        row = res.fetchone()
        while row:
            log.debug("AUS.getMatchingRules: %s", self.convertRule(row))
            # ignore any rules which would update ourselves to the same version
            if row['mapping'] != updateQuery['name']:
                if self._versionMatchesRule(row['version'], updateQuery['version']) and \
                  self._channelMatchesRule(row['channel'], updateQuery['channel']):
                    rules.append(self.convertRule(row))
            row = res.fetchone()
        log.debug("AUS.getMatchingRules: Reduced matches:")
        for r in rules:
            log.debug("AUS.getMatchingRules: %s", r)
        return rules

    def evaluateRules(self, updateQuery):
        rules = self.getMatchingRules(updateQuery)

        ### XXX throw any N->N update rules and keep the highest priority remaining one
        if len(rules) >= 1:
            rules = sorted(rules,key=lambda rule: rule['priority'], reverse=True)
            log.debug("AUS.evaluateRules: Returning rule:")
            log.debug("AUS.evaluateRules: %s", rules[0])
            return rules[0]
        return None

    def getFallbackChannel(self, channel):
        return channel.split('-cck-')[0]

    def expandRelease(self, updateQuery, rule):
        if not rule:
            return None
        # read data from releases table
        res = self.db.execute("SELECT * from releases WHERE name=?;",
                         (rule['mapping'],)).fetchone()
        if not res:
            # need to log some sort of data inconsistency error here
            log.debug("AUS.expandRelease: Failed to get release data from db for:")
            log.debug("AUS.expandRelease: %s", updateQuery)
            return None
        relData = json.loads(res['data'])
        updateData = defaultdict(list)

        buildTarget = updateQuery['buildTarget']
        locale = updateQuery['locale']

	# return early if we don't have an update for this platform
	if buildTarget not in relData['platforms']:
            return updateData

        # platforms may be aliased to another platform in the case
        # of identical data, minimizing the json size
        alias = relData['platforms'][buildTarget].get('alias')
        if alias and alias in relData['platforms']:
            relDataPlat = relData['platforms'][alias]
        else:
            relDataPlat = relData['platforms'][buildTarget]

        # return early if we don't have an update for this locale
        if locale not in relDataPlat['locales']:
            log.debug("AUS.expandRelease: No update to %s for %s/%s", rule['mapping'], buildTarget, locale)
            return updateData
        else:
            relDataPlatLoc = relDataPlat['locales'][locale]

        # this is for the properties AUS2 can cope with today
        if relData['data_version'] == 1:
            updateData['type'] = rule['update_type']
            for key in ('appv','extv', 'data_version'):
                updateData[key] = relData[key]
            if 'detailsUrl' in relData:
                updateData['detailsUrl'] = relData['detailsUrl'].replace('%LOCALE%',updateQuery['locale'])
            updateData['build'] = relDataPlat['buildID']

            # evaluate types of updates and see if we can use them
            for patchKey in relDataPlatLoc:
                if patchKey not in ('partial','complete'):
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
                    updateData['patches'].append({
                        'type': patchKey,
                        'URL':  url,
                        'hashFunction': relData['hashFunction'],
                        'hashValue': patch['hashValue'],
                        'size': patch['filesize']
                    })

            # older branches required a <partial> in the update.xml, which we
            # used to fake by repeating the complete data.
            if 'fakePartials' in relData and relData['fakePartials'] and len(updateData['patches']) == 1 and \
              updateData['patches'][0]['type'] == 'complete':
                patch = copy.copy(updateData['patches'][0])
                patch['type'] = 'partial'
                updateData['patches'].append(patch)

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
            if rel['data_version'] == 1:
                xml.append('    <update type="%s" version="%s" extensionVersion="%s" buildID="%s"' % \
                           (rel['type'], rel['appv'], rel['extv'], rel['build']))
                if rel['detailsUrl']:
                    xml.append(' detailsURL="%s"' % rel['detailsUrl'])
                xml.append('>')
                for patch in sorted(rel['patches']):
                    xml.append('        <patch type="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s"/>' % \
                               (patch['type'], patch['URL'], patch['hashFunction'], patch['hashValue'], patch['size']))
                # XXX: need to handle old releases needing completes duplicating partials
                # add another parameter in the rule table and use it here
                xml.append('    </update>')
        xml.append('</updates>')
        return '\n'.join(xml)
