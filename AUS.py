import sqlite3, re
from collections import defaultdict
try:
    import json
except:
    import simplejson as json

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

    def dumpRules(self):
        rules = self.db.execute("SELECT * FROM update_paths ORDER BY priority,version,mapping;")
        if rules:
            print "Rules are \n(id, priority, mapping, throttle, product, version, channel, buildTarget, buildID, locale, osVersion, distribution, distVersion, UA arch)"
            for rule in rules:
                print rule
            print "-"*50

    def dumpReleases(self):
        releases = self.db.execute("SELECT * FROM releases;")
        if releases:
            print "Releases are \n(name, data:"
            for release in releases:
                print "(%s, %s " % (release[0],json.dumps(json.loads(release[1]),indent=2))
            print "-"*50

    def identifyRequest(self, updateQuery):
        buildTarget = updateQuery['buildTarget']
        buildID = updateQuery['buildID']

        res = self.db.execute("SELECT * FROM releases WHERE product=? AND version=?",
                         (updateQuery['product'],updateQuery['version']))
        release = self.convertRelease(res.fetchone())
        while release:
            if buildTarget in release['data']['platforms'].keys() and \
              buildID == release['data']['platforms'][buildTarget]['buildID']:
                return release['name']
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
        r = self.convertRow(release)
        r['data'] = json.loads(r['data'])
        return r

    def getMatchingRules(self, updateQuery):
        #print "\nlooking for rules that apply to"
        #print updateQuery
        # get anything that must match or is undefined in rules
        res = self.db.execute("""
            SELECT * from update_paths
            WHERE throttle > 0
              AND (product=? OR product IS NULL)
              AND (channel=? OR channel IS NULL)
              AND (buildTarget=? OR buildTarget IS NULL)
              AND (buildID=? OR buildID IS NULL)
              AND (locale=? OR locale IS NULL)
              AND (osVersion=? OR osVersion IS NULL)
              AND (distribution=? OR distribution IS NULL)
              AND (distVersion=? OR distVersion IS NULL)
              AND (headerArchitecture=? OR headerArchitecture IS NULL)
            """, (updateQuery['product'],
                  updateQuery['channel'],
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
        #print "\nraw matches:"
        row = res.fetchone()
        while row:
            #print row, updateQuery['name']
            # ignore any rules which would update ourselves to the same version
            if row['mapping'] != updateQuery['name']:
                # now resolve our special meanings
                if row['version'] is None:
                    rules.append(self.convertRule(row))
                else:
                    test = row['version'].replace('.','\.').replace('*','.*')
                    if re.match(test, updateQuery['version']):
                        rules.append(self.convertRule(row))
            row = res.fetchone()
    #    print "\nreduced matches:"
    #    for r in rules:
    #        print r
        return rules

    def evaluateRules(self, updateQuery):
        rules = self.getMatchingRules(updateQuery)
        #print "\nrules before"
        #for r in rules:
        #    print r
        ### XXX throw any N->N update rules and keep the highest priority remaining one
        if len(rules) >= 1:
            rules = sorted(rules,key=lambda rule: rule['priority'], reverse=True)
            return rules[0]
        #print "\nrules after"
        #for r in rules:
        #    print r
        return None

    def expandRelease(self, updateQuery, rule):
        if not rule:
            return None
        # read data from releases table
        res = self.db.execute("SELECT * from releases WHERE name=?;",
                         (rule['mapping'],)).fetchone()
        relData = json.loads(res['data'])
        updateData = defaultdict(list)

        # return early if we don't have an update for this platform and locale
        buildTarget = updateQuery['buildTarget']
        locale = updateQuery['locale']
        if buildTarget not in relData['platforms'].keys() or \
          locale not in relData['platforms'][buildTarget]['locales'].keys():
            # print "AUS.expandRelease: no update to %s for %s/%s" % (rule['mapping'],buildTarget,locale)
            return updateData

        # this is for the properties AUS2 can cope with today
        if relData['data_version'] == 1:
            updateData['type'] = rule['update_type']
            for key in ('appv','extv','detailsUrl', 'data_version'):
                updateData[key] = relData[key]
            updateData['build'] = relData['platforms'][buildTarget]['buildID']

            # evaluate types of updates and see if we can use them
            for patchKey in relData['platforms'][buildTarget]['locales'][locale]:
                if patchKey not in ('partial','complete'):
                    continue
                patch = relData['platforms'][buildTarget]['locales'][locale][patchKey]
                if patch['from'] == updateQuery['name'] or patch['from'] == '*':
                    if 'fileurls' in patch and \
                       'channel' in patch['fileurls']:
                        url = patch['fileurls'][updateQuery['channel']]
                    else:
                        url = relData['fileUrls'][updateQuery['channel']]
                    url = url.replace('%LOCALE%',updateQuery['locale'])
                    url = url.replace('%OS_FTP%',relData['platforms'][buildTarget]['OS_FTP'])
                    url = url.replace('%FILENAME%', relData['ftpFilenames'][patchKey])
                    url = url.replace('%PRODUCT%',relData['bouncerProducts'][patchKey])
                    url = url.replace('%OS_BOUNCER%',relData['platforms'][buildTarget]['OS_BOUNCER'])
                    updateData['patches'].append({
                        'type': patchKey,
                        'URL':  url,
                        'hashFunction': relData['hashFunction'],
                        'hashValue': patch['hashValue'],
                        'size': patch['filesize']
                    })
        return updateData

    def createSnippet(self, updateQuery, release):
        rel = self.expandRelease(updateQuery, release)
        if not rel:
            # handle this better, both for prod and debugging
            # print "AUS.createSnippet: couldn't expand rule for update target"
            return {}

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
                        "extv=%s" % rel['extv'],
                        "detailsUrl=%s" % rel['detailsUrl']]
            if rel['type'] == 'major':
                snippets.append('updateType=major')
            # AUS2 snippets have a trailing newline, add one here for easy diffing
            snippets[patch['type']] = "\n".join(snippet) + '\n'
        # XXX: need to handle old releases needing completes duplicating partials
        # add another parameter in the rule table and use it here
        return snippets

    def createXML(self, updateQuery, release):
        # this will fall down all sorts of interesting ways by hardcoding fields
        xml = ['<?xml version="1.0"?>']
        rel = self.expandRelease(updateQuery, release)
        if rel:
            xml.append('<updates>')
            if rel['data_version'] == 1:
                xml.append('    <update type="%s" version="%s" extensionVersion="%s" buildID="%s" detailsURL="%s">' % \
                           (rel['type'], rel['appv'], rel['extv'], rel['build'], rel['detailsUrl']))
                for patch in rel['patches']:
                    xml.append('        <patch type="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s"/>' % \
                               (patch['type'], patch['URL'], patch['hashFunction'], patch['hashValue'], patch['size']))
                # XXX: need to handle old releases needing completes duplicating partials
                # add another parameter in the rule table and use it here
                xml.append('    </update>')
            # else you're out of luck
            xml.append('</updates>')
        return '\n'.join(xml)
