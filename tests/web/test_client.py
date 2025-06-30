# coding: latin-1
import logging
import os
import time
import unittest
from collections import defaultdict
from contextlib import ExitStack
from tempfile import mkstemp
from xml.dom import minidom

import mock
import pytest
from hypothesis import assume, example, given
from hypothesis.strategies import characters, integers, just, text

import auslib.services.releases as releases_service
import auslib.web.public.client as client_api
from auslib.blobs.base import createBlob
from auslib.errors import BadDataError
from auslib.global_state import cache, dbo
from auslib.web.public.base import flask_app as app
from auslib.web.public.client import extract_query_version

mock_autograph_exception_count = 0


def setUpModule():
    # Silence SQLAlchemy-Migrate's debugging logger
    logging.getLogger("migrate").setLevel(logging.CRITICAL)


def validate_cache_stats(lookups, hits, misses, data_version_lookups, data_version_hits, data_version_misses, mocked_incr):
    for cache_name in ("releases", "release_assets"):
        c = cache.caches[cache_name]
        assert c.lookups == lookups, cache_name
        assert c.hits == hits, cache_name
        assert c.misses == misses, cache_name
        mocked_incr.assert_has_calls([mock.call(f"{cache_name}.hits")] * hits, any_order=True)
        mocked_incr.assert_has_calls([mock.call(f"{cache_name}.misses")] * misses, any_order=True)

    for cache_name in ("releases_data_version", "release_assets_data_versions"):
        c = cache.caches[cache_name]
        assert c.lookups == data_version_lookups, cache_name
        assert c.hits == data_version_hits, cache_name
        assert c.misses == data_version_misses, cache_name
        mocked_incr.assert_has_calls([mock.call(f"{cache_name}.hits")] * data_version_hits, any_order=True)
        mocked_incr.assert_has_calls([mock.call(f"{cache_name}.misses")] * data_version_misses, any_order=True)


class TestGetSystemCapabilities(unittest.TestCase):
    def testUnprefixedInstructionSetOnly(self):
        self.assertEqual(client_api.getSystemCapabilities("SSE3"), {"instructionSet": "SSE3", "memory": None, "jaws": None})

    def testUnprefixedInstructionSetAndMemory(self):
        self.assertEqual(client_api.getSystemCapabilities("SSE3,8095"), {"instructionSet": "SSE3", "memory": 8095, "jaws": None})

    def testPrefixedInstructionSetAndMemory(self):
        self.assertEqual(client_api.getSystemCapabilities("ISET:SSE2,MEM:6321"), {"instructionSet": "SSE2", "memory": 6321, "jaws": None})

    def testPrefixedInstructionSetMemoryAndJaws(self):
        self.assertEqual(client_api.getSystemCapabilities("ISET:SSE2,MEM:6321,JAWS:1"), {"instructionSet": "SSE2", "memory": 6321, "jaws": True})

    def testNothingProvided(self):
        self.assertEqual(client_api.getSystemCapabilities("NA"), {"instructionSet": "NA", "memory": None, "jaws": None})

    def testNonIntegerMemory(self):
        # Real things we've seen for "memory"
        self.assertEqual(
            client_api.getSystemCapabilities("ISET:SSE2,MEM:16384');declare @q varchar(99);set @q='"), {"instructionSet": "SSE2", "memory": None, "jaws": None}
        )
        self.assertEqual(client_api.getSystemCapabilities("ISET:SSE2,MEM:-nan(ind)"), {"instructionSet": "SSE2", "memory": None, "jaws": None})
        self.assertEqual(client_api.getSystemCapabilities("ISET:SSE2,MEM:8.1023"), {"instructionSet": "SSE2", "memory": None, "jaws": None})
        self.assertEqual(client_api.getSystemCapabilities("ISET:SSE2,MEM:unknown"), {"instructionSet": "SSE2", "memory": None, "jaws": None})

    def testUnknownField(self):
        self.assertEqual(client_api.getSystemCapabilities("ISET:SSE3,MEM:6721,PROC:Intel"), {"instructionSet": "SSE3", "memory": 6721, "jaws": None})

    def testBadFieldFormat(self):
        self.assertEqual(
            client_api.getSystemCapabilities("ISET:SSE4_2,MEM:32768,(select*from(select(sleep(20)))a)"),
            {"instructionSet": "SSE4_2", "memory": 32768, "jaws": None},
        )

    def testNonBooleanJaws(self):
        self.assertEqual(
            client_api.getSystemCapabilities("ISET:SSE3,MEM:16268,JAWS:0%27%22%60%20%2d%2d%23%c0%22%c0%27%d5%22%d5%27aa"),
            {"instructionSet": "SSE3", "memory": 16268, "jaws": None},
        )


@pytest.mark.usefixtures("current_db_schema")
class ClientTestCommon(unittest.TestCase):
    def assertHttpResponse(self, http_response):
        self.assertEqual(http_response.status_code, 200, http_response.get_data())
        self.assertEqual(http_response.mimetype, "text/xml")

    def assertUpdatesAreEmpty(self, http_reponse):
        self.assertHttpResponse(http_reponse)
        # An empty update contains an <updates> tag with a newline, which is what we're expecting here
        self.assertEqual(minidom.parseString(http_reponse.get_data()).getElementsByTagName("updates")[0].firstChild.nodeValue, "\n")

    def assertUpdateEqual(self, http_reponse, expected_xml_string):
        self.assertHttpResponse(http_reponse)
        returned = minidom.parseString(http_reponse.get_data())
        expected = minidom.parseString(expected_xml_string)
        self.assertEqual(returned.toxml(), expected.toxml())

    def assertUpdateTextEqual(self, http_response, expected):
        self.assertHttpResponse(http_response)
        returned = http_response.get_data(as_text=True)
        self.assertEqual(returned, expected)


