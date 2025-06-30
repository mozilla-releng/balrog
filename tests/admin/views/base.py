import logging
import os
import unittest
from tempfile import mkstemp

import pytest

from auslib.blobs.base import createBlob
from auslib.global_state import cache, dbo
from auslib.util.auth import AuthError

from ...fakes import FakeBlob, FakeGCSHistory


def setUpModule():
    # Silence SQLAlchemy-Migrate's debugging logger
    logging.getLogger("migrate").setLevel(logging.CRITICAL)


@pytest.mark.usefixtures("current_db_schema")
class ViewTest(unittest.TestCase):
    """Base class for all view tests. Sets up some sample data, and provides
    some helper methods."""

    @pytest.fixture(autouse=True)
    def setup(self, insert_release, firefox_56_0_build1, app):
        from auslib.web.admin.views import base as view_base

        self.view_base = view_base

        # Mock out verified_userinfo, because we don't want to talk to Auth0
        # or need to provide real credentials in tests.
        # We don't do this with "mock" because this is a base to all of other
        # tests, and "mock" must be applied in the tests itself.
        self.orig_base_verified_userinfo = view_base.verified_userinfo
        self.mocked_user = None

        def my_userinfo(*args, **kwargs):
            if not self.mocked_user:
                raise AuthError("auth required", 401)
            return {"email": self.mocked_user}

        view_base.verified_userinfo = my_userinfo

        self.version_fd, self.version_file = mkstemp()
        cache.reset()
        cache.make_copies = True
        app.app.config["SECRET_KEY"] = "abc123"
        app.app.config["DEBUG"] = True
        app.app.config["ALLOWLISTED_DOMAINS"] = {"good.com": ("a", "b", "c", "d")}
        app.app.config["VERSION_FILE"] = self.version_file
        app.app.config["AUTH_DOMAIN"] = "balrog.test.dev"
        app.app.config["AUTH_AUDIENCE"] = "balrog test"
        app.app.config["M2M_ACCOUNT_MAPPING"] = {}
        app.app.config["CORS_ORIGINS"] = "*"
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
        dbo.setDb("sqlite:///:memory:", releases_history_buckets={"*": "fake"}, releases_history_class=FakeGCSHistory)

        self.orig_releases_history = dbo.releases.history
        # TODO: need a better mock, or maybe a Fake that stores history in memory?
        # only the merge tests benefit from having history
        # the rest are fine if we just let history be None
        # maybe we should mock this only in the tests we care about?
        dbo.releases.history = FakeGCSHistory()

        dbo.setDomainAllowlist({"good.com": ("a", "b", "c", "d")})
        self.metadata.create_all(dbo.engine)
        dbo.permissions.t.insert().execute(permission="admin", username="bill", data_version=1)
        dbo.permissions.t.insert().execute(permission="permission", username="bob", data_version=1)
        dbo.permissions.t.insert().execute(
            permission="release", username="bob", options=dict(products=["fake", "a", "b"], actions=["create", "modify"]), data_version=1
        )
        dbo.permissions.t.insert().execute(permission="release", username="julie", options=dict(products=["a"], actions=["modify"]), data_version=1)
        dbo.permissions.t.insert().execute(permission="rule", username="julie", options=dict(products=["fake"], actions=["create"]), data_version=1)
        dbo.permissions.t.insert().execute(permission="release_read_only", username="bob", options=dict(actions=["set"], products=["a", "b"]), data_version=1)
        dbo.permissions.t.insert().execute(permission="rule", username="bob", options=dict(actions=["modify"], products=["a", "b"]), data_version=1)
        dbo.permissions.t.insert().execute(permission="release", username="ashanti", options=dict(actions=["modify"], products=["a"]), data_version=1)
        dbo.permissions.t.insert().execute(permission="scheduled_change", username="mary", options=dict(actions=["enact"]), data_version=1)
        dbo.permissions.t.insert().execute(permission="release_locale", username="ashanti", options=dict(actions=["modify"], products=["a"]), data_version=1)
        dbo.permissions.t.insert().execute(permission="admin", username="billy", options=dict(products=["a"]), data_version=1)
        dbo.permissions.user_roles.t.insert().execute(username="bill", role="releng", data_version=1)
        dbo.permissions.user_roles.t.insert().execute(username="bill", role="qa", data_version=1)
        dbo.permissions.user_roles.t.insert().execute(username="bob", role="relman", data_version=1)
        dbo.permissions.user_roles.t.insert().execute(username="julie", role="releng", data_version=1)
        dbo.permissions.user_roles.t.insert().execute(username="mary", role="relman", data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="fake", channel="a", role="releng", signoffs_required=1, data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="fake", channel="e", role="releng", signoffs_required=1, data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="fake", channel="j", role="releng", signoffs_required=1, data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(product="fake", channel="k", role="relman", signoffs_required=1, data_version=2)
        dbo.productRequiredSignoffs.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=10, product="fake", channel="k", role="relman")
        dbo.productRequiredSignoffs.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=11, product="fake", channel="k", role="relman", signoffs_required=2, data_version=1
        )
        dbo.productRequiredSignoffs.history.t.insert().execute(
            change_id=3, changed_by="bill", timestamp=25, product="fake", channel="k", role="relman", signoffs_required=1, data_version=2
        )
        dbo.permissionsRequiredSignoffs.t.insert().execute(product="fake", role="releng", signoffs_required=1, data_version=1)
        dbo.permissionsRequiredSignoffs.t.insert().execute(product="bar", role="releng", signoffs_required=1, data_version=1)
        dbo.permissionsRequiredSignoffs.t.insert().execute(product="blah", role="releng", signoffs_required=1, data_version=1)
        dbo.permissionsRequiredSignoffs.t.insert().execute(product="doop", role="releng", signoffs_required=1, data_version=2)
        dbo.permissionsRequiredSignoffs.t.insert().execute(product="superfake", role="relman", signoffs_required=1, data_version=1)
        dbo.permissionsRequiredSignoffs.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=10, product="doop", role="releng")
        dbo.permissionsRequiredSignoffs.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=11, product="doop", role="releng", signoffs_required=2, data_version=1
        )
        dbo.permissionsRequiredSignoffs.history.t.insert().execute(
            change_id=3, changed_by="bill", timestamp=25, product="doop", role="releng", signoffs_required=1, data_version=2
        )
        dbo.releases.t.insert().execute(name="a", product="a", data=createBlob(dict(name="a", hashFunction="sha512", schema_version=1)), data_version=1)
        dbo.releases.t.insert().execute(name="ab", product="a", data=createBlob(dict(name="ab", hashFunction="sha512", schema_version=1)), data_version=1)
        dbo.releases.history.bucket.blobs["ab/None-456-bob.json"] = FakeBlob("")
        dbo.releases.history.bucket.blobs["ab/1-456-bob.json"] = FakeBlob(
            """
{
    "name": "ab",
    "hashFunction": "sha512",
    "schema_version": 1
}
"""
        )
        dbo.releases.t.insert().execute(name="b", product="b", data=createBlob(dict(name="b", hashFunction="sha512", schema_version=1)), data_version=1)
        dbo.releases.history.bucket.blobs["b/None-567-bob.json"] = FakeBlob("")
        dbo.releases.history.bucket.blobs["b/1-567-bob.json"] = FakeBlob(
            """
{
    "name": "b",
    "hashFunction": "sha512",
    "schema_version": 1
}
"""
        )
        dbo.releases.t.insert().execute(name="c", product="c", data=createBlob(dict(name="c", hashFunction="sha512", schema_version=1)), data_version=1)
        dbo.releases.t.insert().execute(
            name="d",
            product="d",
            data_version=1,
            data=createBlob(
                """
{
    "name": "d",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "d": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
"""
            ),
        )
        dbo.releases.history.bucket.blobs["d/None-678-bob.json"] = FakeBlob("")
        dbo.releases.history.bucket.blobs["d/1-678-bob.json"] = FakeBlob(
            """
{
    "name": "d",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "d": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
"""
        )
        dbo.rules.t.insert().execute(
            rule_id=1,
            priority=100,
            version="3.5",
            buildTarget="d",
            backgroundRate=100,
            mapping="c",
            update_type="minor",
            product="a",
            channel="a",
            data_version=2,
        )
        dbo.rules.history.t.insert().execute(change_id=1, timestamp=50, changed_by="bill", rule_id=1)
        dbo.rules.history.t.insert().execute(
            change_id=2,
            timestamp=51,
            changed_by="bill",
            rule_id=1,
            priority=100,
            version="3.5",
            buildTarget="d",
            backgroundRate=50,
            mapping="c",
            update_type="minor",
            product="a",
            channel="a",
            data_version=1,
        )
        dbo.rules.history.t.insert().execute(
            change_id=3,
            timestamp=65,
            changed_by="bill",
            rule_id=1,
            priority=100,
            version="3.5",
            buildTarget="d",
            backgroundRate=100,
            mapping="c",
            update_type="minor",
            product="a",
            channel="a",
            data_version=2,
        )
        dbo.rules.t.insert().execute(
            rule_id=2,
            alias="frodo",
            priority=100,
            version="3.3",
            buildTarget="d",
            backgroundRate=100,
            mapping="b",
            update_type="minor",
            product="a",
            channel="a",
            data_version=1,
        )
        dbo.rules.history.t.insert().execute(change_id=4, timestamp=60, changed_by="bill", rule_id=2)
        dbo.rules.history.t.insert().execute(
            change_id=5,
            timestamp=61,
            changed_by="bill",
            rule_id=2,
            alias="frodo",
            priority=100,
            version="3.3",
            buildTarget="d",
            backgroundRate=100,
            mapping="b",
            update_type="minor",
            product="a",
            channel="a",
            data_version=1,
        )
        dbo.rules.t.insert().execute(
            rule_id=3,
            product="a",
            priority=100,
            version="3.5",
            buildTarget="a",
            backgroundRate=100,
            mapping="a",
            update_type="minor",
            channel="a",
            data_version=2,
        )
        dbo.rules.history.t.insert().execute(change_id=6, timestamp=72, changed_by="bill", rule_id=3)
        dbo.rules.history.t.insert().execute(
            change_id=7,
            timestamp=73,
            changed_by="bill",
            rule_id=3,
            product="a",
            priority=50,
            version="3.5",
            buildTarget="a",
            backgroundRate=100,
            mapping="a",
            update_type="minor",
            channel="a",
            data_version=1,
        )
        dbo.rules.history.t.insert().execute(
            change_id=8,
            timestamp=105,
            changed_by="bill",
            rule_id=3,
            product="a",
            priority=100,
            version="3.5",
            buildTarget="a",
            backgroundRate=100,
            mapping="a",
            update_type="minor",
            channel="a",
            data_version=2,
        )
        dbo.rules.t.insert().execute(
            rule_id=4, product="fake", priority=80, buildTarget="d", backgroundRate=100, mapping="a", update_type="minor", channel="a", data_version=1
        )
        dbo.rules.history.t.insert().execute(change_id=9, timestamp=80, changed_by="bill", rule_id=4)
        dbo.rules.history.t.insert().execute(
            change_id=10,
            timestamp=81,
            changed_by="bill",
            rule_id=4,
            product="fake",
            priority=80,
            buildTarget="d",
            backgroundRate=100,
            mapping="a",
            update_type="minor",
            channel="a",
            data_version=1,
        )
        dbo.rules.t.insert().execute(
            rule_id=5, priority=80, buildTarget="d", version="3.3", backgroundRate=0, mapping="c", update_type="minor", product="a", channel="a", data_version=1
        )
        dbo.rules.history.t.insert().execute(change_id=11, timestamp=90, changed_by="bill", rule_id=5)
        dbo.rules.history.t.insert().execute(
            change_id=12,
            timestamp=91,
            changed_by="bill",
            rule_id=5,
            priority=80,
            buildTarget="d",
            version="3.3",
            backgroundRate=0,
            mapping="c",
            update_type="minor",
            product="a",
            channel="a",
            data_version=1,
        )
        dbo.rules.t.insert().execute(rule_id=6, product="fake", priority=40, backgroundRate=50, mapping="a", update_type="minor", channel="e", data_version=1)
        dbo.rules.history.t.insert().execute(change_id=13, timestamp=110, changed_by="bill", rule_id=6)
        dbo.rules.history.t.insert().execute(
            change_id=14,
            timestamp=111,
            changed_by="bill",
            rule_id=6,
            product="fake",
            priority=40,
            backgroundRate=50,
            mapping="a",
            update_type="minor",
            channel="e",
            data_version=1,
        )
        dbo.rules.t.insert().execute(rule_id=7, product="fake", priority=30, backgroundRate=85, mapping="a", update_type="minor", channel="c", data_version=1)
        dbo.rules.history.t.insert().execute(change_id=15, timestamp=115, changed_by="bill", rule_id=7)
        dbo.rules.history.t.insert().execute(
            change_id=16,
            timestamp=116,
            changed_by="bill",
            rule_id=7,
            product="fake",
            priority=30,
            backgroundRate=85,
            mapping="a",
            update_type="minor",
            channel="c",
            data_version=1,
        )
        dbo.rules.t.insert().execute(
            rule_id=8, product="fake2", priority=25, backgroundRate=100, mapping="a", update_type="minor", channel="c", mig64=True, data_version=1
        )
        dbo.rules.history.t.insert().execute(change_id=17, timestamp=150, changed_by="bill", rule_id=8)
        dbo.rules.history.t.insert().execute(
            change_id=18,
            timestamp=151,
            changed_by="bill",
            rule_id=8,
            product="fake2",
            priority=25,
            backgroundRate=100,
            mapping="a",
            update_type="minor",
            channel="c",
            mig64=True,
            data_version=1,
        )
        dbo.rules.t.insert().execute(
            rule_id=9, product="fake3", priority=25, backgroundRate=100, mapping="a", update_type="minor", channel="c", jaws=True, data_version=1
        )
        dbo.rules.history.t.insert().execute(change_id=19, timestamp=160, changed_by="bill", rule_id=9)
        dbo.rules.history.t.insert().execute(
            change_id=20,
            timestamp=161,
            changed_by="bill",
            rule_id=9,
            product="fake3",
            priority=25,
            backgroundRate=100,
            mapping="a",
            update_type="minor",
            channel="c",
            jaws=True,
            data_version=1,
        )
        self.client = app.test_client()

        # Insert a release into the new tables to make sure it doesn't show up
        # in the old API.
        insert_release(firefox_56_0_build1, "Firefox", history=False)

        yield

        dbo.reset()
        os.close(self.version_fd)
        os.remove(self.version_file)
        self.view_base.verified_userinfo = self.orig_base_verified_userinfo
        dbo.releases.history = self.orig_releases_history

    def _get(self, url, qs={}, username=None):
        headers = {"Accept-Encoding": "application/json", "Accept": "application/json"}
        self.mocked_user = username
        ret = self.client.get(url, params=qs, headers=headers)
        return ret

    def _post(self, url, data={}, username="bill", **kwargs):
        self.mocked_user = username
        return self.client.post(url, json=data, **kwargs)

    def _put(self, url, data={}, username="bill"):
        self.mocked_user = username
        return self.client.put(url, json=data)

    def _delete(self, url, qs={}, username="bill"):
        self.mocked_user = username
        return self.client.delete(url, params=qs)

    def assertStatusCode(self, response, expected):
        self.assertEqual(response.status_code, expected, "%d - %s" % (response.status_code, response.text))
