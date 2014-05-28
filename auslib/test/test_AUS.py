import simplejson as json
import mock
import unittest
from xml.dom import minidom

from auslib.AUS import AUS
from auslib.blob import ReleaseBlobV1, ReleaseBlobV2

def RandomAUSTest(AUS, backgroundRate, force, mapping):
    with mock.patch('auslib.db.Rules.getRulesMatchingQuery') as m:
        m.return_value=[dict(backgroundRate=backgroundRate, priority=1, mapping=mapping, update_type='minor')]

        results = AUS.rand.getRange()
        resultsLength = len(results)
        def se(*args, **kwargs):
            return results.pop()
        with mock.patch('auslib.AUS.AUSRandom.getInt') as m2:
            m2.side_effect = se
            served = 0
            tested = 0
            while len(results) > 0:
                updateQuery = dict(
                    channel='foo', force=force, buildTarget='a', buildID='0',
                    locale='a', version='1.0'
                )
                r, _ = AUS.evaluateRules(updateQuery)
                tested +=1
                if r:
                    served += 1
                # bail out if we're not asking for any randint's
                if resultsLength == len(results):
                    break
            return (served, tested)

class TestAUSThrottling(unittest.TestCase):
    def setUp(self):
        self.AUS = AUS()
        self.AUS.setDb('sqlite:///:memory:')
        self.AUS.db.create()
        self.AUS.db.releases.t.insert().execute(name='b', product='b', version='b', data_version=1, data='{"name": "b", "extv": "1.0", "schema_version": 1, "platforms": {"a": {"buildID": "1", "locales": {"a": {}}}}}')

    def testThrottling100(self):
        (served, tested) = RandomAUSTest(self.AUS, backgroundRate=100, force=False, mapping='b')
        self.assertEqual(served, 1)
        self.assertEqual(tested, 1)

    def testThrottling50(self):
        (served, tested) = RandomAUSTest(self.AUS, backgroundRate=50, force=False, mapping='b')
        self.assertEqual(served,  50)
        self.assertEqual(tested, 100)

    def testThrottling25(self):
        (served, tested) = RandomAUSTest(self.AUS, backgroundRate=25, force=False, mapping='b')
        self.assertEqual(served,  25)
        self.assertEqual(tested, 100)

    def testThrottlingZero(self):
        (served, tested) = RandomAUSTest(self.AUS, backgroundRate=0, force=False, mapping='b')
        self.assertEqual(served,   0)
        self.assertEqual(tested, 100)

    def testThrottling25WithForcing(self):
        (served, tested) = RandomAUSTest(self.AUS, backgroundRate=25, force=True, mapping='b')
        self.assertEqual(served, 1)
        self.assertEqual(tested, 1)