class ClientTestBase(ClientTestCommon):
    maxDiff = 2000

    @classmethod
    def setUpClass(cls):
        # Error handlers are removed in order to give us better debug messages
        cls.error_spec = app.error_handler_spec
        # Ripped from https://github.com/pallets/flask/blob/2.3.3/src/flask/scaffold.py#L131-L134
        app.error_handler_spec = defaultdict(lambda: defaultdict(dict))

    @classmethod
    def tearDownClass(cls):
        app.error_handler_spec = cls.error_spec

    @pytest.fixture(autouse=True)
    def setup(self, insert_release, firefox_54_0_1_build1, firefox_56_0_build1, superblob_e8f4a19, hotfix_bug_1548973_1_1_4, firefox_100_0_build1, timecop_1_0):
        cache.reset()
        cache.make_cache("releases", 50, 10)
        cache.make_cache("releases_data_version", 50, 5)
        cache.make_cache("release_assets", 50, 10)
        cache.make_cache("release_assets_data_versions", 50, 5)
        self.version_fd, self.version_file = mkstemp()
        app.config["DEBUG"] = True
        app.config["SPECIAL_FORCE_HOSTS"] = ("http://a.com", "http://download.mozilla.org")
        app.config["ALLOWLISTED_DOMAINS"] = {
            "a.com": ("b", "c", "e", "f", "response-a", "response-b", "s", "responseblob-a", "responseblob-b", "q", "fallback", "distTest"),
            "download.mozilla.org": ("Firefox",),
            "archive.mozilla.org": ("Firefox",),
            "ftp.mozilla.org": ("SystemAddons",),
        }
        app.config["VERSION_FILE"] = self.version_file
        app.config["CONTENT_SIGNATURE_PRODUCTS"] = ["gmp"]
        with open(self.version_file, "w+") as f:
            f.write(
                """
{
  "source":"https://github.com/mozilla-releng/balrog",
  "version":"1.0",
  "commit":"abcdef123456"
}
"""
            )
        dbo.setDb("sqlite:///:memory:")
        self.metadata.create_all(dbo.engine)
        dbo.setDomainAllowlist(app.config["ALLOWLISTED_DOMAINS"])
        self.client = app.test_client()
        dbo.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="b", update_type="minor", product="b", data_version=1, alias="moz-releng")
        dbo.releases.t.insert().execute(
            name="b",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "b",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "2",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/z"
                    }
                },
                "xh": {
                    "complete": {
                        "filesize": "5",
                        "from": "*",
                        "hashValue": "6",
                        "fileUrl": "http://a.com/x"
                    }
                }
            }
        }
    }
}
"""
            ),
        )

        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="s", update_type="minor", product="s", instructionSet="SSE", data_version=1)
        dbo.releases.t.insert().execute(
            name="s",
            product="s",
            data_version=1,
            data=createBlob(
                """
{
    "name": "s",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "5",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "5",
                        "from": "*",
                        "hashValue": "5",
                        "fileUrl": "http://a.com/s"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(priority=90, backgroundRate=0, mapping="q", update_type="minor", product="q", fallbackMapping="fallback", data_version=1)
        dbo.releases.t.insert().execute(
            name="q",
            product="q",
            data_version=1,
            data=createBlob(
                """
{
    "name": "q",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "5",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "5",
                        "from": "*",
                        "hashValue": "5",
                        "fileUrl": "http://a.com/q"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.releases.t.insert().execute(
            name="fallback",
            product="q",
            data_version=1,
            data=createBlob(
                """
{
    "name": "fallback",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "5",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "5",
                        "from": "*",
                        "hashValue": "5",
                        "fileUrl": "http://a.com/fallback"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(
            rule_id=42024, priority=90, backgroundRate=100, mapping="c", update_type="minor", product="c", distribution="default", data_version=1
        )
        dbo.releases.t.insert().execute(
            name="c",
            product="c",
            data_version=1,
            data=createBlob(
                """
{
    "name": "c",
    "schema_version": 1,
    "appv": "10.0",
    "extv": "10.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "11",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "12",
                        "from": "*",
                        "hashValue": "13",
                        "fileUrl": "http://a.com/y"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(
            priority=90,
            backgroundRate=100,
            mapping="distTest",
            update_type="minor",
            product="distTest",
            distribution="mozilla1,mozilla2,mozilla3",
            data_version=1,
        )
        dbo.releases.t.insert().execute(
            name="distTest",
            product="distTest",
            data_version=1,
            data=createBlob(
                """
{
    "name": "distTest",
    "schema_version": 1,
    "appv": "10.0",
    "extv": "10.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "11",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "12",
                        "from": "*",
                        "hashValue": "13",
                        "fileUrl": "http://a.com/distTest"
                    }
                }
            }
        }
    }
}
"""
            ),
        )

        dbo.rules.t.insert().execute(priority=80, backgroundRate=100, mapping="c2", update_type="minor", product="c", data_version=1)
        dbo.releases.t.insert().execute(
            name="c2",
            product="c",
            data_version=1,
            data=createBlob(
                """
{
    "name": "c2",
    "schema_version": 1,
    "appv": "15.0",
    "extv": "15.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "51",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "52",
                        "from": "*",
                        "hashValue": "53",
                        "fileUrl": "http://a.com/x"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="d", update_type="minor", product="d", data_version=1)
        dbo.releases.t.insert().execute(
            name="d",
            product="d",
            data_version=1,
            data=createBlob(
                """
{
    "name": "d",
    "schema_version": 1,
    "appv": "20.0",
    "extv": "20.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "21",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 22,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://evil.com/y"
                    }
                }
            }
        }
    }
}
"""
            ),
        )

        dbo.rules.t.insert().execute(priority=90, backgroundRate=0, mapping="e", update_type="minor", product="e", data_version=1)
        dbo.releases.t.insert().execute(
            name="e",
            product="e",
            data_version=1,
            data=createBlob(
                """
{
    "name": "e",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "25",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 22,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://a.com/y"
                    }
                }
            }
        }
    }
}
"""
            ),
        )

        dbo.rules.t.insert().execute(
            priority=90, backgroundRate=100, mapping="f", update_type="minor", product="f", channel="a", memory="<=8000", data_version=1
        )
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="f", update_type="minor", product="f", channel="b", memory="9000", data_version=1)
        dbo.rules.t.insert().execute(
            priority=90, backgroundRate=100, mapping="f", update_type="minor", product="f", channel="c", memory=">10000", data_version=1
        )
        dbo.releases.t.insert().execute(
            name="f",
            product="f",
            data_version=1,
            data=createBlob(
                """
{
    "name": "f",
    "schema_version": 1,
    "hashFunction": "sha512",
    "appv": "1.0",
    "extv": "1.0",
    "platforms": {
        "p": {
            "buildID": "35",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 33,
                        "from": "*",
                        "hashValue": "34",
                        "fileUrl": "http://a.com/f"
                    }
                }
            }
        }
    }
}
"""
            ),
        )

        dbo.rules.t.insert().execute(priority=200, backgroundRate=100, mapping="gmp", update_type="minor", product="gmp", data_version=1)
        dbo.rules.t.insert().execute(
            priority=200,
            backgroundRate=100,
            mapping="gmp-with-one-response-product",
            update_type="minor",
            product="gmp-with-one-response-product",
            data_version=1,
        )
        dbo.rules.t.insert().execute(priority=190, backgroundRate=100, mapping="response-a", update_type="minor", product="response-a", data_version=1)
        dbo.rules.t.insert().execute(priority=180, backgroundRate=100, mapping="response-b", update_type="minor", product="response-b", data_version=1)
        dbo.releases.t.insert().execute(
            name="gmp-with-one-response-product",
            product="gmp-with-one-response-product",
            data_version=1,
            data=createBlob(
                """
{
    "name": "superblob",
    "schema_version": 4000,
    "products": ["response-a"]
}
"""
            ),
        )
        dbo.releases.t.insert().execute(
            name="gmp",
            product="gmp",
            data_version=1,
            data=createBlob(
                """
{
    "name": "superblob",
    "schema_version": 4000,
    "products": ["response-a", "response-b"]
}
"""
            ),
        )
        dbo.releases.t.insert().execute(
            name="response-a",
            product="response-a",
            data_version=1,
            data=createBlob(
                """
{
    "name": "response-a",
    "schema_version": 1,
    "extv": "2.5",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "25",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 22,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://a.com/public"
                    }
                }
            }
        },
        "q": {
            "buildID": "25",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 22,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://a.com/public-q"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.releases.t.insert().execute(
            name="response-b",
            product="response-b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "response-b",
    "schema_version": 1,
    "extv": "2.5",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "25",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 27777777,
                        "from": "*",
                        "hashValue": "23",
                        "fileUrl": "http://a.com/b"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(
            priority=180, backgroundRate=100, mapping="systemaddons-uninstall", update_type="minor", product="systemaddons-uninstall", data_version=1
        )
        dbo.releases.t.insert().execute(
            name="systemaddons-uninstall",
            product="systemaddons-uninstall",
            data_version=1,
            data=createBlob(
                """
{
    "name": "fake",
    "schema_version": 5000,
    "hashFunction": "SHA512",
    "uninstall": true
}
"""
            ),
        )
        dbo.rules.t.insert().execute(priority=180, backgroundRate=100, mapping="systemaddons", update_type="minor", product="systemaddons", data_version=1)
        dbo.releases.t.insert().execute(
            name="systemaddons",
            product="systemaddons",
            data_version=1,
            data=createBlob(
                """
{
    "name": "fake",
    "schema_version": 5000,
    "hashFunction": "SHA512",
    "uninstall": false,
    "addons": {
        "c": {
            "version": "1",
            "platforms": {
                "p": {
                    "filesize": 2,
                    "hashValue": "3",
                    "fileUrl": "http://a.com/blah"
                }
            }
        }
    }
}
"""
            ),
        )

        dbo.rules.t.insert().execute(
            priority=1000,
            backgroundRate=0,
            mapping="product_that_should_not_be_updated-1.1",
            update_type="minor",
            product="product_that_should_not_be_updated",
            data_version=1,
        )
        dbo.releases.t.insert().execute(
            name="product_that_should_not_be_updated-1.1",
            product="product_that_should_not_be_updated",
            data_version=1,
            data=createBlob(
                """
{
    "name": "product_that_should_not_be_updated-1.1",
    "schema_version": 1,
    "appv": "1.1",
    "extv": "1.1",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "2",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/z"
                    }
                }
            }
        }
    }
}
"""
            ),
        )

        dbo.rules.t.insert().execute(
            priority=90,
            backgroundRate=100,
            mapping="product_that_should_not_be_updated-2.0",
            update_type="minor",
            product="product_that_should_not_be_updated",
            data_version=1,
        )
        dbo.releases.t.insert().execute(
            name="product_that_should_not_be_updated-2.0",
            product="product_that_should_not_be_updated",
            data_version=1,
            data=createBlob(
                """
{
    "name": "product_that_should_not_be_updated-2.0",
    "schema_version": 1,
    "appv": "2.0",
    "extv": "2.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "2",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/z"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(
            priority=200,
            backgroundRate=100,
            mapping="superblobaddon-with-multiple-response-blob",
            update_type="minor",
            product="superblobaddon-with-multiple-response-blob",
            data_version=1,
        )
        dbo.rules.t.insert().execute(
            priority=200,
            backgroundRate=100,
            mapping="superblobaddon-with-multiple-response-blob-glob",
            update_type="minor",
            product="superblobaddon-with-multiple-response-blob-glob",
            version="99.8.*",
            data_version=1,
        )
        dbo.rules.t.insert().execute(
            priority=200,
            backgroundRate=100,
            mapping="superblobaddon-with-one-response-blob",
            update_type="minor",
            product="superblobaddon-with-one-response-blob",
            data_version=1,
        )
        dbo.releases.t.insert().execute(
            name="superblobaddon-with-one-response-blob",
            product="superblobaddon-with-one-response-blob",
            data_version=1,
            data=createBlob(
                """
{
    "name": "superblobaddon",
    "schema_version": 4000,
    "blobs": ["responseblob-a"]
}
"""
            ),
        )
        dbo.releases.t.insert().execute(
            name="superblobaddon-with-multiple-response-blob",
            product="superblobaddon-with-multiple-response-blob",
            data_version=1,
            data=createBlob(
                """
{
    "name": "superblobaddon",
    "schema_version": 4000,
    "blobs": ["responseblob-a", "responseblob-b"]
}
"""
            ),
        )
        dbo.releases.t.insert().execute(
            name="superblobaddon-with-multiple-response-blob-glob",
            product="superblobaddon-with-multiple-response-blob-glob",
            data_version=1,
            data=createBlob(
                """
{
    "name": "superblobaddon",
    "schema_version": 4000,
    "blobs": ["responseblob-a", "responseblob-b"]
}
"""
            ),
        )
        dbo.releases.t.insert().execute(
            name="responseblob-a",
            product="responseblob-a",
            data_version=1,
            data=createBlob(
                """
{
    "name": "responseblob-a",
    "schema_version": 5000,
    "hashFunction": "SHA512",
    "addons": {
        "c": {
            "version": "1",
            "platforms": {
                "p": {
                    "filesize": 2,
                    "hashValue": "3",
                    "fileUrl": "http://a.com/e"
                },
                "q": {
                    "filesize": 4,
                    "hashValue": "5",
                    "fileUrl": "http://a.com/e"
                },
                "q2": {
                    "alias": "q"
                }
            }
        },
        "d": {
            "version": "5",
            "platforms": {
                "q": {
                    "filesize": 10,
                    "hashValue": "11",
                    "fileUrl": "http://a.com/c"
                },
                "default": {
                    "filesize": 20,
                    "hashValue": "50",
                    "fileUrl": "http://a.com/c"
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.releases.t.insert().execute(
            name="responseblob-b",
            product="responseblob-b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "responseblob-b",
    "schema_version": 5000,
    "hashFunction": "sha512",
    "uninstall": false,
    "addons": {
        "b": {
            "version": "1",
            "platforms": {
                "p": {
                        "filesize": 27,
                        "hashValue": "23",
                        "fileUrl": "http://a.com/b"

                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(
            priority=100, product="Firefox", channel="release", mapping="Firefox-56.0-build1", backgroundRate=100, update_type="minor", data_version=1
        )
        insert_release(firefox_54_0_1_build1, "Firefox", history=False)
        insert_release(firefox_56_0_build1, "Firefox", history=False)
        insert_release(firefox_100_0_build1, "Firefox", history=False)
        dbo.rules.t.insert().execute(
            priority=100, product="Firefox", channel="release100", mapping="Firefox-100.0-build1", backgroundRate=100, update_type="minor", data_version=1
        )
        dbo.rules.t.insert().execute(
            priority=300,
            product="SystemAddons",
            channel="releasesjson",
            mapping="Superblob-e8f4a19cfd695bf0eb66a2115313c31cc23a2369c0dc7b736d2f66d9075d7c66",
            backgroundRate=100,
            update_type="minor",
            data_version=1,
        )
        insert_release(superblob_e8f4a19, "SystemAddons", history=False)
        insert_release(hotfix_bug_1548973_1_1_4, "SystemAddons", history=False)
        insert_release(timecop_1_0, "SystemAddons", history=False)

        yield

        os.close(self.version_fd)
        os.remove(self.version_file)


@pytest.fixture(scope="function")
def mock_autograph(monkeypatch):
    monkeypatch.setitem(app.config, "AUTOGRAPH_gmp_URL", "fake")
    monkeypatch.setitem(app.config, "AUTOGRAPH_gmp_KEYID", "fake")
    monkeypatch.setitem(app.config, "AUTOGRAPH_gmp_USERNAME", "fake")
    monkeypatch.setitem(app.config, "AUTOGRAPH_gmp_PASSWORD", "fake")

    def mockreturn(*args):
        global mock_autograph_exception_count
        if mock_autograph_exception_count > 0:
            mock_autograph_exception_count -= 1
            raise Exception("unable to contact autograph")
        return ("abcdef", "https://this.is/a.x5u")

    import auslib.util.autograph

    monkeypatch.setattr(auslib.util.autograph, "_sign_hash", mockreturn)
    # speed up tests by not actually sleeping
    monkeypatch.setattr(time, "sleep", lambda _: None)


class ClientTest(ClientTestBase):
    def testGetHeaderArchitectureWindows(self):
        self.assertEqual(client_api.getHeaderArchitecture("WINNT_x86-msvc", "Firefox Intel Windows"), "Intel")

    def testGetHeaderArchitectureMacIntel(self):
        self.assertEqual(client_api.getHeaderArchitecture("Darwin_x86-gcc3-u-ppc-i386", "Firefox Intel Mac"), "Intel")

    def testGetHeaderArchitectureMacPPC(self):
        self.assertEqual(client_api.getHeaderArchitecture("Darwin_ppc-gcc3-u-ppc-i386", "Firefox PPC Mac"), "PPC")

    def testDontUpdateToYourself(self):
        ret = self.client.get("/update/3/b/1.0/2/p/l/a/a/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testDontUpdateBackwards(self):
        ret = self.client.get("/update/3/b/1.0/5/p/l/a/a/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testDontDecreaseVersion(self):
        ret = self.client.get("/update/3/c/15.0/1/p/l/a/a/default/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testVersion1Get(self):
        ret = self.client.get("/update/1/b/1.0/1/p/l/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )

    def testVersion2Get(self):
        ret = self.client.get("/update/2/b/1.0/0/p/l/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )

    def testVersion2GetIgnoresRuleWithDistribution(self):
        ret = self.client.get("/update/2/c/10.0/1/p/l/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="15.0" extensionVersion="15.0" buildID="51">
        <patch type="complete" URL="http://a.com/x" hashFunction="sha512" hashValue="53" size="52"/>
    </update>
</updates>
""",
        )

    def testVersion3Get(self):
        ret = self.client.get("/update/3/a/1.0/1/a/a/a/a/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testVersion3GetWithUpdate(self):
        ret = self.client.get("/update/3/b/1.0/1/p/l/a/a/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )

    def testVersion3GetWithDistribution(self):
        ret = self.client.get("/update/3/c/1.0/1/p/l/a/a/default/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="10.0" extensionVersion="10.0" buildID="11">
        <patch type="complete" URL="http://a.com/y" hashFunction="sha512" hashValue="13" size="12"/>
    </update>
</updates>
""",
        )

    def testVersion4GetWithDistribution(self):
        ret = self.client.get("/update/4/c/1.0/1/p/l/a/a/default/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="10.0" extensionVersion="10.0" buildID="11">
        <patch type="complete" URL="http://a.com/y" hashFunction="sha512" hashValue="13" size="12"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithDistribution(self):
        ret = self.client.get("/update/6/c/1.0/1/p/l/a/a/SSE/default/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="10.0" extensionVersion="10.0" buildID="11">
        <patch type="complete" URL="http://a.com/y" hashFunction="sha512" hashValue="13" size="12"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithDistributionInList(self):
        ret = self.client.get("/update/6/distTest/1.0/1/p/l/a/a/SSE/mozilla2/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="10.0" extensionVersion="10.0" buildID="11">
        <patch type="complete" URL="http://a.com/distTest" hashFunction="sha512" hashValue="13" size="12"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithDistributionNotInList(self):
        ret = self.client.get("/update/6/distTest/1.0/1/p/l/a/a/SSE/notinlist/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testVersion6GetNotMatchSubstringDistribution(self):
        ret = self.client.get("/update/6/distTest/1.0/1/p/l/a/a/SSE/zilla/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testVersion6GetDoesntMatchWrongDistribution(self):
        ret = self.client.get("/update/6/c/1.0/1/p/l/a/a/SSE/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="15.0" extensionVersion="15.0" buildID="51">
        <patch type="complete" URL="http://a.com/x" hashFunction="sha512" hashValue="53" size="52"/>
    </update>
</updates>
""",
        )

    def testVersion4Get(self):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithInstructionSetMatch(self):
        ret = self.client.get("/update/6/s/1.0/1/p/l/a/a/SSE/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="5">
        <patch type="complete" URL="http://a.com/s" hashFunction="sha512" hashValue="5" size="5"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithLessThanEqualToMemory(self):
        ret = self.client.get("/update/6/f/1.0/1/p/l/a/a/ISET:SSE3,MEM:8000/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="35">
        <patch type="complete" URL="http://a.com/f" hashFunction="sha512" hashValue="34" size="33"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithLessThanEqualToMemoryEncoded(self):
        ret = self.client.get("/update/6/f/1.0/1/p/l/a/a/ISET%3aSSE3%2cMEM%3a8000/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="35">
        <patch type="complete" URL="http://a.com/f" hashFunction="sha512" hashValue="34" size="33"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithExactMemory(self):
        ret = self.client.get("/update/6/f/1.0/1/p/l/b/a/ISET:SSE3,MEM:9000/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="35">
        <patch type="complete" URL="http://a.com/f" hashFunction="sha512" hashValue="34" size="33"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithExactMemoryEncoded(self):
        ret = self.client.get("/update/6/f/1.0/1/p/l/b/a/ISET%3aSSE3%2cMEM%3a9000/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="35">
        <patch type="complete" URL="http://a.com/f" hashFunction="sha512" hashValue="34" size="33"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithGreaterThanMemory(self):
        ret = self.client.get("/update/6/f/1.0/1/p/l/c/a/ISET:SSE3,MEM:11000/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="35">
        <patch type="complete" URL="http://a.com/f" hashFunction="sha512" hashValue="34" size="33"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithGreaterThanMemoryEncoded(self):
        ret = self.client.get("/update/6/f/1.0/1/p/l/c/a/ISET%3aSSE3%2cMEM%3a11000/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="35">
        <patch type="complete" URL="http://a.com/f" hashFunction="sha512" hashValue="34" size="33"/>
    </update>
</updates>
""",
        )

    def testVersion6GetWithFallbackMapping(self):
        ret = self.client.get("/update/6/q/1.0/1/p/l/a/a/a/a/1/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="5">
        <patch type="complete" URL="http://a.com/fallback" hashFunction="sha512" hashValue="5" size="5"/>
    </update>
</updates>
""",
        )

    def testShouldNotServeUpdateForOldVersion(self):
        ret = self.client.get("/update/6/q/2.0/1/p/l/a/a/a/a/1/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testVersion6GetWithoutInstructionSetMatch(self):
        ret = self.client.get("/update/6/s/1.0/1/p/l/a/a/SSE2/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testGetURLNotInAllowlist(self):
        ret = self.client.get("/update/3/d/20.0/1/p/l/a/a/a/a/update.xml")
        self.assertHttpResponse(ret)
        self.assertEqual(minidom.parseString(ret.get_data()).getElementsByTagName("updates")[0].firstChild.nodeValue, "\n    ")

    def testEmptySnippetMissingExtv(self):
        ret = self.client.get("/update/3/e/20.0/1/p/l/a/a/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testUnicodeAcceptedInURLFields(self):
        # /update/1, 2, and 3 are just subsets of /update/4 - so we don't
        # need to test them explicitly
        v4_url = "/update/4/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/update.xml"
        subs = [3, "e", "20.0", "1", "p", "l", "a", "a", "a", "a"]
        for i in range(0, 10):
            my_subs = subs[:]
            subs[i] = "ÃÃÃÃÃÃ"
            my_url = v4_url.format(*my_subs)
            ret = self.client.get(my_url)
            self.assertEqual(ret.status_code, 200)

        v5_url = "/update/5/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/update.xml"
        subs = [3, "e", "20.0", "1", "p", "l", "a", "a", "a", "a"]
        for i in range(0, 10):
            my_subs = subs[:]
            subs[i] = "ÃÃÃÃÃÃ"
            my_url = v5_url.format(*my_subs)
            ret = self.client.get(my_url)
            self.assertEqual(ret.status_code, 200)

        v6_url = "/update/6/{}/{}/{}/{}/{}/{}/{}/{}/{}/{}/update.xml"
        subs = [3, "e", "20.0", "1", "p", "l", "a", "a", "a", "a"]
        for i in range(0, 10):
            my_subs = subs[:]
            subs[i] = "ÃÃÃÃÃÃ"
            my_url = v6_url.format(*my_subs)
            ret = self.client.get(my_url)
            self.assertEqual(ret.status_code, 200)

    def testUnicodeAcceptedInQueryFields(self):
        for field in ("force", "mig64", "avast"):
            ret = self.client.get("/update/6/3/e/2.0.0/1/p/l/a/a/a/a/update.xml?{}=ÃÃÃÃÃÃ".format(field))
            self.assertEqual(ret.status_code, 200)

    def testRobotsExists(self):
        ret = self.client.get("/robots.txt")
        self.assertEqual(ret.status_code, 200)
        self.assertEqual(ret.mimetype, "text/plain")
        self.assertTrue("User-agent" in ret.get_data(as_text=True))

    def testContributeJsonExists(self):
        ret = self.client.get("/contribute.json")
        self.assertEqual(ret.status_code, 200)
        self.assertTrue(ret.get_json())
        self.assertEqual(ret.mimetype, "application/json")

    def testBadAvastURLsFromBug1125231(self):
        # Some versions of Avast have a bug in them that prepends "x86 "
        # to the locale. We need to make sure we handle this case correctly
        # so that these people can keep up to date.
        ret = self.client.get("/update/4/b/1.0/1/p/x86 l/a/a/a/a/1/update.xml")
        self.assertHttpResponse(ret)
        # Compare the Avast-style URL to the non-messed up equivalent. They
        # should get the same update XML.
        ret2 = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
        self.assertHttpResponse(ret2)
        self.assertEqual(ret.get_data(), ret2.get_data())

    def testFixForBug1125231DoesntBreakXhLocale(self):
        ret = self.client.get("/update/4/b/1.0/1/p/xh/a/a/a/a/1/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/x" hashFunction="sha512" hashValue="6" size="5"/>
    </update>
</updates>
""",
        )

    def testAvastURLsWithBadQueryArgs(self):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1%3Favast=1")
        self.assertHttpResponse(ret)
        ret2 = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1")
        self.assertHttpResponse(ret2)
        self.assertEqual(ret.get_data(), ret2.get_data())

    def testAvastURLsWithUnescapedBadQueryArgs(self):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1?avast=1")
        self.assertHttpResponse(ret)
        ret2 = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1")
        self.assertHttpResponse(ret2)
        self.assertEqual(ret.get_data(), ret2.get_data())

    def testAvastURLsWithGoodQueryArgs(self):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=1&avast=1")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z?force=1" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )

    @given(text(alphabet=characters(blacklist_categories=("Cs", "Po")), max_size=128))
    @example("")
    @example('1" name="Firefox 54.0" isOSUpdate="false" installDate="1498012260998')
    @example("1)")
    @example('"|sleep 7 #')
    def testForceParamWithBadInputs(self, x):
        assume(x != "1")
        assume(x != "-1")
        force_output = """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
"""
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?force=%s" % x)
        self.assertUpdateEqual(ret, force_output)

    def testDeprecatedEsrVersionStyleGetsUpdates(self):
        ret = self.client.get("/update/3/b/1.0esrpre/1/p/l/a/a/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )

    def testGMPResponseWithoutSigning(self):
        ret = self.client.get("/update/4/gmp/1.0/1/p/l/a/a/a/a/1/update.xml")
        assert "Content-Signature" not in ret.headers

    @pytest.mark.usefixtures("mock_autograph")
    @unittest.mock.patch("auslib.web.public.helpers.make_hash")
    def testGMPResponseWithSigning(self, mocked_make_hash):
        ret = self.client.get("/update/4/gmp/1.0/1/p/l/a/a/a/a/1/update.xml")
        assert ret.headers["Content-Signature"] == "x5u=https://this.is/a.x5u; p384ecdsa=abcdef"
        mocked_make_hash.assert_called_once_with(ret.text)

    @pytest.mark.usefixtures("mock_autograph")
    @unittest.mock.patch("auslib.web.public.helpers.make_hash")
    def testGMPResponseWithSigningAutographTempFailure(self, mocked_make_hash):
        global mock_autograph_exception_count
        mock_autograph_exception_count = 1
        ret = self.client.get("/update/4/gmp/1.0/1/p/l/a/a/a/a/1/update.xml")
        assert ret.headers["Content-Signature"] == "x5u=https://this.is/a.x5u; p384ecdsa=abcdef"
        mocked_make_hash.assert_called_once_with(ret.text)

    @pytest.mark.usefixtures("mock_autograph")
    def testGMPResponseWithSigningAutographPermanentFailure(self):
        global mock_autograph_exception_count
        mock_autograph_exception_count = 3
        with pytest.raises(Exception):
            self.client.get("/update/4/gmp/1.0/1/p/l/a/a/a/a/1/update.xml")

    def testGetWithResponseProducts(self):
        ret = self.client.get("/update/4/gmp/1.0/1/p/l/a/a/a/a/1/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <addons>
        <patch type="complete" URL="http://a.com/public" hashFunction="sha512" hashValue="23" size="22"/>
        <patch type="complete" URL="http://a.com/b" hashFunction="sha512" hashValue="23" size="27777777"/>
    </addons>
</updates>
""",
        )

    def testGetWithResponseProductsWithAbsentRule(self):
        ret = self.client.get("/update/4/gmp/1.0/1/q/l/a/a/a/a/1/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <addons>
        <patch type="complete" URL="http://a.com/public-q" hashFunction="sha512" hashValue="23" size="22"/>
    </addons>
</updates>
""",
        )

    def testGetWithResponseProductsWithOneRule(self):
        ret = self.client.get("/update/4/gmp-with-one-response-product/1.0/1/q/l/a/a/a/a/1/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <addons>
        <patch type="complete" URL="http://a.com/public-q" hashFunction="sha512" hashValue="23" size="22"/>
    </addons>
</updates>
""",
        )

    def testSystemAddonsBlobWithUninstall(self):
        ret = self.client.get("/update/4/systemaddons-uninstall/1.0/1/z/p/a/b/c/d/1/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <addons>
    </addons>
</updates>
""",
        )

    def testSystemAddonsBlobWithoutUninstall(self):
        ret = self.client.get("/update/4/systemaddons/1.0/1/z/p/a/b/c/d/1/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>


</updates>
""",
        )

    def testSuperBlobAddOnMultipleUpdates(self):
        ret = self.client.get("/update/3/superblobaddon-with-multiple-response-blob/1.0/1/p/l/a/a/a/a/update.xml")
        # update / 3 / gg / 3 / 1 / p / l / a / a / a / a / update.xml?force = 0
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <addons>
        <addon id="c" URL="http://a.com/e" hashFunction="SHA512" hashValue="3" size="2" version="1"/>
        <addon id="d" URL="http://a.com/c" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
        <addon id="b" URL="http://a.com/b" hashFunction="sha512" hashValue="23" size="27" version="1"/>
    </addons>
</updates>
""",
        )

    def testSuperBlobAddOnMultipleUpdatesGlob(self):
        # Matches version glob
        ret = self.client.get("/update/3/superblobaddon-with-multiple-response-blob-glob/99.8.1/1/p/l/a/a/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <addons>
        <addon id="c" URL="http://a.com/e" hashFunction="SHA512" hashValue="3" size="2" version="1"/>
        <addon id="d" URL="http://a.com/c" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
        <addon id="b" URL="http://a.com/b" hashFunction="sha512" hashValue="23" size="27" version="1"/>
    </addons>
</updates>
""",
        )

    def testSuperBlobAddOnNoUpdatesGlob(self):
        # Doesn't match version glob
        ret = self.client.get("/update/3/superblobaddon-with-multiple-response-blob-glob/99.9.0/1/p/l/a/a/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
</updates>
""",
        )

    def testSuperBlobAddOnOneUpdates(self):
        ret = self.client.get("/update/3/superblobaddon-with-one-response-blob/1.0/1/p/l/a/a/a/a/update.xml")
        # update / 3 / gg / 3 / 1 / p / l / a / a / a / a / update.xml?force = 0
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <addons>
        <addon id="c" URL="http://a.com/e" hashFunction="SHA512" hashValue="3" size="2" version="1"/>
        <addon id="d" URL="http://a.com/c" hashFunction="SHA512" hashValue="50" size="20" version="5"/>
    </addons>
</updates>
""",
        )

    def testUpdateBackgroundRateSetTo0(self):
        ret = self.client.get("/update/3/product_that_should_not_be_updated/1.0/1/p/l/a/a/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    @given(just("x"))
    @example(invalid_version="1x")
    @example(invalid_version="x1")
    def testUpdateInvalidQueryVersion(self, invalid_version):
        query_version = extract_query_version("/update/{}/a/b/c/update.xml".format(invalid_version))
        self.assertEqual(query_version, 0)

    @given(integers(min_value=1, max_value=100))
    @example(qv=1)
    def testUpdateQueryVersion(self, qv):
        query_version = extract_query_version("/update/{}/a/b/c/update.xml".format(qv))
        self.assertEqual(query_version, qv)

    # TODO: switch to text() after https://bugzilla.mozilla.org/show_bug.cgi?id=1387049 is ready
    # @given(text(min_size=1, max_size=20), text(min_size=1, max_size=20))
    @given(just("mig64"), just(1))
    def testUnknownQueryStringParametersAreAllowedV1(self, param, val):
        ret = self.client.get("/update/1/b/1.0/1/p/l/a/update.xml?{}={}".format(param, val))
        self.assertEqual(ret.status_code, 200)

    # TODO: switch to text() after https://bugzilla.mozilla.org/show_bug.cgi?id=1387049 is ready
    # @given(text(min_size=1, max_size=20), text(min_size=1, max_size=20))
    @given(just("mig64"), just(1))
    def testUnknownQueryStringParametersAreAllowedV2(self, param, val):
        ret = self.client.get("/update/2/c/10.0/1/p/l/a/a/update.xml?{}={}".format(param, val))
        self.assertEqual(ret.status_code, 200)

    # TODO: switch to text() after https://bugzilla.mozilla.org/show_bug.cgi?id=1387049 is ready
    # @given(text(min_size=1, max_size=20), text(min_size=1, max_size=20))
    @given(just("mig64"), just(1))
    def testUnknownQueryStringParametersAreAllowedV3(self, param, val):
        ret = self.client.get("/update/3/b/1.0/1/p/l/a/a/a/a/update.xml?{}={}".format(param, val))
        self.assertEqual(ret.status_code, 200)

    # TODO: switch to text() after https://bugzilla.mozilla.org/show_bug.cgi?id=1387049 is ready
    # @given(text(min_size=1, max_size=20), text(min_size=1, max_size=20))
    @given(just("mig64"), just(1))
    def testUnknownQueryStringParametersAreAllowedV4(self, param, val):
        ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml?{}={}".format(param, val))
        self.assertEqual(ret.status_code, 200)

    # TODO: switch to text() after https://bugzilla.mozilla.org/show_bug.cgi?id=1387049 is ready
    # @given(text(min_size=1, max_size=20), text(min_size=1, max_size=20))
    @given(just("mig64"), just(1))
    def testUnknownQueryStringParametersAreAllowedV5(self, param, val):
        ret = self.client.get("/update/5/b/1.0/1/p/l/a/a/a/a/1/update.xml?{}={}".format(param, val))
        self.assertEqual(ret.status_code, 200)

    # TODO: switch to text() after https://bugzilla.mozilla.org/show_bug.cgi?id=1387049 is ready
    # @given(text(min_size=1, max_size=20), text(min_size=1, max_size=20))
    @given(just("mig64"), just(1))
    def testUnknownQueryStringParametersAreAllowedV6(self, param, val):
        ret = self.client.get("/update/6/s/1.0/1/p/l/a/a/SSE/a/a/update.xml?{}={}".format(param, val))
        self.assertEqual(ret.status_code, 200)

    def test_get_with_release_with_missing_alias_in_from_release(self):
        ret = self.client.get(
            "/update/6/Firefox/54.0.1/20170628075643/WINNT_x86-msvc-x64/en-US/release"
            "/Windows_NT 6.1.0.0 (x86)/ISET:SSE3,MEM:4096,JAWS:0/default/default/update.xml"
        )
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="56.0" appVersion="56.0" platformVersion="56.0" buildID="20170918210324"
            detailsURL="https://www.mozilla.org/en-US/firefox/56.0/releasenotes/">
        <patch type="complete" URL="http://download.mozilla.org/?product=firefox-56.0-complete&amp;os=win&amp;lang=en-US" hashFunction="sha512"
                hashValue="3530e6d88cb44c0360ec2aec4e171bdc4a45a6062d2fcbca25264882876dce3486a23a903a71fa612f93fcf9261067dbe22e2f4f8cc8e7dd3e55578095b43b4e"
                size="38171451"/>
        <patch type="partial" URL="http://download.mozilla.org/?product=firefox-56.0-partial-54.0.1&amp;os=win&amp;lang=en-US" hashFunction="sha512"
                hashValue="ce5820a550a7b9c9d0be29c629242def63ff333bc12b5d2d45d23c8e2b238adda9bd9f7ef14649616aae8b78e9545e8e7ec3fe93ac1b3d808027254087790af6"
                size="26673535"/>
    </update>
</updates>""",
        )

    def test_get_with_release_in_new_tables(self):
        with ExitStack() as stack:
            mocked_releases_json_scheduled_changes = stack.enter_context(mock.patch("auslib.services.releases.dbo.releases_json.scheduled_changes"))
            mocked_release_assets_scheduled_changes = stack.enter_context(mock.patch("auslib.services.releases.dbo.release_assets.scheduled_changes"))
            mocked_get_base_row = stack.enter_context(mock.patch.object(releases_service, "get_base_row", wraps=releases_service.get_base_row))
            mocked_get_base_data_version = stack.enter_context(
                mock.patch.object(releases_service, "get_base_data_version", wraps=releases_service.get_base_data_version)
            )
            mocked_get_asset_rows = stack.enter_context(mock.patch.object(releases_service, "get_asset_rows", wraps=releases_service.get_asset_rows))
            mocked_get_asset_data_versions = stack.enter_context(
                mock.patch.object(releases_service, "get_asset_data_versions", wraps=releases_service.get_asset_data_versions)
            )
            t = stack.enter_context(mock.patch("time.time"))
            mocked_incr = stack.enter_context(mock.patch("statsd.StatsClient.incr"))
            # The lookups/hits/misses here come in multiples of 4 because we have:
            #  - a release that the rule is pointing to
            #  - 3 potential partials, all of which get looked at
            args = [
                {
                    # The first query should be all misses
                    "time": 10,
                    "lookups": 4,
                    "hits": 0,
                    "misses": 4,
                    "data_version_lookups": 4,
                    "data_version_hits": 0,
                    "data_version_misses": 4,
                },
                {
                    # Make sure a look up soon after will be fully cached (including data version)
                    "time": 13,
                    "lookups": 8,
                    "hits": 4,
                    "misses": 4,
                    "data_version_lookups": 8,
                    "data_version_hits": 4,
                    "data_version_misses": 4,
                },
                {
                    # And a look up after the data version cache expires should only invalidate data version caches
                    "time": 15,
                    "lookups": 12,
                    "hits": 8,
                    "misses": 4,
                    "data_version_lookups": 12,
                    "data_version_hits": 4,
                    "data_version_misses": 8,
                },
                {
                    # And make sure the main caches invalidate at the right time
                    "time": 20,
                    "lookups": 16,
                    "hits": 8,
                    "misses": 8,
                    "data_version_lookups": 16,
                    "data_version_hits": 4,
                    "data_version_misses": 12,
                },
                {
                    # After an update if data_version is expired but the blob is not we forcibly update the blob
                    "time": 25,
                    "lookups": 20,
                    "hits": 12,
                    "misses": 8,
                    "data_version_lookups": 20,
                    "data_version_hits": 4,
                    "data_version_misses": 16,
                    "update": True,
                },
                {
                    # Fresh query with expired caches
                    "time": 30,
                    "lookups": 24,
                    "hits": 12,
                    "misses": 12,
                    "data_version_lookups": 24,
                    "data_version_hits": 4,
                    "data_version_misses": 20,
                },
                {
                    # And now check the blob is updated after assets update
                    "time": 35,
                    "lookups": 28,
                    "hits": 16,
                    "misses": 12,
                    "data_version_lookups": 28,
                    "data_version_hits": 4,
                    "data_version_misses": 24,
                    "update_assets": True,
                },
            ]
            for arg in args:
                t.return_value = arg["time"]

                if arg.get("update"):
                    dbo.releases_json.update(where={"name": "Firefox-54.0.1-build1"}, what={}, old_data_version=1)
                if arg.get("update_assets"):
                    dbo.release_assets.update(
                        where={"name": "Firefox-54.0.1-build1", "path": ".platforms.Darwin_x86_64-gcc3-u-i386-x86_64.locales.af"}, what={}, old_data_version=1
                    )

                ret = self.client.get(
                    "/update/6/Firefox/54.0.1/20170628075643/WINNT_x86_64-msvc-x64/en-US/release"
                    "/Windows_NT 6.1.0.0 (x86)/ISET:SSE3,MEM:4096,JAWS:0/default/default/update.xml"
                )
                self.assertUpdateEqual(
                    ret,
                    """<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="56.0" appVersion="56.0" platformVersion="56.0" buildID="20170918210324"
            detailsURL="https://www.mozilla.org/en-US/firefox/56.0/releasenotes/">
        <patch type="complete" URL="http://download.mozilla.org/?product=firefox-56.0-complete&amp;os=win64&amp;lang=en-US" hashFunction="sha512"
            hashValue="d355668278173e0e55f26dc8d6951965317db5779659e0267907ea458d26ca8327a200631a48defca4f2d97066ee8545717a54a2f75569114bd03a0fa30ea37e"
            size="41323124"/>
        <patch type="partial" URL="http://download.mozilla.org/?product=firefox-56.0-partial-54.0.1&amp;os=win64&amp;lang=en-US" hashFunction="sha512"
            hashValue="34c7fd9b706111cbe62e86b02122cfc7cd7281a0f1d1569c7c69cf8c2944fab758fc08f4d09895403cb2a19208351801e0d26d6774b6abd727f103ba0db47cef"
            size="29129138"/>
    </update>
</updates>""",
                )
                validate_cache_stats(
                    arg["lookups"], arg["hits"], arg["misses"], arg["data_version_lookups"], arg["data_version_hits"], arg["data_version_misses"], mocked_incr
                )
                # In addition to validating cache hits and misses, we need to make
                # sure that we didn't call the database layer more than we expected
                # to without going through the cache layer.
                call_count = arg["misses"]
                if t.return_value >= 25:
                    call_count += 1
                assert mocked_get_base_row.call_count == call_count
                call_count = arg["misses"]
                if t.return_value >= 35:
                    call_count += 1
                assert mocked_get_asset_rows.call_count == call_count
                assert mocked_get_base_data_version.call_count == arg["data_version_misses"]
                assert mocked_get_asset_data_versions.call_count == arg["data_version_misses"]

            assert mocked_releases_json_scheduled_changes.select.call_count == 0
            assert mocked_release_assets_scheduled_changes.select.call_count == 0

    def test_superblob_multiresponse_releases_json(self):
        with ExitStack() as stack:
            mocked_releases_json_scheduled_changes = stack.enter_context(mock.patch("auslib.services.releases.dbo.releases_json.scheduled_changes"))
            mocked_release_assets_scheduled_changes = stack.enter_context(mock.patch("auslib.services.releases.dbo.release_assets.scheduled_changes"))
            ret = self.client.get("/update/3/SystemAddons/1.0/1/p/l/releasesjson/a/a/a/update.xml")
            self.assertUpdateEqual(
                ret,
                """<?xml version="1.0"?>
<updates>
    <addons>
        <addon id="hotfix-bug-1548973@mozilla.org"
            URL="https://ftp.mozilla.org/pub/system-addons/hotfix-bug-1548973/hotfix-bug-1548973@mozilla.org-1.1.4-signed.xpi"
            hashFunction="sha512"
            hashValue="c9c9e51fb7c642e01915f367c94d3aa00abfb3ea872f40220b8ead0dfd8e82c1e387bc5fca7cc55ac8f45322a3361a29f4947fe601eb9e94cfafad8ade2a1ce8"
            size="11436" version="1.1.4"/>
        <addon id="timecop@mozilla.com"
            URL="https://ftp.mozilla.org/pub/system-addons/timecop/timecop@mozilla.com-1.0-signed.xpi"
            hashFunction="sha512"
            hashValue="0bc9ebc56a07ba7d230e175aa9669b40aec1aff2aaef86a9323f27242fe671e07942e8f21d9b37e4643436cb317d5bd087eb471d55cc43174fb96206f8c5c0f7"
            size="5129" version="1.0"/>
    </addons>
</updates>
""",
            )

            assert mocked_releases_json_scheduled_changes.select.call_count == 0
            assert mocked_release_assets_scheduled_changes.select.call_count == 0

    def test_serve_update_with_rule_information_in_header(self):
        ret = self.client.get("/update/6/c/1.0/1/p/l/a/a/SSE/default/a/update.xml")
        assert "Rule-ID" in ret.headers
        assert "Rule-Data-Version" in ret.headers
        assert "42024" == ret.headers["Rule-ID"]
        assert "1" == ret.headers["Rule-Data-Version"]

    def test_version_100(self):
        ret = self.client.get(
            "/update/6/Firefox/54.0.1/20170628075643/WINNT_x86-msvc-x64/en-US/release100"
            "/Windows_NT 6.1.0.0 (x86)/ISET:SSE3,MEM:4096,JAWS:0/default/default/update.xml"
        )
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" displayVersion="100.0" appVersion="100.0" platformVersion="100.0" buildID="20170918210324"
            detailsURL="https://www.mozilla.org/en-US/firefox/100.0/releasenotes/">
        <patch type="complete" URL="http://download.mozilla.org/?product=firefox-100.0-complete&amp;os=win&amp;lang=en-US" hashFunction="sha512"
                hashValue="3530e6d88cb44c0360ec2aec4e171bdc4a45a6062d2fcbca25264882876dce3486a23a903a71fa612f93fcf9261067dbe22e2f4f8cc8e7dd3e55578095b43b4e"
                size="38171451"/>
        <patch type="partial" URL="http://download.mozilla.org/?product=firefox-100.0-partial-54.0.1&amp;os=win&amp;lang=en-US" hashFunction="sha512"
                hashValue="ce5820a550a7b9c9d0be29c629242def63ff333bc12b5d2d45d23c8e2b238adda9bd9f7ef14649616aae8b78e9545e8e7ec3fe93ac1b3d808027254087790af6"
                size="26673535"/>
    </update>
</updates>""",
        )


class ClientTestMig64(ClientTestCommon):
    """Tests the expected real world scenarios for the mig64 query parameter.
    mig64=0 is not tested because we have no client code that sends it. These
    cases are tested in the db layer tests, though."""

    @classmethod
    def setUpClass(cls):
        # Error handlers are removed in order to give us better debug messages
        cls.error_spec = app.error_handler_spec
        # Ripped from https://github.com/pallets/flask/blob/2.3.3/src/flask/scaffold.py#L131-L134
        app.error_handler_spec = defaultdict(lambda: defaultdict(dict))

    @classmethod
    def tearDownClass(cls):
        app.error_handler_spec = cls.error_spec

    def setUp(self):
        app.config["DEBUG"] = True
        app.config["SPECIAL_FORCE_HOSTS"] = ("http://a.com",)
        app.config["ALLOWLISTED_DOMAINS"] = {"a.com": ("a", "b", "c")}
        dbo.setDb("sqlite:///:memory:")
        self.metadata.create_all(dbo.engine)
        self.client = app.test_client()
        dbo.setDomainAllowlist({"a.com": ("a", "b", "c")})
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="a", update_type="minor", product="a", data_version=1)
        dbo.releases.t.insert().execute(
            name="a",
            product="a",
            data_version=1,
            data=createBlob(
                """
{
    "name": "a",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "2",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/z"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="b", update_type="minor", product="b", mig64=True, data_version=1)
        dbo.releases.t.insert().execute(
            name="b",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "b",
    "schema_version": 1,
    "appv": "2.0",
    "extv": "2.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "12",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "13",
                        "from": "*",
                        "hashValue": "14",
                        "fileUrl": "http://a.com/z1"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="c", update_type="minor", product="c", mig64=False, data_version=1)
        dbo.releases.t.insert().execute(
            name="c",
            product="c",
            data_version=1,
            data=createBlob(
                """
{
    "name": "c",
    "schema_version": 1,
    "appv": "3.0",
    "extv": "3.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "22",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "23",
                        "from": "*",
                        "hashValue": "24",
                        "fileUrl": "http://a.com/z2"
                    }
                }
            }
        }
    }
}
"""
            ),
        )

    def testRuleFalseQueryNull(self):
        ret = self.client.get("/update/3/c/1.0/2/p/l/a/a/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testRuleFalseQueryTrue(self):
        ret = self.client.get("/update/3/c/1.0/2/p/l/a/a/a/a/update.xml?mig64=1")
        self.assertUpdatesAreEmpty(ret)

    def testRuleTrueQueryNull(self):
        ret = self.client.get("/update/3/b/1.0/2/p/l/a/a/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testRuleTrueQueryTrue(self):
        ret = self.client.get("/update/3/b/1.0/2/p/l/a/a/a/a/update.xml?mig64=1")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="2.0" extensionVersion="2.0" buildID="12">
        <patch type="complete" URL="http://a.com/z1" hashFunction="sha512" hashValue="14" size="13"/>
    </update>
</updates>
""",
        )

    def testRuleNullQueryNull(self):
        ret = self.client.get("/update/3/a/1.0/1/p/l/a/a/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )

    def testRuleNullQueryTrue(self):
        ret = self.client.get("/update/3/a/1.0/1/p/l/a/a/a/a/update.xml?mig64=1")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )


class ClientTestJaws(ClientTestCommon):
    """Tests the expected real world scenarios for the JAWS parameter in
    SYSTEM_CAPABILITIES."""

    @classmethod
    def setUpClass(cls):
        # Error handlers are removed in order to give us better debug messages
        cls.error_spec = app.error_handler_spec
        # Ripped from https://github.com/pallets/flask/blob/2.3.3/src/flask/scaffold.py#L131-L134
        app.error_handler_spec = defaultdict(lambda: defaultdict(dict))

    @classmethod
    def tearDownClass(cls):
        app.error_handler_spec = cls.error_spec

    def setUp(self):
        app.config["DEBUG"] = True
        app.config["SPECIAL_FORCE_HOSTS"] = ("http://a.com",)
        app.config["ALLOWLISTED_DOMAINS"] = {"a.com": ("a", "b", "c")}
        dbo.setDb("sqlite:///:memory:")
        self.metadata.create_all(dbo.engine)
        self.client = app.test_client()
        dbo.setDomainAllowlist({"a.com": ("a", "b", "c")})
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="a", update_type="minor", product="a", data_version=1)
        dbo.releases.t.insert().execute(
            name="a",
            product="a",
            data_version=1,
            data=createBlob(
                """
{
    "name": "a",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "2",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/z"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="b", update_type="minor", product="b", jaws=True, data_version=1)
        dbo.releases.t.insert().execute(
            name="b",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "b",
    "schema_version": 1,
    "appv": "2.0",
    "extv": "2.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "12",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "13",
                        "from": "*",
                        "hashValue": "14",
                        "fileUrl": "http://a.com/z1"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping="c", update_type="minor", product="c", jaws=False, data_version=1)
        dbo.releases.t.insert().execute(
            name="c",
            product="c",
            data_version=1,
            data=createBlob(
                """
{
    "name": "c",
    "schema_version": 1,
    "appv": "3.0",
    "extv": "3.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "22",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "23",
                        "from": "*",
                        "hashValue": "24",
                        "fileUrl": "http://a.com/z2"
                    }
                }
            }
        }
    }
}
"""
            ),
        )

    def testRuleFalseQueryNull(self):
        ret = self.client.get("/update/6/c/1.0/2/p/l/a/a/a/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testRuleFalseQueryTrue(self):
        ret = self.client.get("/update/6/c/1.0/2/p/l/a/a/JAWS:1/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testRuleFalseQueryFalse(self):
        ret = self.client.get("/update/6/c/1.0/2/p/l/a/a/ISET:SSE3,MEM:8096,JAWS:0/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="3.0" extensionVersion="3.0" buildID="22">
        <patch type="complete" URL="http://a.com/z2" hashFunction="sha512" hashValue="24" size="23"/>
    </update>
</updates>
""",
        )

    def testRuleTrueQueryNull(self):
        ret = self.client.get("/update/6/b/1.0/2/p/l/a/a/a/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testRuleTrueQueryTrue(self):
        ret = self.client.get("/update/6/b/1.0/2/p/l/a/a/ISET:SSE3,MEM:8096,JAWS:1/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="2.0" extensionVersion="2.0" buildID="12">
        <patch type="complete" URL="http://a.com/z1" hashFunction="sha512" hashValue="14" size="13"/>
    </update>
</updates>
""",
        )

    def testRuleTrueQueryFalse(self):
        ret = self.client.get("/update/6/b/1.0/2/p/l/a/a/ISET:SSE3,MEM:8096,JAWS:0/a/a/update.xml")
        self.assertUpdatesAreEmpty(ret)

    def testRuleNullQueryNull(self):
        ret = self.client.get("/update/6/a/1.0/1/p/l/a/a/a/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )

    def testRuleNullQueryTrue(self):
        ret = self.client.get("/update/6/a/1.0/1/p/l/a/a/ISET:SSE3,MEM:8096,JAWS:1/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )

    def testRuleNullQueryFalse(self):
        ret = self.client.get("/update/6/a/1.0/1/p/l/a/a/ISET:SSE3,MEM:8096,JAWS:0/a/a/update.xml")
        self.assertUpdateEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
""",
        )


class ClientTestEmergencyShutoff(ClientTestBase):
    def setUp(self):
        super(ClientTestEmergencyShutoff, self).setUp()
        self.update_xml = """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="2">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>
"""
        cache.reset()

    def testShutoffUpdates(self):
        update_query = "/update/3/b/1.0/1/p/l/a/a/a/a/update.xml"
        ret = self.client.get(update_query)
        self.assertUpdateEqual(ret, self.update_xml)

        dbo.emergencyShutoffs.t.insert().execute(product="b", channel="a", data_version=1)

        ret = self.client.get(update_query)
        self.assertUpdatesAreEmpty(ret)

    def testShutoffUpdatesCache(self):
        # Create the updates_disabled cache for this test
        cache.make_cache("updates_disabled", 10, 100)
        update_query = "/update/3/b/1.0/1/p/l/a/a/a/a/update.xml"
        ret = self.client.get(update_query)
        self.assertUpdateEqual(ret, self.update_xml)

        dbo.emergencyShutoffs.t.insert().execute(product="b", channel="a", data_version=1)

        # We should actually get the same update here since the disabled
        # updates check has been cached
        ret = self.client.get(update_query)
        self.assertUpdateEqual(ret, self.update_xml)

    def testShutoffUpdatesFallbackChannel(self):
        update_query = "/update/3/b/1.0/1/p/l/a-cck-foo/a/a/a/update.xml"
        ret = self.client.get(update_query)
        self.assertUpdateEqual(ret, self.update_xml)

        dbo.emergencyShutoffs.t.insert().execute(product="b", channel="a", data_version=1)

        ret = self.client.get(update_query)
        self.assertUpdatesAreEmpty(ret)


class ClientTestWithErrorHandlers(ClientTestCommon):
    """Most of the tests are run without the error handler because it gives more
    useful output when things break. However, we still need to test that our
    error handlers works!"""

    def setUp(self):
        app.config["DEBUG"] = True
        app.config["ALLOWLISTED_DOMAINS"] = {"a.com": ("a",)}
        dbo.setDb("sqlite:///:memory:")
        self.metadata.create_all(dbo.engine)
        self.client = app.test_client()

    def testCacheControlIsSet(self):
        ret = self.client.get("/update/3/c/15.0/1/p/l/a/a/default/a/update.xml")
        self.assertEqual(ret.headers.get("Cache-Control"), "public, max-age=90")

    def testCacheControlIsNotSetFor404(self):
        ret = self.client.get("/whizzybang")
        self.assertEqual(ret.headers.get("Cache-Control"), None)

    def testContentSecurityPolicyIsSet(self):
        ret = self.client.get("/update/3/c/15.0/1/p/l/a/a/default/a/update.xml")
        self.assertEqual(ret.headers.get("Content-Security-Policy"), "default-src 'none'; frame-ancestors 'none'")

    def testContentSecurityPolicyIsSetFor404(self):
        ret = self.client.get("/whizzybang")
        self.assertEqual(ret.headers.get("Content-Security-Policy"), "default-src 'none'; frame-ancestors 'none'")

    def testContentSecurityPolicyIsSetFor400(self):
        with mock.patch("auslib.web.public.client.get_update_blob") as m:
            m.side_effect = BadDataError("I break!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.headers.get("Content-Security-Policy"), "default-src 'none'; frame-ancestors 'none'")

    def testContentSecurityPolicyIsSetFor500(self):
        with mock.patch("auslib.web.public.client.get_update_blob") as m:
            m.side_effect = Exception("I break!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.headers.get("Content-Security-Policy"), "default-src 'none'; frame-ancestors 'none'")

    def testStrictTransportSecurityIsSet(self):
        ret = self.client.get("/update/3/c/15.0/1/p/l/a/a/default/a/update.xml")
        self.assertEqual(ret.headers.get("Strict-Transport-Security"), "max-age=31536000;")

    def testStrictTransportSecurityIsSetFor404(self):
        ret = self.client.get("/whizzybang")
        self.assertEqual(ret.headers.get("Strict-Transport-Security"), "max-age=31536000;")

    def testStrictTransportSecurityIsSetFor400(self):
        with mock.patch("auslib.web.public.client.get_update_blob") as m:
            m.side_effect = BadDataError("I break!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.headers.get("Strict-Transport-Security"), "max-age=31536000;")

    def testStrictTransportSecurityIsSetFor500(self):
        with mock.patch("auslib.web.public.client.get_update_blob") as m:
            m.side_effect = Exception("I break!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.headers.get("Strict-Transport-Security"), "max-age=31536000;")

    def testXContentTypeOptionsIsSet(self):
        ret = self.client.get("/update/3/c/15.0/1/p/l/a/a/default/a/update.xml")
        self.assertEqual(ret.headers.get("X-Content-Type-Options"), "nosniff")

    def testXContentTypeOptionsIsSetFor404(self):
        ret = self.client.get("/whizzybang")
        self.assertEqual(ret.headers.get("X-Content-Type-Options"), "nosniff")

    def testXContentTypeOptionsIsSetFor400(self):
        with mock.patch("auslib.web.public.client.get_update_blob") as m:
            m.side_effect = BadDataError("I break!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.headers.get("X-Content-Type-Options"), "nosniff")

    def testXContentTypeOptionsIsSetFor500(self):
        with mock.patch("auslib.web.public.client.get_update_blob") as m:
            m.side_effect = Exception("I break!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.headers.get("X-Content-Type-Options"), "nosniff")

    def testEmptySnippetOn404(self):
        ret = self.client.get("/update/whizzybang")
        self.assertUpdatesAreEmpty(ret)

    @given(just("/whizzybang"))
    @example(path="/")
    @example(path="/api/v1")
    @example(path="/api/v1/releases/")
    @example(path="/api/v1/rules/")
    def test404ResponseForNonUpdateEndpoint(self, path):
        ret = self.client.get(path)
        self.assertEqual(ret.status_code, 404)

    def testErrorMessageOn500(self):
        with mock.patch("auslib.web.public.client.getQueryFromURL") as m:
            m.side_effect = Exception("I break!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.status_code, 500)
            self.assertEqual(ret.mimetype, "text/plain")
            self.assertEqual("I break!", ret.get_data(as_text=True))

    def testErrorMessageOn500withSimpleArgs(self):
        with mock.patch("auslib.web.public.client.getQueryFromURL") as m:
            m.side_effect = Exception("I break!")
            m.side_effect.args = ("one", "two", "three")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.status_code, 500)
            self.assertEqual(ret.mimetype, "text/plain")
            data = ret.get_data(as_text=True)
            for arg in ("one", "two", "three"):
                self.assertIn(arg, data)

    def testErrorMessageOn500withComplexArgs(self):
        with mock.patch("auslib.web.public.client.getQueryFromURL") as m:
            m.side_effect = Exception("I break!")
            m.side_effect.args = ("one", ("two", "three"))
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.status_code, 500)
            self.assertEqual(ret.mimetype, "text/plain")
            data = ret.get_data(as_text=True)
            for arg in ("one", "two", "three"):
                self.assertIn(arg, data)

    def testEscapedOutputOn500(self):
        with mock.patch("auslib.web.public.client.getQueryFromURL") as m:
            m.side_effect = Exception("50.1.0zibj5<img src%3da onerror%3dalert(document.domain)>")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.status_code, 500)
            self.assertEqual(ret.mimetype, "text/plain")
            self.assertEqual("50.1.0zibj5&lt;img src%3da onerror%3dalert(document.domain)&gt;", ret.get_data(as_text=True))

    def testEscapedOutputOn400(self):
        with mock.patch("auslib.web.public.client.getQueryFromURL") as m:
            m.side_effect = BadDataError("Version number 50.1.0zibj5<img src%3da onerror%3dalert(document.domain)> is invalid.")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            error_message = ret.get_data(as_text=True)
            self.assertEqual(ret.status_code, 400, error_message)
            self.assertEqual(ret.mimetype, "text/plain")
            self.assertEqual("Version number 50.1.0zibj5&lt;img src%3da onerror%3dalert(document.domain)&gt; is invalid.", error_message)

    def testSentryBadDataError(self):
        with mock.patch("auslib.web.public.client.getQueryFromURL") as m, mock.patch("auslib.web.public.base.capture_exception") as sentry:
            m.side_effect = BadDataError("exterminate!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertFalse(sentry.called)
            self.assertEqual(ret.status_code, 400, ret.get_data())
            self.assertEqual(ret.mimetype, "text/plain")

    def testSentryRealError(self):
        with mock.patch("auslib.web.public.client.getQueryFromURL") as m, mock.patch("auslib.web.public.base.capture_exception") as sentry:
            m.side_effect = Exception("exterminate!")
            ret = self.client.get("/update/4/b/1.0/1/p/l/a/a/a/a/1/update.xml")
            self.assertEqual(ret.status_code, 500)
            self.assertEqual(ret.mimetype, "text/plain")
            self.assertTrue(sentry.called)
            self.assertEqual("exterminate!", ret.get_data(as_text=True))

    def testNonSubstitutedUrlVariablesReturnEmptyUpdate(self):
        request1 = "/update/1/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/update.xml"
        request2 = "/update/2/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/update.xml"
        request3 = "/update/3/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/" "update.xml"
        request4 = (
            "/update/4/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/"
            "%MOZ_VERSION%/update.xml"
        )
        request5 = (
            "/update/5/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/" "%IMEI%/update.xml"
        )
        request6 = (
            "/update/6/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%SYSTEM_CAPABILITIES%/%DISTRIBUTION%/"
            "%DISTRIBUTION_VERSION%/update.xml"
        )

        with mock.patch("auslib.web.public.client") as mock_cr_view:
            for request in [request1, request2, request3, request4, request5, request6]:
                ret = self.client.get(request)
                self.assertUpdatesAreEmpty(ret)
                self.assertFalse(mock_cr_view.called)

    # "Accepted" is a bit weird here - it basically just means "doesn't cause an ISE 500"
    # We don't have any valid query fields with unicode in their name, so a 400 is the
    # best thing we can test for.
    def testUnicodeAcceptedInQueryFieldName(self):
        ret = self.client.get("/update/6/3/e/2.0.0/1/p/l/a/a/a/a/update.xml?fooÃÃÃÃÃÃbar=1")
        self.assertEqual(ret.status_code, 400)


class ClientTestCompactXML(ClientTestCommon):
    """Tests the compact XML needed to rescue two Firefox nightlies (bug 1517743)."""

    @classmethod
    def setUpClass(cls):
        # Error handlers are removed in order to give us better debug messages
        cls.error_spec = app.error_handler_spec
        # Ripped from https://github.com/pallets/flask/blob/2.3.3/src/flask/scaffold.py#L131-L134
        app.error_handler_spec = defaultdict(lambda: defaultdict(dict))

    @classmethod
    def tearDownClass(cls):
        app.error_handler_spec = cls.error_spec

    def setUp(self):
        self.version_fd, self.version_file = mkstemp()
        app.config["DEBUG"] = True
        app.config["SPECIAL_FORCE_HOSTS"] = ("http://a.com",)
        app.config["ALLOWLISTED_DOMAINS"] = {"a.com": ("b",)}
        dbo.setDb("sqlite:///:memory:")
        self.metadata.create_all(dbo.engine)
        dbo.setDomainAllowlist({"a.com": ("b",)})
        self.client = app.test_client()
        dbo.rules.t.insert().execute(
            priority=90, backgroundRate=100, mapping="Firefox-mozilla-central-nightly-latest", update_type="minor", product="b", data_version=1
        )
        dbo.releases.t.insert().execute(
            name="Firefox-mozilla-central-nightly-latest",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Firefox-mozilla-central-nightly-latest",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "30000101000000",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/z"
                    }
                }
            }
        }
    }
}
"""
            ),
        )

    def testGoodNightly(self):
        ret = self.client.get("/update/6/b/1.0/20181212121212/p/l/a/a/a/a/a/update.xml")
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="1.0" extensionVersion="1.0" buildID="30000101000000">
        <patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>""",
        )

    def testBrokenNightly(self):
        ret = self.client.get("/update/6/b/1.0/20190103220533/p/l/a/a/a/a/a/update.xml")
        self.assertUpdateTextEqual(
            ret,
            '<?xml version="1.0"?><updates><update type="minor" version="1.0" extensionVersion="1.0" buildID="30000101000000">'
            '<patch type="complete" URL="http://a.com/z" hashFunction="sha512" hashValue="4" size="3"/></update></updates>',
        )


class ClientTestPinning(ClientTestCommon):
    """Tests that setting update pins work as expected - by holding an install back to the specified
    version."""

    def setUp(self):
        self.version_fd, self.version_file = mkstemp()
        app.config["DEBUG"] = True
        app.config["SPECIAL_FORCE_HOSTS"] = ("http://a.com",)
        app.config["ALLOWLISTED_DOMAINS"] = {"a.com": ("b",)}
        dbo.setDb("sqlite:///:memory:")
        self.metadata.create_all(dbo.engine)
        dbo.setDomainAllowlist({"a.com": ("b",)})
        self.client = app.test_client()
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="1.", mapping="Firefox-mozilla-central-nightly-1")
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="1.0.", mapping="Firefox-mozilla-central-nightly-1")
        dbo.releases.t.insert().execute(
            name="Firefox-mozilla-central-nightly-1",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Firefox-mozilla-central-nightly-1",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "30000101000010",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/1"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="2.0.", mapping="Firefox-mozilla-central-nightly-2")
        dbo.releases.t.insert().execute(
            name="Firefox-mozilla-central-nightly-2",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Firefox-mozilla-central-nightly-2",
    "schema_version": 1,
    "appv": "2.0",
    "extv": "2.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "30000101000020",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/2"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="2.1.", mapping="Firefox-mozilla-central-nightly-2-1")
        dbo.releases.t.insert().execute(
            name="Firefox-mozilla-central-nightly-2-1",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Firefox-mozilla-central-nightly-2-1",
    "schema_version": 1,
    "appv": "2.1",
    "extv": "2.1",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "30000101000021",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/2_1"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="2.2.", mapping="Firefox-mozilla-central-nightly-2-2")
        dbo.releases.t.insert().execute(
            name="Firefox-mozilla-central-nightly-2-2",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Firefox-mozilla-central-nightly-2-2",
    "schema_version": 1,
    "appv": "2.2",
    "extv": "2.2",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "30000101000022",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/2_2"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="2.", mapping="Firefox-mozilla-central-nightly-2-3")
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="2.3.", mapping="Firefox-mozilla-central-nightly-2-3")
        dbo.releases.t.insert().execute(
            name="Firefox-mozilla-central-nightly-2-3",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Firefox-mozilla-central-nightly-2-3",
    "schema_version": 1,
    "appv": "2.3",
    "extv": "2.3",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "30000101000023",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/2_3"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(
            priority=200, backgroundRate=100, mapping="Firefox-mozilla-central-nightly-3", update_type="minor", product="b", data_version=1, version="<3.0"
        )
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="3.", mapping="Firefox-mozilla-central-nightly-3")
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="3.0.", mapping="Firefox-mozilla-central-nightly-3")
        dbo.releases.t.insert().execute(
            name="Firefox-mozilla-central-nightly-3",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Firefox-mozilla-central-nightly-3",
    "schema_version": 1,
    "appv": "3.0",
    "extv": "3.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "30000101000030",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/3"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="4.", mapping="Firefox-mozilla-central-nightly-4")
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="4.0.", mapping="Firefox-mozilla-central-nightly-4")
        dbo.releases.t.insert().execute(
            name="Firefox-mozilla-central-nightly-4",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Firefox-mozilla-central-nightly-4",
    "schema_version": 1,
    "appv": "4.0",
    "extv": "4.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "30000101000040",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/4"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.rules.t.insert().execute(
            priority=90, backgroundRate=100, mapping="Firefox-mozilla-central-nightly-5", update_type="minor", product="b", data_version=1
        )
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="5.", mapping="Firefox-mozilla-central-nightly-5")
        dbo.pinnable_releases.t.insert().execute(data_version=1, product="b", channel="c", version="5.0.", mapping="Firefox-mozilla-central-nightly-5")
        dbo.releases.t.insert().execute(
            name="Firefox-mozilla-central-nightly-5",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Firefox-mozilla-central-nightly-5",
    "schema_version": 1,
    "appv": "5.0",
    "extv": "5.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "30000101000050",
            "locales": {
                "l": {
                    "complete": {
                        "filesize": "3",
                        "from": "*",
                        "hashValue": "4",
                        "fileUrl": "http://a.com/5"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.releases.t.insert().execute(
            name="desupport",
            product="b",
            data_version=1,
            data=createBlob(
                """
{
    "name": "desupport",
    "schema_version": 50,
    "detailsUrl": "http://example.com/desupport",
    "displayVersion": "1"
}
"""
            ),
        )
        dbo.rules.t.insert().execute(
            priority=100, backgroundRate=100, mapping="desupport", update_type="minor", product="b", data_version=1, osVersion="obsolete"
        )

    def testUnpinnedRecent(self):
        ret = self.client.get("/update/6/b/3.0/30000101000030/p/l/c/a/a/a/a/update.xml")
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="5.0" extensionVersion="5.0" buildID="30000101000050">
        <patch type="complete" URL="http://a.com/5" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>""",
        )

    def testUnpinnedWatershed(self):
        ret = self.client.get("/update/6/b/1.0/30000101000010/p/l/c/a/a/a/a/update.xml")
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="3.0" extensionVersion="3.0" buildID="30000101000030">
        <patch type="complete" URL="http://a.com/3" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>""",
        )

    def testMajorPinSameVersion(self):
        ret = self.client.get("/update/6/b/1.0/30000101000010/p/l/c/a/a/a/a/update.xml?pin=1.")
        self.assertUpdatesAreEmpty(ret)

    def testMinorPinSameVersion(self):
        ret = self.client.get("/update/6/b/1.0/30000101000010/p/l/c/a/a/a/a/update.xml?pin=1.0.")
        self.assertUpdatesAreEmpty(ret)

    def testMajorPinWatershed(self):
        ret = self.client.get("/update/6/b/1.0/30000101000010/p/l/c/a/a/a/a/update.xml?pin=5.")
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="3.0" extensionVersion="3.0" buildID="30000101000030">
        <patch type="complete" URL="http://a.com/3" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>""",
        )

    def testMinorPinWatershed(self):
        ret = self.client.get("/update/6/b/1.0/30000101000010/p/l/c/a/a/a/a/update.xml?pin=5.0.")
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="3.0" extensionVersion="3.0" buildID="30000101000030">
        <patch type="complete" URL="http://a.com/3" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>""",
        )

    def testMajorPin(self):
        ret = self.client.get("/update/6/b/1.0/30000101000010/p/l/c/a/a/a/a/update.xml?pin=2.")
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="2.3" extensionVersion="2.3" buildID="30000101000023">
        <patch type="complete" URL="http://a.com/2_3" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>""",
        )

    def testMinorPinThroughMajorVersion(self):
        ret = self.client.get("/update/6/b/1.0/30000101000010/p/l/c/a/a/a/a/update.xml?pin=2.2.")
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="2.2" extensionVersion="2.2" buildID="30000101000022">
        <patch type="complete" URL="http://a.com/2_2" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>""",
        )

    def testMinorPin(self):
        ret = self.client.get("/update/6/b/2.0/30000101000020/p/l/c/a/a/a/a/update.xml?pin=2.2.")
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="2.2" extensionVersion="2.2" buildID="30000101000022">
        <patch type="complete" URL="http://a.com/2_2" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>""",
        )

    def testMajorPinFromWatershed(self):
        ret = self.client.get("/update/6/b/3.0/30000101000030/p/l/c/a/a/a/a/update.xml?pin=4.")
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="4.0" extensionVersion="4.0" buildID="30000101000040">
        <patch type="complete" URL="http://a.com/4" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>""",
        )

    def testMinorPinFromWatershed(self):
        ret = self.client.get("/update/6/b/3.0/30000101000030/p/l/c/a/a/a/a/update.xml?pin=4.0.")
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>
    <update type="minor" version="4.0" extensionVersion="4.0" buildID="30000101000040">
        <patch type="complete" URL="http://a.com/4" hashFunction="sha512" hashValue="4" size="3"/>
    </update>
