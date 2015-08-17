#!/usr/bin/env python

import os
import os.path
import glob
import re
import difflib
import time
import site

try:
    import json
    assert json  # to shut pyflakes up
except:
    import simplejson as json

mydir = os.path.dirname(os.path.abspath(__file__))
site.addsitedir(os.path.join(mydir, ".."))
site.addsitedir(os.path.join(mydir, "..", 'vendor/lib/python'))

from auslib.AUS import AUS as AUS_Class
from auslib.global_state import dbo

import logging
log = logging.getLogger(__name__)

WHITELISTED_DOMAINS = ('download.mozilla.org', 'stage-old.mozilla.org', 'ftp.mozilla.org', 'stage.mozilla.org')
SPECIAL_FORCE_HOSTS = ('download.mozilla.org',)


def populateDB(testdir):
    # assuming we're already in the right directory with a db connection
    # read any rules we already have
    rules = os.path.join(testdir, 'rules.sql')
    if os.path.exists(rules):
        f = open(rules, 'r')
        for line in f:
            if line.startswith('#'):
                continue
            dbo.engine.execute(line.strip())
    # and add any json blobs we created painstakingly, converting to compact json
    for f in glob.glob('%s/*.json' % testdir):
        data = json.load(open(f, 'r'))
        product = data['name'].split('-')[0]
        # JSON files can have the extv version at the top level, or in the locales
        # If we can't find it at the top level, look for it in a locale. This is
        # less accurate, but the best we can do.
        version = data.get('appVersion', data.get('extv'))
        if not version:
            version = data.get('platforms').values()[0].get('locales').values()[0].get('extv')
            if not version:
                raise Exception("Couldn't find version for %s" % data['name'])
        dbo.engine.execute("INSERT INTO releases (name, product, version, data, data_version) VALUES ('%s', '%s', '%s','%s', 1)" %
                           (data['name'], product, version, json.dumps(data)))
    # TODO - create a proper importer that walks the snippet store to find hashes ?


def getQueryFromPath(snippetPath):
    """ Use regexp to turn a path to a release snippet like
            "Firefox/3.6.13/WINNT_x86-msvc/20101122053531/af/beta/complete.txt"
        into
            testUpdate = {
                  'product': 'Firefox',
                  'version': '3.6.13',
                  'buildID': '20101122053531',
                  'buildTarget': 'WINNT_x86-msvc',
                  'locale': 'af',
                  'channel': 'beta',
                  'osVersion': 'foo',
                  'distribution': 'foo',
                  'distVersion': 'foo',
                  'headerArchitecture': 'Intel',
                  'name': ''
                 }
    """
    m = re.match("^(?P<product>.*?)/(?P<version>.*?)/(?P<buildTarget>.*?)/(?P<buildID>.*?)/(?P<locale>.*?)/(?P<channel>.*?)/", snippetPath)
    if m:
        update = m.groupdict()
        update['osVersion'] = 'foo'
        update['distribution'] = 'foo'
        update['distVersion'] = 'foo'
        update['headerArchitecture'] = 'Intel'
        update['force'] = False
        update['name'] = ''
        return update
    else:
        # raise an error ?
        pass


def walkSnippets(AUS, testPath):
    start = time.time()

    # walk tree of snippets and create sorted list, I/O intensive
    AUS2snippets = []
    for root, dirs, files in os.walk(testPath):
        for f in files:
            AUS2snippets.append(os.path.join(root, f))
    AUS2snippets = sorted(AUS2snippets)

    passCount = 0
    failCount = 0

    for f in AUS2snippets:
        f = os.path.relpath(f)
        snipType = os.path.splitext(os.path.basename(f))[0]

        # generate the AUS snippets
        log.debug('test-rules.walkSnippets: %s' % f)
        testQuery = getQueryFromPath(f.lstrip(testPath))
        testQuery['queryVersion'] = 3
        release, update_type = AUS.evaluateRules(testQuery)
        if release:
            balrog_snippets = release.createSnippets(testQuery, update_type, WHITELISTED_DOMAINS, SPECIAL_FORCE_HOSTS)
        else:
            balrog_snippets = {"partial": "", "complete": ""}

        if snipType in balrog_snippets:
            balrog_snippet = balrog_snippets[snipType]
            AUS2snippet = open(f, 'r').read()
            if AUS2snippet != balrog_snippet:
                diff = difflib.unified_diff(
                    AUS2snippet.splitlines(),
                    balrog_snippet.splitlines(),
                    lineterm='',
                    n=20)
                log.info("FAIL: %s", f)
                failCount += 1
                for line in diff:
                    log.info('DIFF: %s', line)
            else:
                log.debug("PASS: %s", f)
                passCount += 1
        else:
            log.info("FAIL: no snippet for %s", f)
            failCount += 1

    elapsed = time.time() - start
    common_return = "(%s PASS, %s FAIL" % (passCount, failCount)

    if elapsed > 0.5:
        rate = (passCount + failCount) / elapsed
        common_return += ", %1.2f sec, %1.1f tests/second)" % (elapsed, rate)
    else:
        common_return += ")"
    if failCount:
        return "FAIL   %s" % common_return
    else:
        return "PASS   %s" % common_return


def isValidTestDir(d):
    if not os.path.exists(os.path.join(d, 'rules.sql')):
        return False
    if not os.path.exists(os.path.join(d, 'snippets')):
        return False
    if not glob.glob('%s/*.json' % d):
        return False
    return True

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_defaults(
        testDirs=[]
    )
    parser.add_option("-t", "--test-dir", dest="testDirs", action="append")
    parser.add_option("", "--dump-rules", dest="dumprules", action="store_true", help="dump rules to stdout")
    parser.add_option("", "--dump-releases", dest="dumpreleases", action="store_true", help="dump release data to stdout")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="verbose output for snippet checking")
    parser.add_option("-k", "--keep-db", dest="keepDB", action="store_true", help="save a copy of the test db in thetest dir")

    options, args = parser.parse_args()

    log_level = logging.INFO
    if options.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level, format='%(message)s')

    if not options.testDirs:
        for dirname in os.listdir('aus-data-snapshots'):
            d = os.path.join('aus-data-snapshots', dirname)
            if isValidTestDir(d):
                options.testDirs.append(d)

    for td in options.testDirs:
        log.info("Starting %s", td)
        if options.keepDB:
            dbPath = os.path.join(td, 'update.db')
            if os.path.exists(dbPath):
                os.remove(dbPath)
            log.info('saving db at %s' % dbPath)
            dbPath = 'sqlite:///%s' % dbPath
        else:
            dbPath = 'sqlite:///:memory:'
        AUS = AUS_Class()
        dbo.setDb(dbPath)
        dbo.create()
        dbo.setDomainWhitelist(WHITELISTED_DOMAINS)
        populateDB(td)
        if options.dumprules:
            log.info("Rules are \n(id, priority, mapping, backgroundRate, product, version, channel, buildTarget, buildID, locale, osVersion, distribution, distVersion, UA arch):")
            for rule in AUS.rules.getOrderedRules():
                log.info(", ".join([str(rule[k]) for k in rule.keys()]))
            log.info("-" * 50)

        if options.dumpreleases:
            log.info("Releases are \n(name, product, version, data):")
            for release in AUS.releases.getReleases():
                log.info("(%s, %s, %s, %s " % (release['name'], release['product'],
                                               release['version'],
                                               json.dumps(release['data'], indent=2)))
            log.info("-" * 50)

        result = walkSnippets(AUS, os.path.join(td, 'snippets'))
        log.info(result)