class TestAUS(unittest.TestCase):
    def setUp(self):
        self.AUS = AUS()
        self.AUS.setSpecialHosts(('http://special.org/',))
        self.AUS.setDb('sqlite:///:memory:')
        self.AUS.db.setDomainWhitelist(('special.org',))
        self.AUS.db.create()
        self.relData = {}
        self.relData['b'] = ReleaseBlobV1(
            name='b',
            schema_version=1,
            appv='1.0',
            extv='1.0',
            hashFunction='sha512',
            detailsUrl='http://example.org/details',
            licenseUrl='http://example.org/license',
            platforms=dict(
                p=dict(
                    buildID=1,
                    locales=dict(
                        l=dict(
                            complete={
                                'filesize': '1',
                                'from': '*',
                                'hashValue': '1',
                                'fileUrl': 'http://special.org/?foo=a',
                            }
                        ),
                        m=dict(
                            complete={
                                'filesize': '1',
                                'from': '*',
                                'hashValue': '1',
                                'fileUrl': 'http://boring.org/a',
                            }
                        )
                    )
                )
            )
        )
        self.AUS.db.releases.t.insert().execute(name='b', product='b', version='1.0', data_version=1,
                                                data=json.dumps(self.relData['b']))
        self.relData['c'] = ReleaseBlobV2(
            name='c',
            schema_version=2,
            appVersion='2.0',
            displayVersion='2.0',
            platformVersion='2.0',
            hashFunction='sha512',
            detailsUrl='http://example.org/details',
            licenseUrl='http://example.org/license',
            actions='silent',
            billboardURL='http://example.com/billboard',
            openURL='http://example.com/url',
            notificationURL='http://example.com/notification',
            alertURL='http://example.com/alert',
            showPrompt='false',
            showNeverForVersion='true',
            showSurvey='false',
            platforms=dict(
                p=dict(
                    buildID=2,
                    locales=dict(
                        o=dict(
                            complete={
                                'filesize': '2',
                                'from': '*',
                                'hashValue': '2',
                                'fileUrl': 'http://special.org/mar'
                            }
                        )
                    )
                )
            )
        )
        self.AUS.db.releases.t.insert().execute(name='c', product='c', version='2.0', data_version=1,
                                                data=json.dumps(self.relData['c']))

    def testSpecialQueryParam(self):
        updateData = self.AUS.expandRelease(
            dict(name=None, buildTarget='p', locale='l', channel='foo', force=False),
            self.relData['b'],
            'minor',
        )
        self.assertEqual(updateData['patches'][0]['URL'],
                         'http://special.org/?foo=a')

    def testSpecialQueryParamForced(self):
        updateData = self.AUS.expandRelease(
            dict(name=None, buildTarget='p', locale='l', channel='foo', force=True),
            self.relData['b'],
            'minor',
        )
        self.assertEqual(updateData['patches'][0]['URL'],
                         'http://special.org/?foo=a&force=1')

    def testNonSpecialQueryParam(self):
        updateData = self.AUS.expandRelease(
            dict(name=None, buildTarget='p', locale='m', channel='foo', force=False),
            self.relData['b'],
            'minor',
        )
        self.assertEqual(updateData['patches'][0]['URL'],
                         'http://boring.org/a')

    def testNonSpecialQueryParamForced(self):
        updateData = self.AUS.expandRelease(
            dict(name=None, buildTarget='p', locale='m', channel='foo', force=True),
            self.relData['b'],
            'minor',
        )
        self.assertEqual(updateData['patches'][0]['URL'],
                         'http://boring.org/a')

    def testMultipleSpecialHosts(self):
        self.AUS.setSpecialHosts(('http://special.org/', 'http://veryspecial.org'))
        updateData = self.AUS.expandRelease(
            dict(name=None, buildTarget='p', locale='l', channel='foo', force=True),
            self.relData['b'],
            'minor',
        )
        self.assertEqual(updateData['patches'][0]['URL'],
                         'http://special.org/?foo=a&force=1')

    def testNoSpecialDefined(self):
        self.AUS.setSpecialHosts(None)
        updateData = self.AUS.expandRelease(
            dict(name=None, buildTarget='p', locale='m', channel='foo', force=True),
            self.relData['b'],
            'minor',
        )
        self.assertEqual(updateData['patches'][0]['URL'],
                         'http://boring.org/a')

    def testCreateXMLAllowedDomain(self):
        xml = self.AUS.createXML(
            dict(name=None, buildTarget='p', locale='l', channel='foo', force=False),
            self.relData['b'],
            'minor',
        )
        # We need to load and re-xmlify these to make sure we don't get failures due to whitespace differences.
        returned = minidom.parseString(xml)
        expected = minidom.parseString("""<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://special.org/?foo=a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>
</updates>
""")
        self.assertEqual(returned.toxml(), expected.toxml())

    def testCreateXMLForbiddenDomain(self):
        # A CEF event gets logged when a forbidden domain is detected,
        # which depends on a Request being set.
        # We don't care about cef events here though, so we'll mock them away
        # See http://docs.python.org/dev/library/unittest.mock#id4 for why
        # AUS.cef_event is patched instead of log.cef_event
        with mock.patch('auslib.AUS.cef_event') as c:
            c.return_value = None
            xml = self.AUS.createXML(
                dict(name=None, buildTarget='p', locale='m', channel='foo', force=False),
                self.relData['b'],
                'minor',
            )
            # An empty update contains an <updates> tag with a newline, which is what we're expecting here
            self.assertEqual(minidom.parseString(xml).getElementsByTagName('updates')[0].firstChild.nodeValue, '\n')

    def testSchemaV1XML(self):
        xml = self.AUS.createXML(
            dict(name=None, buildTarget='p', locale='l', channel='foo', force=False),
            self.relData['b'], update_type='minor',
        )
        expected = """\
<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="1" detailsURL="http://example.org/details" licenseURL="http://example.org/license">
        <patch type="complete" URL="http://special.org/?foo=a" hashFunction="sha512" hashValue="1" size="1"/>
    </update>\n</updates>\
"""
        self.assertEqual(xml, expected)

    def testSchemaV2XML(self):
        xml = self.AUS.createXML(
            dict(name=None, buildTarget='p', locale='o', channel='foo', force=False),
            self.relData['c'], update_type='minor',
        )
        expected = """\
<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="2.0" appVersion="2.0" platformVersion="2.0" buildID="2" detailsURL="http://example.org/details" licenseURL="http://example.org/license" billboardURL="http://example.com/billboard" showPrompt="false" showNeverForVersion="true" showSurvey="false" actions="silent" openURL="http://example.com/url" notificationURL="http://example.com/notification" alertURL="http://example.com/alert">
        <patch type="complete" URL="http://special.org/mar" hashFunction="sha512" hashValue="2" size="2"/>
    </update>\n</updates>\
"""
        self.assertEqual(xml, expected)
