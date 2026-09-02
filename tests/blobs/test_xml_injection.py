"""Adversarial guard tests: rendering any XML blob type with injection payloads
in its escapable (URL / free-form / reflected) fields must still produce
well-formed XML, with no raw markup leaking through.

These are a safety net for the "someone forgets to escape a new field" concern:
attribute values are meant to flow through auslib.blobs.base.renderXMLAttributes,
which escapes by construction. If a new emit site bypasses it with raw string
interpolation, the malformed output will fail xml parsing here.

Note: schema-restricted fields (versions, hashes, vendor/addon keys) are NOT
exercised here -- they are protected on input by their schema patterns, covered
by the per-blob schema-rejection tests, and are deliberately not escaped on
output.
"""

import json
import unittest
from xml.dom.minidom import parseString

from auslib.blobs.base import createBlob

# Contains ", <, >, & and a fake attribute/tag -- everything needed to break out
# of an attribute or open a new element if a value were left unescaped.
PAYLOAD = 'x"><injected evil="1">&y'
# A URL on an allowlisted domain, carrying the payload in its path/query so it
# survives the domain allowlist check and reaches the response.
URL_PAYLOAD = "http://a.com/" + PAYLOAD


def assemble(blob, query, allowlisted_domains, special_force_hosts=None):
    parts = blob.getHeaderXML()
    parts.append(blob.getInnerHeaderXML(query, "minor", allowlisted_domains, special_force_hosts))
    parts.extend(blob.getInnerXML(query, "minor", allowlisted_domains, special_force_hosts))
    parts.append(blob.getInnerFooterXML(query, "minor", allowlisted_domains, special_force_hosts))
    parts.append(blob.getFooterXML())
    return "\n".join(p for p in parts if p)


def update_line_doc(blob, query, allowlisted_domains):
    # The apprelease <update ...> line carries the free-form/URL attributes
    # (detailsURL, actions, openURL, ...). We test it in isolation to avoid the
    # unrelated fileUrl-resolution machinery; patch-URL escaping is covered by
    # test_apprelease.TestSpecialQueryParams and TestXMLAttributeInjectionHardening.
    line = blob.getInnerHeaderXML(query, "minor", allowlisted_domains, None)
    return "<updates>\n" + line + "\n</update>\n</updates>"


class TestXMLWellFormednessUnderInjection(unittest.TestCase):
    def setUp(self):
        self.allowlistedDomains = {"a.com": ("g",)}

    def _assertSafe(self, xml):
        # Raises ExpatError if any payload broke out of its attribute/element.
        parseString(xml)
        # And the raw markup must not appear un-escaped anywhere.
        self.assertNotIn("<injected", xml)
        self.assertNotIn('evil="1"', xml)

    def testGMPBlob(self):
        blob = createBlob(
            json.dumps(
                {
                    "name": "g",
                    "schema_version": 1000,
                    "hashFunction": "sha512",
                    "vendors": {
                        "v": {
                            "version": "1",
                            "platforms": {"p": {"filesize": 1, "hashValue": "abc", "fileUrl": URL_PAYLOAD, "mirrorUrls": [URL_PAYLOAD]}},
                        }
                    },
                }
            )
        )
        query = {"product": "g", "buildTarget": "p"}
        self._assertSafe(assemble(blob, query, self.allowlistedDomains))

    def testSystemAddonsBlob(self):
        blob = createBlob(
            json.dumps(
                {
                    "name": "s",
                    "schema_version": 5000,
                    "hashFunction": "sha512",
                    "addons": {"a": {"version": "1", "platforms": {"p": {"filesize": 1, "hashValue": "abc", "fileUrl": URL_PAYLOAD}}}},
                }
            )
        )
        query = {"product": "g", "buildTarget": "p"}
        self._assertSafe(assemble(blob, query, self.allowlistedDomains))

    def testAppReleaseV9UpdateLine(self):
        blob = createBlob(
            json.dumps(
                {
                    "name": "n",
                    "schema_version": 9,
                    "hashFunction": "sha512",
                    "appVersion": "31.0",
                    "displayVersion": "31.0",
                    "updateLine": [{"for": {}, "fields": {"detailsURL": URL_PAYLOAD, "actions": PAYLOAD, "openURL": URL_PAYLOAD, "type": "minor"}}],
                    "platforms": {"p": {"buildID": 50, "locales": {"l": {}}}},
                }
            )
        )
        query = {"product": "g", "buildTarget": "p", "locale": "l", "channel": "a", "version": "1.0", "buildID": "1"}
        self._assertSafe(update_line_doc(blob, query, self.allowlistedDomains))

    def testAppReleaseV2UpdateLineOptionalAttributes(self):
        blob = createBlob(
            json.dumps(
                {
                    "name": "n",
                    "schema_version": 2,
                    "hashFunction": "sha512",
                    "appVersion": "1.0",
                    "displayVersion": "1.0",
                    "platformVersion": "1.0",
                    "detailsUrl": URL_PAYLOAD,
                    "licenseUrl": URL_PAYLOAD,
                    "actions": PAYLOAD,
                    "billboardURL": URL_PAYLOAD,
                    "openURL": URL_PAYLOAD,
                    "notificationURL": URL_PAYLOAD,
                    "alertURL": URL_PAYLOAD,
                    "platforms": {"p": {"buildID": 1, "locales": {"l": {}}}},
                }
            )
        )
        query = {"product": "g", "buildTarget": "p", "locale": "l", "channel": "a", "version": "1.0", "buildID": "1"}
        self._assertSafe(update_line_doc(blob, query, self.allowlistedDomains))

    def testDesupportBlobReflectedQuery(self):
        blob = createBlob(json.dumps({"name": "d", "schema_version": 50, "detailsUrl": "http://a.com/%LOCALE%/%VERSION%", "displayVersion": "50.0"}))
        # locale and version come from the (client-supplied) update request.
        query = {"product": "g", "buildTarget": "p_x", "locale": PAYLOAD, "version": PAYLOAD, "channel": "a"}
        self._assertSafe(assemble(blob, query, self.allowlistedDomains))
