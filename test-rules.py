import os, glob, re
from collections import defaultdict
from model import UpdateDB
try:
    import json
except:
    import simplejson as json

def populateDB():
    # assuming we're already in the right directory with a db connection
    # read any rules we already have
    if os.path.exists('rules.sql'):
        f = open('rules.sql','r')
        for line in f:
            if line.startswith('#'):
                continue
            db.execute(line.strip())
    # and add any json blobs we created painstakingly, converting to compact json
    for f in glob.glob('*.json'):
        data = json.load(open(f,'r'))
        product,version = data['name'].split('-')[0:2]
        db.execute("INSERT INTO releases VALUES ('%s', '%s', '%s','%s')" %
                   (data['name'], product, version, json.dumps(data)))
    db.commit()
    # TODO - create a proper importer that walks the snippet store to find hashes ?

def dumpRules():
    rules = db.execute("SELECT * FROM update_paths ORDER BY priority,version,mapping;")
    if rules:
        print "Rules are \n(id, priority, mapping, throttle, product, version, channel, buildTarget, buildID, locale, osVersion, distribution, distVersion, UA arch)"
        for rule in rules:
            print rule
        print "-"*50

def dumpReleases():
    releases = db.execute("SELECT * FROM releases;")
    if releases:
        print "Releases are \n(name, data:"
        for release in releases:
            print "(%s, %s " % (release[0],json.dumps(json.loads(release[1]),indent=2))
        print "-"*50

def identifyRequest(updateQuery):
    buildTarget = updateQuery['buildTarget']
    buildID = updateQuery['buildID']
    
    res = db.execute("SELECT * FROM releases WHERE product=? AND version=?",
                     (updateQuery['product'],updateQuery['version']))
    release = convertRelease(res.fetchone())
    while release:
        if buildTarget in release['data']['platforms'].keys() and \
          buildID == release['data']['platforms'][buildTarget]['buildID']:
            return release['name']
        release = convertRelease(res.fetchone())
    return None

def convertRow(row):
    # takes a sqlite3.Row and turns it into a dict
    dict = {}
    for key in row.keys():
        dict[key] = row[key]
    return dict

def convertRule(rule):
    return convertRow(rule)

def convertRelease(release):
    # takes a sqlite3.Row of a release and returns a dict w/ json 'data'
    r = convertRow(release)
    r['data'] = json.loads(r['data'])
    return r

def getMatchingRules(updateQuery):
    print "\nlooking for rules that apply to"
    print updateQuery
    # get anything that must match or is undefined in rules
    res = db.execute("""
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
    print "\nraw matches:"
    row = res.fetchone()
    while row:
        print row, updateQuery['name']
        # ignore any rules which would update ourselves to the same version
        if row['mapping'] != updateQuery['name']:
            # now resolve our special meanings
            if row['version'] is None:
                rules.append(convertRule(row))
            else: 
                test = row['version'].replace('.','\.').replace('*','.*')
                if re.match(test, updateQuery['version']):
                    rules.append(convertRule(row))
        row = res.fetchone()
#    print "\nreduced matches:"
#    for r in rules:
#        print r
    return rules

def evaluateRules(updateQuery):
    rules = getMatchingRules(updateQuery)
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

def expandRelease(updateQuery, rule):
    if not rule:
        return None
    # read data from releases table
    res = db.execute("SELECT * from releases WHERE name=?;",
                     (rule['mapping'],)).fetchone()
    relData = json.loads(res['data'])
    updateData = defaultdict(list)

    # return early if we don't have an update for this platform and locale
    buildTarget = updateQuery['buildTarget']
    locale = updateQuery['locale']
    if buildTarget not in relData['platforms'].keys() or \
      locale not in relData['platforms'][buildTarget]['locales'].keys():
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
                url = url.replace('%PRODUCT%',relData['bouncerProducts'][patchKey])
                url = url.replace('%OS_FTP%',relData['platforms'][buildTarget]['OS_FTP'])
                url = url.replace('%OS_BOUNCER%',relData['platforms'][buildTarget]['OS_BOUNCER'])
                updateData['patches'].append({
                    'type': patchKey,
                    'URL':  url,
                    'hashFunction': relData['hashFunction'],
                    'hashValue': patch['hashValue'],
                    'size': patch['filesize']
                })

    return updateData

def createSnippet(updateQuery, release):
    rel = expandRelease(updateQuery, release)
    if not rel:
        return None

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
        snippets[patch['type']] = "\n".join(snippet)
    return snippets

def createXML(updateQuery, release):
    # this will fall down all sorts of interesting ways by hardcoding fields
    xml = ['<?xml version="1.0"?>']
    rel = expandRelease(updateQuery, release)
    if rel:
        xml.append('<updates>')
        if rel['data_version'] == 1:
            xml.append('    <update type="%s" version="%s" extensionVersion="%s" buildID="%s" detailsURL="%s">' % \
                       (rel['type'], rel['appv'], rel['extv'], rel['build'], rel['detailsUrl']))
            for patch in rel['patches']:
                xml.append('        <patch type="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s"/>' % \
                           (patch['type'], patch['URL'], patch['hashFunction'], patch['hashValue'], patch['size']))
            xml.append('    </update>')
        # else you're out of luck
        xml.append('</updates>')
    return '\n'.join(xml)


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_defaults(
        db='update.db'
    )
    parser.add_option("-c", "--clobber", dest="clobber", action="store_true", help="clobber existing db")
    parser.add_option("-i", "--inputdir", dest="inputdir", help="aus datastore to read")
    parser.add_option("-d", "--db", dest="db", help="database to use, relative to inputdir")
    parser.add_option("", "--dump-rules", dest="dumprules", action="store_true", help="dump rules to stdout")
    parser.add_option("", "--dump-releases", dest="dumpreleases", action="store_true", help="dump release data to stdout")

    options, args = parser.parse_args()
    if not options.inputdir or not os.path.isdir(options.inputdir):
        parser.error('Must specify a directory to read with -i/--inputdir')
    os.chdir(options.inputdir)

    if options.clobber and os.path.exists(options.db):
        os.remove(options.db)
    dbObj = UpdateDB(dbname = options.db)
    db = dbObj.db
    if options.clobber:
        populateDB()

    # "pretty" printing
    if options.dumprules:
        dumpRules()
    if options.dumpreleases:
        dumpReleases()


    # version 3 update + UA arch
    testUpdate = {'product': 'Firefox',
                  'version': '3.6.12',
                  'buildID': '20101026210630',
                  'buildTarget': 'WINNT_x86-msvc',
                  'locale': 'en-US',
                  'channel': 'releasetest',
                  'osVersion': 'foo',
                  'distribution': 'foo',
                  'distVersion': 'foo',
                  'headerArchitecture': 'Intel',
                  'name': ''
                 }
    
    testUpdate['name'] = identifyRequest(testUpdate)
    print "\nThe request is from %s" % testUpdate['name']
    
    rule = evaluateRules(testUpdate)
    print "\nthe one rule to rule them all is:"
    print rule
    
    snippets = createSnippet(testUpdate,rule)
    if snippets:
        for type in snippets.keys():
            print "\n%s snippet:" % type
            print snippets[type]
    else:
        print "\nno snippets"
        
    xml = createXML(testUpdate,rule)
    print "\nxml is:\n%s" % xml

    # once this is working, walk tree of snippets and calculate snippet
    # compare to data on disk
    # use this to fill out rules (ignore locales for now ? lots of hashes/sizes)
    # create a way to programaticaly generate the json