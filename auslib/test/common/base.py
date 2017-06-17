import unittest
import logging

from auslib.blobs.base import createBlob
from auslib.global_state import dbo
from auslib.web.public.base import app


def setUpModule():
    # Silence SQLAlchemy-Migrate's debugging logger
    logging.getLogger('migrate').setLevel(logging.CRITICAL)


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

    def setUp(self):
        app.config['DEBUG'] = True
        self.public_client = app.test_client()

        dbo.setDb('sqlite:///:memory:')
        dbo.create()
        dbo.setDomainWhitelist({'a.com': ('q')})
        dbo.permissions.t.insert().execute(permission='admin', username='bill', data_version=1)
        dbo.rules.t.insert().execute(rule_id=1, priority=90, backgroundRate=100, mapping='b', update_type='minor', product='Fennec',
                                     data_version=1, alias="moz-releng")
        dbo.releases.t.insert().execute(name='Fennec.55.0a1', product='Fennec', data_version=1, data=createBlob("""
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
"""))
        dbo.rules.t.insert().execute(priority=90, backgroundRate=100, mapping='s', update_type='minor', product='Firefox',
                                     systemCapabilities="SSE", data_version=1)
        dbo.releases.t.insert().execute(name='Firefox.55.0a1', product='Firefox', data_version=1, data=createBlob("""
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
"""))
        dbo.rules.t.insert().execute(priority=90, backgroundRate=0, mapping='q', update_type='minor', product='q',
                                     data_version=1)
        dbo.releases.t.insert().execute(name='q', product='q', data_version=1, data=createBlob("""
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
"""))