</updates>""",
        )

    def testMajorPinUpdateBackwards(self):
        ret = self.client.get("/update/6/b/2.0/30000101000020/p/l/c/a/a/a/a/update.xml?pin=1.")
        self.assertUpdatesAreEmpty(ret)

    def testMinorPinUpdateBackwards(self):
        ret = self.client.get("/update/6/b/2.2/30000101000022/p/l/c/a/a/a/a/update.xml?pin=2.1.")
        self.assertUpdatesAreEmpty(ret)

    def testBrokenPin(self):
        ret = self.client.get("/update/6/b/2.2/30000101000022/p/l/c/a/a/a/a/update.xml?pin=2")
        self.assertEqual(ret.status_code, 400)
        error_message = ret.get_data(as_text=True)
        self.assertEqual(error_message, "Version Pin String '2' is invalid.")

    def testPinWithDesupport(self):
        ret = self.client.get("/update/6/b/3.0/30000101000020/p/l/c/obsolete/a/a/a/update.xml?pin=4.")
        self.assertEqual(ret.status_code, 200)
        self.assertUpdateTextEqual(
            ret,
            """<?xml version="1.0"?>
<updates>

    <update type="minor" unsupported="true" detailsURL="http://example.com/desupport" displayVersion="1">
</update>
</updates>""",
        )
