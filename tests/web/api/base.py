import logging
import unittest

import pytest

from auslib.blobs.base import createBlob
from auslib.global_state import dbo
from auslib.web.public.base import conenxion_app as app


def setUpModule():
    # Silence SQLAlchemy-Migrate's debugging logger
    logging.getLogger("migrate").setLevel(logging.CRITICAL)


@pytest.mark.usefixtures("current_db_schema")
class CommonTestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Error handlers are removed in order to give us better debug messages
        cls.error_spec = app.error_handler_spec
        # Ripped from https://github.com/mitsuhiko/flask/blob/1f5927eee2288b4aaf508af5dc1f148aa2140d91/flask/app.py#L394
        app.error_handler_spec = {None: {}}

    @classmethod
    def tearDownClass(cls):
        app.error_handler_spec = cls.error_spec

    @pytest.fixture(autouse=True)
    def setup(self, insert_release, firefox_54_0_1_build1, firefox_56_0_build1, superblob_e8f4a19, hotfix_bug_1548973_1_1_4, timecop_1_0):
        app.config["DEBUG"] = True
        self.public_client = app.test_client()

        dbo.setDb("sqlite:///:memory:")
        self.metadata.create_all(dbo.engine)
        dbo.rules.t.insert().execute(
            rule_id=1, priority=90, backgroundRate=100, mapping="Fennec.55.0a1", update_type="minor", product="Fennec", data_version=1, alias="moz-releng"
        )
        dbo.releases.t.insert().execute(
            name="Fennec.55.0a1",
            product="Fennec",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Fennec.55.0a1",
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
        dbo.rules.t.insert().execute(
            rule_id=2, priority=90, backgroundRate=100, mapping="Firefox.55.0a1", update_type="minor", product="Firefox", instructionSet="SSE", data_version=1
        )
        dbo.releases.t.insert().execute(
            name="Firefox.55.0a1",
            product="Firefox",
            data_version=1,
            data=createBlob(
                """
{
    "name": "Firefox.55.0a1",
    "schema_version": 1,
    "appv": "1.0",
    "extv": "1.0",
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "buildID": "5",
            "locales": {
                "l": {
                    "buildID": "5",
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
        dbo.rules.t.insert().execute(rule_id=3, priority=90, backgroundRate=0, mapping="q", update_type="minor", product="q", data_version=3)
        dbo.rules.history.t.insert().execute(
            change_id=1, changed_by="usr", timestamp=10, rule_id=3, priority=90, backgroundRate=0, mapping="y", update_type="minor", product="y", data_version=2
        )
        dbo.rules.history.t.insert().execute(
            change_id=2, changed_by="usr", timestamp=10, rule_id=3, priority=90, backgroundRate=0, mapping="z", update_type="minor", product="z", data_version=1
        )
        dbo.releases.t.insert().execute(
            name="q",
            product="q",
            data_version=2,
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
            "buildID": "6",
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

        dbo.rules.t.insert().execute(
            rule_id=4, priority=90, backgroundRate=100, mapping="Firefox.55.0a1", update_type="minor", product="Firefox", mig64=True, data_version=1
        )
        insert_release(firefox_54_0_1_build1, "Firefox", history=False)
        insert_release(firefox_56_0_build1, "Firefox", history=False)
        insert_release(superblob_e8f4a19, "SystemAddons", history=False)
        insert_release(hotfix_bug_1548973_1_1_4, "SystemAddons", history=False)
        insert_release(timecop_1_0, "SystemAddons", history=False)
