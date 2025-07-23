from copy import deepcopy

import pytest
from aiohttp import ClientError
from mock import MagicMock, mock

import auslib.services.releases
import auslib.util.timestamp
from auslib.blobs.base import createBlob
from auslib.global_state import dbo
from auslib.util.data_structures import deep_dict

from ...fakes import FakeBlobFactory, FakeGCSHistoryAsync


def versions_dict(depth=4, default=1):
    d = deep_dict(depth, default)
    return d


def populate_versions_dict(release, default=1):
    d = versions_dict(default=default)
    for pname, pdata in release["platforms"].items():
        for lname in pdata.get("locales", {}):
            assert d["platforms"][pname]["locales"][lname]

    return d


def test_versions_dict_still_works_as_expected():
    # Tests to make sure our assupmtions about how versions_dict/defaultdict hasn't changed
    # in a way that breaks other tests. If this test fails, we likely need to rework how
    # we're populating old_data_versions/new_data_versions in other tests.
    vd = versions_dict()
    assert vd["a"]["b"]["c"]["d"]
    # This verifies that the above assert populated `vd` correctly.
    assert vd == {"a": {"b": {"c": {"d": 1}}}}
    # This verifies that `vd` doesn't automatically add other entries when comparing it to
    # a dictionary with additional contents.
    assert vd != {"a": {"b": {"c": {"d": 1, "e": 1}}}}


def get_release_history(name):
    return [(k, v) for k, v in dbo.releases_json.history.bucket.blobs.items() if k.startswith(f"{name}/")]


def get_release_assets_history(name, path):
    return [(k, v) for k, v in dbo.release_assets.history.bucket.blobs.items() if k.startswith(f"{name}-{path}/")]


# TODO: It would be great if we could session scope this, and have
# the database revert itself after every test (rather than rebuilding
# more or less from scratch)
@pytest.fixture(scope="function")
def releases_db(
    db_schema,
    insert_release,
    insert_release_sc,
    firefox_56_0_build1,
    firefox_60_0b3_build1,
    firefox_64_0_build1,
    firefox_65_0_build1,
    firefox_66_0_build1,
    firefox_67_0_build1,
    cdm_16,
    cdm_17,
):
    dbo.setDb("sqlite:///:memory:", releases_history_buckets={"*": "fake"}, async_releases_history_class=FakeGCSHistoryAsync)
    db_schema.create_all(dbo.engine)
    dbo.permissions.t.insert().execute(permission="admin", username="bob", data_version=1)
    dbo.permissions.user_roles.t.insert().execute(username="bob", role="releng", data_version=1)
    dbo.permissions.user_roles.t.insert().execute(username="bob", role="tb-releng", data_version=1)
    dbo.productRequiredSignoffs.t.insert().execute(product="Firefox", channel="release", role="releng", signoffs_required=1, data_version=1)
    dbo.releases.t.insert().execute(
        name="Firefox-56.0-build1", product="Firefox", data=createBlob(dict(name="a", schema_version=1, hashFunction="sha512")), data_version=1
    )
    dbo.releases.t.insert().execute(
        name="Firefox-60.0b3-build1", product="Firefox", data=createBlob(dict(name="a", schema_version=1, hashFunction="sha512")), data_version=1
    )
    dbo.releases.t.insert().execute(
        name="Firefox-66.0-build1", product="Firefox", data=createBlob(dict(name="a", schema_version=1, hashFunction="sha512")), data_version=1
    )
    dbo.rules.t.insert().execute(
        rule_id=1, priority=100, product="Firefox", channel="release", mapping="Firefox-56.0-build1", update_type="minor", data_version=1
    )
    dbo.rules.t.insert().execute(
        rule_id=2, priority=100, product="Firefox", channel="beta", mapping="Firefox-60.0b3-build1", update_type="minor", data_version=1
    )
    dbo.rules.t.insert().execute(
        rule_id=3, priority=50, product="Firefox", channel="release", mapping="Firefox-66.0-build1", update_type="minor", data_version=1
    )
    dbo.rules.t.insert().execute(rule_id=4, priority=100, channel="beta", mapping="CDM-17", update_type="minor", data_version=1)
    insert_release(cdm_16, "CDM")
    insert_release(cdm_17, "CDM")
    insert_release(firefox_56_0_build1, "Firefox")
    insert_release(firefox_60_0b3_build1, "Firefox")
    insert_release_sc(firefox_64_0_build1, "Firefox", change_type="insert")
    insert_release(firefox_65_0_build1, "Firefox")
    insert_release(firefox_66_0_build1, "Firefox")
    insert_release_sc(firefox_66_0_build1, "Firefox", signoff_user="bob", signoff_role="releng")
    insert_release(firefox_67_0_build1, "Firefox")
    insert_release_sc(firefox_67_0_build1, "Firefox", change_type="delete", signoff_user="bob", signoff_role="releng")
    insert_release(dict(name="Firefox-empty", schema_version=9, hashFunction="sha512"), "Firefox")
    # Insert a Release into the old table to make sure it doesn't show up in the new API
    dbo.releases.t.insert().execute(name="b", product="b", data=createBlob(dict(name="b", hashFunction="sha512", schema_version=1)), data_version=1)


@pytest.mark.usefixtures("releases_db")
def test_get_releases(api):
    ret = api.get("/v2/releases")
    assert ret.status_code == 200, ret.text
    expected = {
        "releases": [
            {
                "name": "CDM-16",
                "product": "CDM",
                "data_version": 1,
                "read_only": False,
                "rule_info": {},
                "scheduled_changes": [],
                "product_required_signoffs": {},
                "required_signoffs": {},
            },
            {
                "name": "CDM-17",
                "product": "CDM",
                "data_version": 1,
                "read_only": False,
                "rule_info": {"4": {"product": None, "channel": "beta"}},
                "scheduled_changes": [],
                "product_required_signoffs": {},
                "required_signoffs": {},
            },
            {
                "name": "Firefox-56.0-build1",
                "product": "Firefox",
                "data_version": 1,
                "read_only": False,
                "rule_info": {"1": {"product": "Firefox", "channel": "release"}},
                "scheduled_changes": [],
                "product_required_signoffs": {"releng": 1},
                "required_signoffs": {"releng": 1},
            },
            {
                "name": "Firefox-60.0b3-build1",
                "product": "Firefox",
                "data_version": 1,
                "read_only": False,
                "rule_info": {"2": {"product": "Firefox", "channel": "beta"}},
                "scheduled_changes": [],
                "product_required_signoffs": {"releng": 1},
                "required_signoffs": {},
            },
            {
                "name": "Firefox-64.0-build1",
                "product": None,
                "data_version": None,
                "read_only": None,
                "rule_info": {},
                "scheduled_changes": [
                    {
                        "name": "Firefox-64.0-build1",
                        "product": "Firefox",
                        "data_version": 1,
                        "read_only": False,
                        "sc_id": 1,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "insert",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {},
                    },
                    {
                        "name": "Firefox-64.0-build1",
                        "path": ".platforms.Darwin_x86_64-gcc3-u-i386-x86_64.locales.en-US",
                        "data_version": 1,
                        "sc_id": 1,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "insert",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {},
                    },
                    {
                        "name": "Firefox-64.0-build1",
                        "path": ".platforms.Linux_x86-gcc3.locales.en-US",
                        "data_version": 1,
                        "sc_id": 2,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "insert",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {},
                    },
                    {
                        "name": "Firefox-64.0-build1",
                        "path": ".platforms.Linux_x86_64-gcc3.locales.en-US",
                        "data_version": 1,
                        "sc_id": 3,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "insert",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {},
                    },
                    {
                        "name": "Firefox-64.0-build1",
                        "path": ".platforms.WINNT_x86-msvc.locales.en-US",
                        "data_version": 1,
                        "sc_id": 4,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "insert",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {},
                    },
                    {
                        "name": "Firefox-64.0-build1",
                        "path": ".platforms.WINNT_x86_64-msvc.locales.en-US",
                        "data_version": 1,
                        "sc_id": 5,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "insert",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {},
                    },
                ],
            },
            {
                "name": "Firefox-65.0-build1",
                "product": "Firefox",
                "data_version": 1,
                "read_only": False,
                "rule_info": {},
                "scheduled_changes": [],
                "product_required_signoffs": {"releng": 1},
                "required_signoffs": {},
            },
            {
                "name": "Firefox-66.0-build1",
                "product": "Firefox",
                "data_version": 1,
                "read_only": False,
                "rule_info": {"3": {"product": "Firefox", "channel": "release"}},
                "scheduled_changes": [
                    {
                        "name": "Firefox-66.0-build1",
                        "product": "Firefox",
                        "data_version": 1,
                        "read_only": False,
                        "sc_id": 2,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "update",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-66.0-build1",
                        "path": ".platforms.Darwin_x86_64-gcc3-u-i386-x86_64.locales.en-US",
                        "data_version": 1,
                        "sc_id": 6,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "update",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-66.0-build1",
                        "path": ".platforms.Linux_x86-gcc3.locales.en-US",
                        "data_version": 1,
                        "sc_id": 7,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "update",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-66.0-build1",
                        "path": ".platforms.Linux_x86_64-gcc3.locales.en-US",
                        "data_version": 1,
                        "sc_id": 8,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "update",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-66.0-build1",
                        "path": ".platforms.WINNT_aarch64-msvc-aarch64.locales.en-US",
                        "data_version": 1,
                        "sc_id": 9,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "update",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-66.0-build1",
                        "path": ".platforms.WINNT_x86-msvc.locales.en-US",
                        "data_version": 1,
                        "sc_id": 10,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "update",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-66.0-build1",
                        "path": ".platforms.WINNT_x86_64-msvc.locales.en-US",
                        "data_version": 1,
                        "sc_id": 11,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "update",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                ],
                "product_required_signoffs": {"releng": 1},
                "required_signoffs": {"releng": 1},
            },
            {
                "name": "Firefox-67.0-build1",
                "product": "Firefox",
                "data_version": 1,
                "read_only": False,
                "rule_info": {},
                "scheduled_changes": [
                    {
                        "name": "Firefox-67.0-build1",
                        "product": "Firefox",
                        "data_version": 1,
                        "read_only": False,
                        "sc_id": 3,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "delete",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-67.0-build1",
                        "path": ".platforms.Darwin_x86_64-gcc3-u-i386-x86_64.locales.en-US",
                        "data_version": 1,
                        "sc_id": 12,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "delete",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-67.0-build1",
                        "path": ".platforms.Linux_x86-gcc3.locales.en-US",
                        "data_version": 1,
                        "sc_id": 13,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "delete",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-67.0-build1",
                        "path": ".platforms.Linux_x86_64-gcc3.locales.en-US",
                        "data_version": 1,
                        "sc_id": 14,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "delete",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-67.0-build1",
                        "path": ".platforms.WINNT_aarch64-msvc-aarch64.locales.en-US",
                        "data_version": 1,
                        "sc_id": 15,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "delete",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-67.0-build1",
                        "path": ".platforms.WINNT_x86-msvc.locales.en-US",
                        "data_version": 1,
                        "sc_id": 16,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "delete",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                    {
                        "name": "Firefox-67.0-build1",
                        "path": ".platforms.WINNT_x86_64-msvc.locales.en-US",
                        "data_version": 1,
                        "sc_id": 17,
                        "scheduled_by": "bob",
                        "when": 2222222222000,
                        "change_type": "delete",
                        "sc_data_version": 1,
                        "complete": False,
                        "signoffs": {"bob": "releng"},
                    },
                ],
                "product_required_signoffs": {"releng": 1},
                "required_signoffs": {},
            },
            {
                "name": "Firefox-empty",
                "product": "Firefox",
                "data_version": 1,
                "read_only": False,
                "rule_info": {},
                "scheduled_changes": [],
                "product_required_signoffs": {"releng": 1},
                "required_signoffs": {},
            },
        ]
    }
    assert ret.json() == expected


@pytest.mark.usefixtures("releases_db")
def test_get_release_404(api):
    ret = api.get("/v2/releases/Firefox-33.0-build1")
    assert ret.status_code == 404, ret.text


@pytest.mark.usefixtures("releases_db")
def test_get_release(api, firefox_56_0_build1):
    ret = api.get("/v2/releases/Firefox-56.0-build1")
    assert ret.status_code == 200, ret.text

    data_versions = populate_versions_dict(firefox_56_0_build1)
    data_versions["."] = 1

    expected = {"blob": firefox_56_0_build1, "data_versions": data_versions, "sc_blob": {}, "sc_data_versions": {}}

    assert ret.json() == expected, ret.json()


@pytest.mark.usefixtures("releases_db")
def test_get_release_scheduled_insert(api, firefox_64_0_build1):
    ret = api.get("/v2/releases/Firefox-64.0-build1")
    assert ret.status_code == 200, ret.text

    expected_blob = deepcopy(firefox_64_0_build1)
    expected_blob["hashFunction"] = "sha1024"
    for platform in firefox_64_0_build1["platforms"]:
        for locale in firefox_64_0_build1["platforms"][platform].get("locales", []):
            if locale == "en-US":
                expected_blob["platforms"][platform]["locales"][locale]["buildID"] = "123456789"
            else:
                del expected_blob["platforms"][platform]["locales"][locale]

    sc_data_versions = populate_versions_dict(expected_blob)
    sc_data_versions["."] = 1
    expected = {"blob": {}, "data_versions": {}, "sc_blob": expected_blob, "sc_data_versions": sc_data_versions}

    assert ret.json() == expected, ret.json()


@pytest.mark.usefixtures("releases_db")
def test_get_release_scheduled_update(api, firefox_66_0_build1):
    ret = api.get("/v2/releases/Firefox-66.0-build1")
    assert ret.status_code == 200, ret.text

    data_versions = populate_versions_dict(firefox_66_0_build1)
    data_versions["."] = 1
    sc_data_versions = versions_dict()
    sc_data_versions["."] = 1
    expected_blob = deepcopy(firefox_66_0_build1)
    expected_blob["hashFunction"] = "sha1024"
    for platform in expected_blob["platforms"]:
        for locale in expected_blob["platforms"][platform].get("locales", []):
            if locale == "en-US":
                expected_blob["platforms"][platform]["locales"][locale]["buildID"] = "123456789"
                assert sc_data_versions["platforms"][platform]["locales"][locale]

    expected = {
        "blob": firefox_66_0_build1,
        "data_versions": data_versions,
        "sc_blob": expected_blob,
        "sc_data_versions": sc_data_versions,
    }

    assert ret.json() == expected, ret.json()


@pytest.mark.usefixtures("releases_db")
def test_get_release_scheduled_delete(api, firefox_67_0_build1):
    ret = api.get("/v2/releases/Firefox-67.0-build1")
    assert ret.status_code == 200, ret.text

    data_versions = populate_versions_dict(firefox_67_0_build1)
    data_versions["."] = 1
    sc_data_versions = versions_dict()
    sc_data_versions["."] = 1
    for pname, pdata in firefox_67_0_build1["platforms"].items():
        for lname in pdata.get("locales", {}):
            if lname == "en-US":
                assert sc_data_versions["platforms"][pname]["locales"][lname]

    expected = {"blob": firefox_67_0_build1, "data_versions": data_versions, "sc_blob": {}, "sc_data_versions": sc_data_versions}

    assert ret.json() == expected, ret.json()


@pytest.mark.usefixtures("releases_db")
def test_get_data_versions_404(api):
    ret = api.get("/v2/releases/Firefox-33.0-build1/data_versions")
    assert ret.status_code == 404, ret.text


@pytest.mark.usefixtures("releases_db")
def test_get_data_versions(api, firefox_56_0_build1):
    ret = api.get("/v2/releases/Firefox-56.0-build1/data_versions")
    assert ret.status_code == 200, ret.text

    data_versions = populate_versions_dict(firefox_56_0_build1)
    data_versions["."] = 1
    expected = {"data_versions": data_versions}

    assert ret.json() == expected, ret.json()


@pytest.mark.usefixtures("releases_db")
def test_get_data_version_404_on_release(api):
    ret = api.get("/v2/releases/Firefox-33.0-build1/.platforms.Linux_x86_64-gcc3.locales.en-US/data_version")
    assert ret.status_code == 404, ret.text


@pytest.mark.usefixtures("releases_db")
def test_get_data_version_404_on_path(api):
    ret = api.get("/v2/releases/Firefox-56.0-build1/.platforms.Linux_x86_64-gcc3.locales.fake/data_version")
    assert ret.status_code == 404, ret.text


@pytest.mark.usefixtures("releases_db")
def test_get_data_version(api):
    ret = api.get("/v2/releases/Firefox-56.0-build1/.platforms.Linux_x86_64-gcc3.locales.en-US/data_version")
    assert ret.status_code == 200, ret.text

    assert ret.json() == {"data_version": 1}, ret.json()


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_fails_when_signoff_required(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["detailsUrl"] = "https://newurl"
    firefox_56_0_build1["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]["buildID"] = "9999999999999"
    old_data_versions = populate_versions_dict(firefox_56_0_build1)
    old_data_versions["."] = 1

    ret = api.put("/v2/releases/Firefox-56.0-build1", json={"blob": firefox_56_0_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 400


@pytest.mark.usefixtures("releases_db")
def test_put_fails_without_permission(api, firefox_60_0b3_build1, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    firefox_60_0b3_build1["detailsUrl"] = "https://newurl"
    firefox_60_0b3_build1["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]["buildID"] = "9999999999999"
    old_data_versions = populate_versions_dict(firefox_60_0b3_build1)
    old_data_versions["."] = 1

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 403, ret.text


@pytest.mark.usefixtures("releases_db")
def test_put_fails_without_permission_new_release(api, firefox_62_0_build1, mock_verified_userinfo):
    mock_verified_userinfo("notbob")

    ret = api.put("/v2/releases/Firefox-62.0-build1", json={"blob": firefox_62_0_build1, "product": "Firefox"})
    assert ret.status_code == 403, ret.text


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_fails_for_invalid_release(api):
    # Only submit a portion of what's needed to have a valid blob
    data = {"platforms": {"Linux_x86_64-gcc3": {"platforms": {"de": {"appVersion": "65.0", "buildID": "9090909090990", "displayVersion": "65.0"}}}}}

    ret = api.put("/v2/releases/Firefox-65.0-build1", json={"blob": data})
    assert ret.status_code == 400, ret.text


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_fails_for_readonly_release(api, firefox_60_0b3_build1):
    dbo.releases_json.t.update(values={"read_only": True}).where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute()

    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    firefox_60_0b3_build1["detailsUrl"] = "https://newurl"
    firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"
    old_data_versions = populate_versions_dict(firefox_60_0b3_build1)
    old_data_versions["."] = 1

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 400, ret.text
    assert "Cannot overwrite" in ret.json()["exception"]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_fails_for_non_aiohttp_exception_in_future(api, firefox_60_0b3_build1, monkeypatch):
    monkeypatch.setattr(dbo.releases_json.history.bucket, "new_blob", FakeBlobFactory(exc=Exception))
    monkeypatch.setattr(dbo.release_assets.history.bucket, "new_blob", FakeBlobFactory(exc=Exception))

    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    firefox_60_0b3_build1["detailsUrl"] = "https://newurl"
    firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"

    old_data_versions = populate_versions_dict(firefox_60_0b3_build1)
    old_data_versions["."] = 1

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 500, ret.text


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_succeeds(api, firefox_60_0b3_build1):
    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    firefox_60_0b3_build1["detailsUrl"] = "https://newurl"
    firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"

    old_data_versions = populate_versions_dict(firefox_60_0b3_build1)
    old_data_versions["."] = 1
    new_data_versions = versions_dict(default=2)
    new_data_versions["."] = 2
    assert new_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute().fetchone().data
    locale_blob = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.en-US")
        .execute()
        .fetchone()
        .data
    )
    assert base_blob["detailsUrl"] == "https://newurl"
    assert locale_blob["buildID"] == "9999999999999"
    assert "locales" not in base_blob["platforms"]["Linux_x86_64-gcc3"]
    base_history = get_release_history("Firefox-60.0b3-build1")
    assert len(base_history) == 3
    # Check to make sure "changed_by" was set
    assert "-bob.json" in base_history[2][0]
    locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.en-US")
    assert len(locale_history) == 3
    assert "-bob.json" in locale_history[2][0]

    unchanged_locale = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.af")
        .execute()
        .fetchone()
    )
    assert unchanged_locale["data_version"] == 1
    unchanged_locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.af")
    assert len(unchanged_locale_history) == 2


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_succeeds_when_history_writes_fail(api, firefox_60_0b3_build1, monkeypatch):
    mocked_sentry = MagicMock()
    monkeypatch.setattr(dbo.releases_json.history.bucket, "new_blob", FakeBlobFactory(exc=ClientError))
    monkeypatch.setattr(dbo.release_assets.history.bucket, "new_blob", FakeBlobFactory(exc=ClientError))
    monkeypatch.setattr(auslib.services.releases, "capture_exception", mocked_sentry)

    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    firefox_60_0b3_build1["detailsUrl"] = "https://newurl"
    firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"

    old_data_versions = populate_versions_dict(firefox_60_0b3_build1)
    old_data_versions["."] = 1
    new_data_versions = versions_dict(default=2)
    new_data_versions["."] = 2
    assert new_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions

    assert mocked_sentry.call_count == 2

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute().fetchone().data
    locale_blob = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.en-US")
        .execute()
        .fetchone()
        .data
    )
    assert base_blob["detailsUrl"] == "https://newurl"
    assert locale_blob["buildID"] == "9999999999999"
    assert "locales" not in base_blob["platforms"]["Linux_x86_64-gcc3"]

    # These should only contain the pre-existing history entries
    base_history = get_release_history("Firefox-60.0b3-build1")
    assert len(base_history) == 2
    locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.en-US")
    assert len(locale_history) == 2

    unchanged_locale = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.af")
        .execute()
        .fetchone()
    )
    assert unchanged_locale["data_version"] == 1
    unchanged_locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.af")
    assert len(unchanged_locale_history) == 2


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_succeeds_for_new_release(api, firefox_62_0_build1):
    new_data_versions = populate_versions_dict(firefox_62_0_build1)
    new_data_versions["."] = 1

    ret = api.put("/v2/releases/Firefox-62.0-build1", json={"blob": firefox_62_0_build1, "product": "Firefox"})
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions

    # Check all parts of the base blob against the full blob
    base_row = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-62.0-build1").execute().fetchone()
    assert base_row.product == "Firefox"
    base_blob = base_row.data
    split_platforms = ["Linux_x86_64-gcc3", "WINNT_x86_64-msvc", "Linux_x86-gcc3", "WINNT_x86-msvc", "Darwin_x86_64-gcc3-u-i386-x86_64"]
    for k in base_blob:
        # Parts of platforms ends up in the assets table, so we have to check this more carefully
        if k == "platforms":
            for p in base_blob[k]:
                expected = deepcopy(firefox_62_0_build1[k][p])
                if p in split_platforms:
                    del expected["locales"]
                assert base_blob[k][p] == expected
        else:
            assert base_blob[k] == firefox_62_0_build1[k]
    # And that locales didn't end up there
    assert "locales" not in base_blob["platforms"]["Linux_x86_64-gcc3"]
    # Check one random locale from the assets table
    locale_blob = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-62.0-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.en-US")
        .execute()
        .fetchone()
        .data
    )
    assert locale_blob == firefox_62_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    base_history = get_release_history("Firefox-62.0-build1")
    assert len(base_history) == 2
    # Check to make sure "changed_by" was set
    assert "-bob.json" in base_history[1][0]
    locale_history = get_release_assets_history("Firefox-62.0-build1", ".platforms.Linux_x86_64-gcc3.locales.en-US")
    assert len(locale_history) == 2
    assert "-bob.json" in locale_history[1][0]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_removes_locales(api, firefox_60_0b3_build1):
    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    del firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]
    del firefox_60_0b3_build1["platforms"]["Linux_x86-gcc3"]["locales"]["af"]

    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]
    assert old_data_versions["platforms"]["Linux_x86-gcc3"]["locales"]["af"]

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    assert ret.json() == {}

    removed_locales = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path.in_((".platforms.Linux_x86_64-gcc3.locales.de", ".platforms.Linux_x86-gcc3.locales.af")))
        .execute()
        .fetchall()
    )
    assert not removed_locales
    base_history = get_release_history("Firefox-60.0b3-build1")
    assert len(base_history) == 2
    locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.de")
    assert len(locale_history) == 3
    # Check to make sure "changed_by" was set
    assert "-bob.json" in locale_history[2][0]

    unchanged_locale = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.zh-TW")
        .execute()
        .fetchone()
    )
    assert unchanged_locale["data_version"] == 1
    unchanged_locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.zh-TW")
    assert len(unchanged_locale_history) == 2


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_remove_add_and_update_locales(api, firefox_60_0b3_build1):
    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    newde = firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]
    del firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]
    firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["af"]["buildID"] = "7777777777"
    firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["newde"] = newde

    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    new_data_versions = versions_dict()
    assert old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["af"]
    assert old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]
    new_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["af"] = 2
    assert new_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["newde"]

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions

    removed_locales = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path.in_((".platforms.Linux_x86_64-gcc3.locales.de",)))
        .execute()
        .fetchall()
    )
    assert not removed_locales
    got_newde = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.newde")
        .execute()
        .fetchone()
        .data
    )
    assert newde == got_newde
    base_history = get_release_history("Firefox-60.0b3-build1")
    assert len(base_history) == 2
    de_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.de")
    assert len(de_history) == 3
    # Check to make sure "changed_by" was set
    assert "-bob.json" in de_history[2][0]
    af_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.af")
    assert len(af_history) == 3
    assert "-bob.json" in af_history[2][0]
    newde_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.newde")
    assert len(newde_history) == 2
    assert "-bob.json" in newde_history[1][0]

    unchanged_locale = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.zh-TW")
        .execute()
        .fetchone()
    )
    assert unchanged_locale["data_version"] == 1
    unchanged_locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.zh-TW")
    assert len(unchanged_locale_history) == 2


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_succeeds_for_nonsplit_release(api, cdm_17):
    cdm_17 = deepcopy(cdm_17)
    cdm_17["vendors"]["gmp-eme-adobe"]["platforms"]["WINNT_x86-msvc"]["filesize"] = 5555555555
    old_data_versions = versions_dict()
    old_data_versions["."] = 1

    ret = api.put("/v2/releases/CDM-17", json={"blob": cdm_17, "product": "CDM", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    assert ret.json() == {".": 2}

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "CDM-17").execute().fetchone().data
    assert base_blob == cdm_17
    history = get_release_history("CDM-17")
    assert len(history) == 3
    # Check to make sure "changed_by" was set
    assert "-bob.json" in history[2][0]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_cancels_scheduled_updates(api, firefox_66_0_build1):
    old_data_versions = populate_versions_dict(firefox_66_0_build1)

    ret = api.put("/v2/releases/Firefox-66.0-build1", json={"blob": firefox_66_0_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text

    base_sc = (
        dbo.releases_json.scheduled_changes.t.select()
        .where(dbo.releases_json.scheduled_changes.base_name == "Firefox-66.0-build1")
        .where(dbo.releases_json.scheduled_changes.complete is False)
        .execute()
        .fetchall()
    )
    assert len(base_sc) == 0
    locale_sc = (
        dbo.release_assets.scheduled_changes.t.select()
        .where(dbo.release_assets.scheduled_changes.base_name == "Firefox-66.0-build1")
        .where(dbo.release_assets.scheduled_changes.complete is False)
        .execute()
        .fetchall()
    )
    assert len(locale_sc) == 0


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_fails_when_release_doesnt_exist(api):
    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "999999999999999"}}}}}
    old_data_versions = populate_versions_dict(blob)
    old_data_versions["."] = 1

    ret = api.post("/v2/releases/Firefox-58.0-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 404


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_fails_when_signoff_required(api):
    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "999999999999999"}}}}}
    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]

    ret = api.post("/v2/releases/Firefox-56.0-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 400


@pytest.mark.usefixtures("releases_db")
def test_post_fails_without_permission(api, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "999999999999999"}}}}}
    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 403, ret.text


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_fails_for_invalid_release_base(api):
    # Add an invalid parameter to the blob
    data = {"foo": "foo"}
    old_data_versions = versions_dict()
    old_data_versions["."] = 1

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": data, "old_data_versions": old_data_versions})
    assert ret.status_code == 400, ret.text
    assert ret.json()["detail"] == "Invalid Blob", ret.json()


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_fails_for_invalid_release_locale(api):
    # add an invalid key to a locale section
    data = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"de": {"foo": "foo"}}}}}
    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": data, "old_data_versions": old_data_versions})
    assert ret.status_code == 400, ret.text
    assert ret.json()["detail"] == "Invalid Blob", ret.json()


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_fails_for_readonly_release(api, firefox_60_0b3_build1):
    dbo.releases_json.t.update(values={"read_only": True}).where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute()

    data = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"de": {"buildID": "333333333333"}}}}}
    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": data, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 400, ret.text
    assert "Cannot update" in ret.json()["exception"]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_fails_update_without_data_version(api):
    blob = {"platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "22222222222"}}}}}
    old_data_versions = {"platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {}}}}
    ret = api.post("/v2/releases/Firefox-empty", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    blob = {"platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "33333333333"}}}}}
    ret = api.post("/v2/releases/Firefox-empty", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 400, ret.text
    assert ret.json()["exception"] == "Missing data_version for .platforms.Darwin_x86_64-gcc3-u-i386-x86_64.locales.de"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_fails_for_non_aiohttp_exception_in_future(api, monkeypatch):
    monkeypatch.setattr(dbo.releases_json.history.bucket, "new_blob", FakeBlobFactory(exc=Exception))
    monkeypatch.setattr(dbo.release_assets.history.bucket, "new_blob", FakeBlobFactory(exc=Exception))

    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "22222222222"}}}}}

    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 500, ret.text


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_succeeds(api):
    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "22222222222"}}}}}

    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]
    new_data_versions = versions_dict(default=2)
    new_data_versions["."] = 2
    assert new_data_versions["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute().fetchone().data
    locale_blob = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Darwin_x86_64-gcc3-u-i386-x86_64.locales.de")
        .execute()
        .fetchone()
        .data
    )
    assert base_blob["detailsUrl"] == "https://newurl"
    assert locale_blob["buildID"] == "22222222222"
    # Make sure something we didn't touch on the blobs are unchanged
    assert base_blob["appVersion"] == "60.0"
    assert locale_blob["appVersion"] == "60.0"
    # Make sure that no locale information made it into the base blob
    assert "locales" not in base_blob["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]
    base_history = get_release_history("Firefox-60.0b3-build1")
    assert len(base_history) == 3
    # Check to make sure "changed_by" was set
    assert "-bob.json" in base_history[2][0]
    locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Darwin_x86_64-gcc3-u-i386-x86_64.locales.de")
    assert len(locale_history) == 3
    assert "-bob.json" in locale_history[2][0]

    unchanged_locale = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.zh-TW")
        .execute()
        .fetchone()
    )
    assert unchanged_locale["data_version"] == 1
    unchanged_locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.zh-TW")
    assert len(unchanged_locale_history) == 2


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_succeeds_when_history_writes_fails(api, monkeypatch):
    mocked_sentry = MagicMock()
    monkeypatch.setattr(dbo.releases_json.history.bucket, "new_blob", FakeBlobFactory(exc=ClientError))
    monkeypatch.setattr(dbo.release_assets.history.bucket, "new_blob", FakeBlobFactory(exc=ClientError))
    monkeypatch.setattr(auslib.services.releases, "capture_exception", mocked_sentry)

    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "22222222222"}}}}}

    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]
    new_data_versions = versions_dict(default=2)
    new_data_versions["."] = 2
    assert new_data_versions["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions

    assert mocked_sentry.call_count == 2

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute().fetchone().data
    locale_blob = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Darwin_x86_64-gcc3-u-i386-x86_64.locales.de")
        .execute()
        .fetchone()
        .data
    )
    assert base_blob["detailsUrl"] == "https://newurl"
    assert locale_blob["buildID"] == "22222222222"
    # Make sure something we didn't touch on the blobs are unchanged
    assert base_blob["appVersion"] == "60.0"
    assert locale_blob["appVersion"] == "60.0"
    # Make sure that no locale information made it into the base blob
    assert "locales" not in base_blob["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]

    # This should only contain pre-existing history entries
    base_history = get_release_history("Firefox-60.0b3-build1")
    assert len(base_history) == 2
    locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Darwin_x86_64-gcc3-u-i386-x86_64.locales.de")
    assert len(locale_history) == 2

    unchanged_locale = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.zh-TW")
        .execute()
        .fetchone()
    )
    assert unchanged_locale["data_version"] == 1
    unchanged_locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.zh-TW")
    assert len(unchanged_locale_history) == 2


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_add_and_update_locales(api, firefox_60_0b3_build1):
    blob = {
        "platforms": {
            "Linux_x86_64-gcc3": {
                "locales": {"af": {"buildID": "7777777777"}, "newde": firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]}
            }
        }
    }

    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["af"]
    new_data_versions = versions_dict(default=1)
    new_data_versions["."] = 1
    new_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["af"] = 2
    assert new_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["newde"]

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": blob, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions

    got_newde = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.newde")
        .execute()
        .fetchone()
        .data
    )
    assert got_newde == firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]
    af_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.af")
    assert len(af_history) == 3
    # Check to make sure "changed_by" was set
    assert "-bob.json" in af_history[2][0]
    newde_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.newde")
    assert len(newde_history) == 2
    assert "-bob.json" in newde_history[1][0]

    unchanged_locale = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.Linux_x86_64-gcc3.locales.zh-TW")
        .execute()
        .fetchone()
    )
    assert unchanged_locale["data_version"] == 1
    unchanged_locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.Linux_x86_64-gcc3.locales.zh-TW")
    assert len(unchanged_locale_history) == 2


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_succeeds_overwrite_updates(api):
    blob = {
        "platforms": {
            "WINNT_x86_64-msvc": {
                "locales": {
                    "af": {
                        "completes": [
                            {
                                "filesize": 99999999,
                                "from": "*",
                                "hashValue": "1111111111111111111111111111111111111111111111111111111111111111"
                                "1111111111111111111111111111111111111111111111111111111111111111",
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 11111,
                                "from": "Firefox-59.0b12-build1",
                                "hashValue": "2222222222222222222222222222222222222222222222222222222222222222"
                                "2222222222222222222222222222222222222222222222222222222222222222",
                            }
                        ],
                    }
                }
            }
        }
    }

    old_data_versions = versions_dict()
    assert old_data_versions["platforms"]["WINNT_x86_64-msvc"]["locales"]["af"]
    new_data_versions = versions_dict(default=2)
    assert new_data_versions["platforms"]["WINNT_x86_64-msvc"]["locales"]["af"]

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions

    locale_blob = (
        dbo.release_assets.t.select()
        .where(dbo.release_assets.name == "Firefox-60.0b3-build1")
        .where(dbo.release_assets.path == ".platforms.WINNT_x86_64-msvc.locales.af")
        .execute()
        .fetchone()
        .data
    )
    assert locale_blob["completes"] == blob["platforms"]["WINNT_x86_64-msvc"]["locales"]["af"]["completes"]
    assert locale_blob["partials"] == blob["platforms"]["WINNT_x86_64-msvc"]["locales"]["af"]["partials"]
    # Make sure something we didn't touch on the blobs are unchanged
    assert locale_blob["appVersion"] == "60.0"
    # Make sure that no locale information made it into the base blob
    locale_history = get_release_assets_history("Firefox-60.0b3-build1", ".platforms.WINNT_x86_64-msvc.locales.af")
    assert len(locale_history) == 3
    assert "-bob.json" in locale_history[2][0]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_succeeds_for_nonsplit_release(api, cdm_17):
    cdm_17 = deepcopy(cdm_17)
    blob = {"vendors": {"gmp-eme-adobe": {"platforms": {"WINNT_x86-msvc": {"filesize": 5555555555}}}}}
    cdm_17["vendors"]["gmp-eme-adobe"]["platforms"]["WINNT_x86-msvc"]["filesize"] = 5555555555
    old_data_versions = versions_dict()
    old_data_versions["."] = 1

    ret = api.post("/v2/releases/CDM-17", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.text
    assert ret.json() == {".": 2}

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "CDM-17").execute().fetchone().data
    assert base_blob == cdm_17
    history = get_release_history("CDM-17")
    assert len(history) == 3
    # Check to make sure "changed_by" was set
    assert "-bob.json" in history[2][0]


@pytest.mark.usefixtures("releases_db")
def test_put_add_scheduled_change_fails_without_permission(api, firefox_56_0_build1, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["displayVersion"] = "sixty five dot oh"

    old_data_versions = versions_dict()
    old_data_versions["."] = 1

    ret = api.put(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": firefox_56_0_build1, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1991639932000},
    )
    assert ret.status_code == 403, ret.text


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_add_scheduled_change_base_only(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["displayVersion"] = "sixty five dot oh"

    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    new_data_versions = {".": {"sc_id": 4, "data_version": 1, "change_type": "update", "signoffs": {"bob": "releng"}, "when": 1991639932000}}

    ret = api.put(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": firefox_56_0_build1, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1991639932000},
    )
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions, ret.json()

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-56.0-build1").execute().fetchone()["data"]
    assert base_blob["displayVersion"] == "56.0"

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-56.0-build1").execute().fetchone()
    base_sc_cond = (
        dbo.releases_json.scheduled_changes.conditions.t.select()
        .where(dbo.releases_json.scheduled_changes.conditions.sc_id == base_sc["sc_id"])
        .execute()
        .fetchone()
    )
    base_sc_signoffs = (
        dbo.releases_json.scheduled_changes.signoffs.t.select()
        .where(dbo.releases_json.scheduled_changes.signoffs.sc_id == base_sc["sc_id"])
        .execute()
        .fetchall()
    )
    assert base_sc["scheduled_by"] == "bob"
    assert base_sc["complete"] is False
    assert base_sc["data_version"] == 1
    assert base_sc["base_data"]["displayVersion"] == "sixty five dot oh"
    assert "locales" not in base_sc["base_data"]["platforms"]["Linux_x86_64-gcc3"]
    assert base_sc["base_product"] == "Firefox"
    assert base_sc["base_data_version"] == 1
    assert base_sc_cond["when"] == 1991639932000
    assert len(base_sc_signoffs) == 1
    assert base_sc_signoffs[0]["username"] == "bob"
    assert base_sc_signoffs[0]["role"] == "releng"

    locale_sc = (
        dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.base_name == "Firefox-56.0-build1").execute().fetchall()
    )
    assert len(locale_sc) == 0


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_add_scheduled_change_locale_only(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"

    old_data_versions = versions_dict()
    assert old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    new_data_versions = {
        "platforms": {
            "Linux_x86_64-gcc3": {
                "locales": {"en-US": {"sc_id": 18, "data_version": 1, "change_type": "update", "signoffs": {"bob": "releng"}, "when": 1991639932000}}
            }
        }
    }

    ret = api.put(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": firefox_56_0_build1, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1991639932000},
    )
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions, ret.json()

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-56.0-build1").execute().fetchall()
    assert len(base_sc) == 0

    locale_sc = (
        dbo.release_assets.scheduled_changes.t.select()
        .where(dbo.release_assets.scheduled_changes.base_name == "Firefox-56.0-build1")
        .where(dbo.release_assets.scheduled_changes.base_path == ".platforms.Linux_x86_64-gcc3.locales.en-US")
        .execute()
        .fetchone()
    )
    locale_sc_cond = (
        dbo.release_assets.scheduled_changes.conditions.t.select()
        .where(dbo.release_assets.scheduled_changes.conditions.sc_id == locale_sc["sc_id"])
        .execute()
        .fetchone()
    )
    locale_sc_signoffs = (
        dbo.release_assets.scheduled_changes.signoffs.t.select()
        .where(dbo.release_assets.scheduled_changes.signoffs.sc_id == locale_sc["sc_id"])
        .execute()
        .fetchall()
    )
    assert locale_sc["scheduled_by"] == "bob"
    assert locale_sc["complete"] is False
    assert locale_sc["data_version"] == 1
    assert locale_sc["base_data"] == firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    assert locale_sc["base_data_version"] == 1
    assert locale_sc_cond["when"] == 1991639932000
    assert len(locale_sc_signoffs) == 1
    assert locale_sc_signoffs[0]["username"] == "bob"
    assert locale_sc_signoffs[0]["role"] == "releng"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_put_add_scheduled_change_base_and_locale(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["displayVersion"] = "fifty six dot oh"
    firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"

    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    new_data_versions = {
        ".": {"sc_id": 4, "data_version": 1, "change_type": "update", "signoffs": {"bob": "releng"}, "when": 1991639932000},
        "platforms": {
            "Linux_x86_64-gcc3": {
                "locales": {"en-US": {"sc_id": 18, "data_version": 1, "change_type": "update", "signoffs": {"bob": "releng"}, "when": 1991639932000}}
            }
        },
    }

    ret = api.put(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": firefox_56_0_build1, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1991639932000},
    )
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions, ret.json()

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-56.0-build1").execute().fetchone()["data"]
    assert base_blob["displayVersion"] == "56.0"

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-56.0-build1").execute().fetchone()
    base_sc_cond = (
        dbo.releases_json.scheduled_changes.conditions.t.select()
        .where(dbo.releases_json.scheduled_changes.conditions.sc_id == base_sc["sc_id"])
        .execute()
        .fetchone()
    )
    base_sc_signoffs = (
        dbo.releases_json.scheduled_changes.signoffs.t.select()
        .where(dbo.releases_json.scheduled_changes.signoffs.sc_id == base_sc["sc_id"])
        .execute()
        .fetchall()
    )
    assert base_sc["scheduled_by"] == "bob"
    assert base_sc["complete"] is False
    assert base_sc["data_version"] == 1
    assert base_sc["base_data"]["displayVersion"] == "fifty six dot oh"
    assert "locales" not in base_sc["base_data"]["platforms"]["Linux_x86_64-gcc3"]
    assert base_sc["base_product"] == "Firefox"
    assert base_sc["base_data_version"] == 1
    assert base_sc_cond["when"] == 1991639932000
    assert len(base_sc_signoffs) == 1
    assert base_sc_signoffs[0]["username"] == "bob"
    assert base_sc_signoffs[0]["role"] == "releng"

    locale_sc = (
        dbo.release_assets.scheduled_changes.t.select()
        .where(dbo.release_assets.scheduled_changes.base_name == "Firefox-56.0-build1")
        .where(dbo.release_assets.scheduled_changes.base_path == ".platforms.Linux_x86_64-gcc3.locales.en-US")
        .execute()
        .fetchone()
    )
    locale_sc_cond = (
        dbo.release_assets.scheduled_changes.conditions.t.select().where(dbo.release_assets.scheduled_changes.conditions.sc_id == 18).execute().fetchone()
    )
    locale_sc_signoffs = (
        dbo.release_assets.scheduled_changes.signoffs.t.select().where(dbo.release_assets.scheduled_changes.signoffs.sc_id == 18).execute().fetchall()
    )
    assert locale_sc["scheduled_by"] == "bob"
    assert locale_sc["complete"] is False
    assert locale_sc["data_version"] == 1
    assert locale_sc["base_data"] == firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    assert locale_sc["base_data_version"] == 1
    assert locale_sc_cond["when"] == 1991639932000
    assert len(locale_sc_signoffs) == 1
    assert locale_sc_signoffs[0]["username"] == "bob"
    assert locale_sc_signoffs[0]["role"] == "releng"


@pytest.mark.usefixtures("releases_db")
def test_post_add_scheduled_change_fails_without_permission(api, firefox_56_0_build1, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["displayVersion"] = "fifty six dot oh"

    old_data_versions = versions_dict()
    old_data_versions["."] = 1

    ret = api.post(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": {"displayVersion": "fifty six dot oh"}, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1991639932000},
    )
    assert ret.status_code == 403, ret.text


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_add_scheduled_change_base_only(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["displayVersion"] = "fifty six dot oh"

    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    new_data_versions = {".": {"sc_id": 4, "data_version": 1, "change_type": "update", "signoffs": {"bob": "releng"}, "when": 1991639932000}}

    ret = api.post(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": {"displayVersion": "fifty six dot oh"}, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1991639932000},
    )
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions, ret.json()

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-56.0-build1").execute().fetchone()["data"]
    assert base_blob["displayVersion"] == "56.0"

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-56.0-build1").execute().fetchone()
    base_sc_cond = (
        dbo.releases_json.scheduled_changes.conditions.t.select()
        .where(dbo.releases_json.scheduled_changes.conditions.sc_id == base_sc["sc_id"])
        .execute()
        .fetchone()
    )
    base_sc_signoffs = (
        dbo.releases_json.scheduled_changes.signoffs.t.select()
        .where(dbo.releases_json.scheduled_changes.signoffs.sc_id == base_sc["sc_id"])
        .execute()
        .fetchall()
    )
    assert base_sc["scheduled_by"] == "bob"
    assert base_sc["complete"] is False
    assert base_sc["data_version"] == 1
    assert base_sc["base_data"]["displayVersion"] == "fifty six dot oh"
    assert "locales" not in base_sc["base_data"]["platforms"]["Linux_x86_64-gcc3"]
    assert base_sc["base_product"] == "Firefox"
    assert base_sc["base_data_version"] == 1
    assert base_sc_cond["when"] == 1991639932000
    assert len(base_sc_signoffs) == 1
    assert base_sc_signoffs[0]["username"] == "bob"
    assert base_sc_signoffs[0]["role"] == "releng"

    locale_sc = (
        dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.base_name == "Firefox-56.0-build1").execute().fetchall()
    )
    assert len(locale_sc) == 0


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_add_scheduled_change_locale_only(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"
    blob = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": {"buildID": "9999999999999"}}}}}

    old_data_versions = versions_dict()
    assert old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    new_data_versions = {
        "platforms": {
            "Linux_x86_64-gcc3": {
                "locales": {"en-US": {"sc_id": 18, "data_version": 1, "change_type": "update", "signoffs": {"bob": "releng"}, "when": 1991639932000}}
            }
        }
    }

    ret = api.post(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": blob, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1991639932000},
    )
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions, ret.json()

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-56.0-build1").execute().fetchall()
    assert len(base_sc) == 0

    locale_sc = (
        dbo.release_assets.scheduled_changes.t.select()
        .where(dbo.release_assets.scheduled_changes.base_name == "Firefox-56.0-build1")
        .where(dbo.release_assets.scheduled_changes.base_path == ".platforms.Linux_x86_64-gcc3.locales.en-US")
        .execute()
        .fetchone()
    )
    locale_sc_cond = (
        dbo.release_assets.scheduled_changes.conditions.t.select()
        .where(dbo.release_assets.scheduled_changes.conditions.sc_id == locale_sc["sc_id"])
        .execute()
        .fetchone()
    )
    locale_sc_signoffs = (
        dbo.release_assets.scheduled_changes.signoffs.t.select()
        .where(dbo.release_assets.scheduled_changes.signoffs.sc_id == locale_sc["sc_id"])
        .execute()
        .fetchall()
    )
    assert locale_sc["scheduled_by"] == "bob"
    assert locale_sc["complete"] is False
    assert locale_sc["data_version"] == 1
    assert locale_sc["base_data"] == firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    assert locale_sc["base_data_version"] == 1
    assert locale_sc_cond["when"] == 1991639932000
    assert len(locale_sc_signoffs) == 1
    assert locale_sc_signoffs[0]["username"] == "bob"
    assert locale_sc_signoffs[0]["role"] == "releng"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_post_add_scheduled_change_base_and_locale(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"
    blob = {"displayVersion": "fifty six dot oh", "platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": {"buildID": "9999999999999"}}}}}

    old_data_versions = versions_dict()
    old_data_versions["."] = 1
    assert old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    new_data_versions = {
        ".": {"sc_id": 4, "data_version": 1, "change_type": "update", "signoffs": {"bob": "releng"}, "when": 1991639932000},
        "platforms": {
            "Linux_x86_64-gcc3": {
                "locales": {"en-US": {"sc_id": 18, "data_version": 1, "change_type": "update", "signoffs": {"bob": "releng"}, "when": 1991639932000}}
            }
        },
    }

    ret = api.post(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": blob, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1991639932000},
    )
    assert ret.status_code == 200, ret.text
    assert ret.json() == new_data_versions, ret.json()

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-56.0-build1").execute().fetchone()["data"]
    assert base_blob["displayVersion"] == "56.0"

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-56.0-build1").execute().fetchone()
    base_sc_cond = (
        dbo.releases_json.scheduled_changes.conditions.t.select()
        .where(dbo.releases_json.scheduled_changes.conditions.sc_id == base_sc["sc_id"])
        .execute()
        .fetchone()
    )
    base_sc_signoffs = (
        dbo.releases_json.scheduled_changes.signoffs.t.select()
        .where(dbo.releases_json.scheduled_changes.signoffs.sc_id == base_sc["sc_id"])
        .execute()
        .fetchall()
    )
    assert base_sc["scheduled_by"] == "bob"
    assert base_sc["complete"] is False
    assert base_sc["data_version"] == 1
    assert base_sc["base_data"]["displayVersion"] == "fifty six dot oh"
    assert "locales" not in base_sc["base_data"]["platforms"]["Linux_x86_64-gcc3"]
    assert base_sc["base_product"] == "Firefox"
    assert base_sc["base_data_version"] == 1
    assert base_sc_cond["when"] == 1991639932000
    assert len(base_sc_signoffs) == 1
    assert base_sc_signoffs[0]["username"] == "bob"
    assert base_sc_signoffs[0]["role"] == "releng"

    locale_sc = (
        dbo.release_assets.scheduled_changes.t.select()
        .where(dbo.release_assets.scheduled_changes.base_name == "Firefox-56.0-build1")
        .where(dbo.release_assets.scheduled_changes.base_path == ".platforms.Linux_x86_64-gcc3.locales.en-US")
        .execute()
        .fetchone()
    )
    locale_sc_cond = (
        dbo.release_assets.scheduled_changes.conditions.t.select()
        .where(dbo.release_assets.scheduled_changes.conditions.sc_id == locale_sc["sc_id"])
        .execute()
        .fetchone()
    )
    locale_sc_signoffs = (
        dbo.release_assets.scheduled_changes.signoffs.t.select()
        .where(dbo.release_assets.scheduled_changes.signoffs.sc_id == locale_sc["sc_id"])
        .execute()
        .fetchall()
    )
    assert locale_sc["scheduled_by"] == "bob"
    assert locale_sc["complete"] is False
    assert locale_sc["data_version"] == 1
    assert locale_sc["base_data"] == firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    assert locale_sc["base_data_version"] == 1
    assert locale_sc_cond["when"] == 1991639932000
    assert len(locale_sc_signoffs) == 1
    assert locale_sc_signoffs[0]["username"] == "bob"
    assert locale_sc_signoffs[0]["role"] == "releng"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_delete_release_404(api):
    ret = api.delete("/v2/releases/Firefox-55.0b3-build1")
    assert ret.status_code == 404, ret.text


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_delete_release_mapped_to(api):
    ret = api.delete("/v2/releases/Firefox-60.0b3-build1")
    assert ret.status_code == 400, ret.text
    assert "mapped to" in ret.json()["exception"], ret.json()


@pytest.mark.usefixtures("releases_db")
def test_delete_release_without_permission(api, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    ret = api.delete("/v2/releases/CDM-16")
    assert ret.status_code == 403, ret.text


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_delete_release(api):
    ret = api.delete("/v2/releases/Firefox-65.0-build1")
    assert ret.status_code == 200, ret.text

    assert len(dbo.releases_json.t.select(dbo.releases_json.name).where(dbo.releases_json.name == "Firefox-65.0-build1").execute().fetchall()) == 0
    assert len(dbo.release_assets.t.select(dbo.release_assets.name).where(dbo.release_assets.name == "Firefox-65.0-build1").execute().fetchall()) == 0


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_delete_scheduled_insert(api):
    ret = api.delete("/v2/releases/Firefox-64.0-build1")
    assert ret.status_code == 200, ret.text

    assert (
        len(dbo.releases_json.scheduled_changes.t.select(dbo.releases_json.name).where(dbo.releases_json.name == "Firefox-64.0-build1").execute().fetchall())
        == 0
    )
    assert (
        len(dbo.release_assets.scheduled_changes.t.select(dbo.release_assets.name).where(dbo.release_assets.name == "Firefox-64.0-build1").execute().fetchall())
        == 0
    )


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_delete_nonsplit_release(api):
    ret = api.delete("/v2/releases/CDM-16")
    assert ret.status_code == 200, ret.text

    assert len(dbo.releases_json.t.select(dbo.releases_json.name).where(dbo.releases_json.name == "CDM-16").execute().fetchall()) == 0
    assert len(dbo.release_assets.t.select(dbo.release_assets.name).where(dbo.release_assets.name == "CDM-16").execute().fetchall()) == 0


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_delete_fails_for_readonly_release(api):
    dbo.releases_json.t.update(values={"read_only": True}).where(dbo.releases_json.name == "Firefox-65.0-build1").execute()

    ret = api.delete("/v2/releases/Firefox-65.0-build1")
    assert ret.status_code == 400, ret.text
    assert "Cannot delete" in ret.json()["exception"]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_set_readonly_404(api):
    ret = api.put("/v2/releases/Firefox-22.0-build1/read_only", json={"read_only": True, "old_data_version": 1})
    assert ret.status_code == 404, ret.text


@pytest.mark.usefixtures("releases_db")
def test_set_readonly_without_permission(api, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    ret = api.put("/v2/releases/Firefox-60.0b3-build1/read_only", json={"read_only": True, "old_data_version": 1})
    assert ret.status_code == 403, ret.text


@pytest.mark.usefixtures("releases_db")
def test_set_readwrite_without_permission(api, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    dbo.releases_json.t.update(values={"read_only": False}).where(dbo.releases_json.name == "CDM-16").execute()
    ret = api.put("/v2/releases/CDM-16/read_only", json={"read_only": True, "old_data_version": 1})
    assert ret.status_code == 403, ret.text


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_set_readonly(api):
    ret = api.put("/v2/releases/Firefox-60.0b3-build1/read_only", json={"read_only": True, "old_data_version": 1})
    assert ret.status_code == 200, ret.text
    assert ret.json()["."] == 2

    got = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute().fetchone().read_only
    assert got is True


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_set_readonly_when_rule_requires_signoff(api):
    ret = api.put("/v2/releases/Firefox-56.0-build1/read_only", json={"read_only": True, "old_data_version": 1})
    assert ret.status_code == 200, ret.text
    assert ret.json()["."] == 2

    got = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-56.0-build1").execute().fetchone().read_only
    assert got is True


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_set_readwrite(api):
    dbo.releases_json.t.update(values={"read_only": True}).where(dbo.releases_json.name == "CDM-16").execute()
    ret = api.put("/v2/releases/CDM-16/read_only", json={"read_only": False, "old_data_version": 1})
    assert ret.status_code == 200, ret.text
    assert ret.json()["."] == 2

    got = dbo.releases_json.t.select().where(dbo.releases_json.name == "CDM-16").execute().fetchone().read_only
    assert got is False


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_set_readwrite_scheduled_change_because_of_rule(api, monkeypatch):
    mocked_time = MagicMock()
    mocked_time.time.return_value = 3333333333
    # We patch the time object instead of the method because patching the method
    # causes SQLAlchemy to break (probably because we're patching a global object?)
    monkeypatch.setattr(auslib.util.timestamp, "time", mocked_time)

    dbo.releases_json.t.update(values={"read_only": True}).where(dbo.releases_json.name == "Firefox-56.0-build1").execute()
    ret = api.put("/v2/releases/Firefox-56.0-build1/read_only", json={"read_only": False, "old_data_version": 1})
    assert ret.status_code == 200, ret.text
    assert ret.json() == {".": {"sc_id": 4, "data_version": 1, "change_type": "update", "signoffs": {"bob": "releng"}, "when": 3333333363000}}

    read_only = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-56.0-build1").execute().fetchone()["read_only"]
    assert read_only is True

    sc_read_only = (
        dbo.releases_json.scheduled_changes.t.select()
        .where(dbo.releases_json.scheduled_changes.base_name == "Firefox-56.0-build1")
        .execute()
        .fetchone()["base_read_only"]
    )
    assert sc_read_only is False


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_set_readwrite_scheduled_change_because_of_product(api, monkeypatch):
    mocked_time = MagicMock()
    mocked_time.time.return_value = 3333333333
    # We patch the time object instead of the method because patching the method
    # causes SQLAlchemy to break (probably because we're patching a global object?)
    monkeypatch.setattr(auslib.util.timestamp, "time", mocked_time)

    dbo.releases_json.t.update(values={"read_only": True}).where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute()
    ret = api.put("/v2/releases/Firefox-60.0b3-build1/read_only", json={"read_only": False, "old_data_version": 1})
    assert ret.status_code == 200, ret.text
    # This endpoint automatically schedules 30 seconds into the future
    assert ret.json() == {".": {"sc_id": 4, "data_version": 1, "change_type": "update", "signoffs": {}, "when": 3333333363000}}

    read_only = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute().fetchone()["read_only"]
    assert read_only is True

    sc_read_only = (
        dbo.releases_json.scheduled_changes.t.select()
        .where(dbo.releases_json.scheduled_changes.base_name == "Firefox-60.0b3-build1")
        .execute()
        .fetchone()["base_read_only"]
    )
    assert sc_read_only is False


@pytest.mark.usefixtures("releases_db")
def test_signoff_as_system_account(api, mock_verified_userinfo):
    mock_verified_userinfo("ffxbld")
    ret = api.put("/v2/releases/Firefox-64.0-build1/signoff", json={"role": "releng"})
    assert ret.status_code == 403, ret.text
    assert "ffxbld cannot signoff" in ret.json()["exception"]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_signoff_without_role(api):
    ret = api.put("/v2/releases/Firefox-64.0-build1/signoff", json={"role": "relman"})
    assert ret.status_code == 403, ret.text
    assert "bob cannot signoff with role 'relman'" in ret.json()["exception"]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_signoff_with_second_role(api):
    ret = api.put("/v2/releases/Firefox-67.0-build1/signoff", json={"role": "tb-releng"})
    assert ret.status_code == 403, ret.text
    assert "Cannot signoff with a second role" in ret.json()["exception"]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_signoff(api):
    ret = api.put("/v2/releases/Firefox-64.0-build1/signoff", json={"role": "releng"})
    assert ret.status_code == 200, ret.text

    sc_id = (
        dbo.releases_json.scheduled_changes.t.select(dbo.releases_json.scheduled_changes.sc_id)
        .where(dbo.releases_json.scheduled_changes.base_name == "Firefox-64.0-build1")
        .execute()
        .fetchone()["sc_id"]
    )
    base_signoffs = (
        dbo.releases_json.scheduled_changes.signoffs.t.select().where(dbo.releases_json.scheduled_changes.signoffs.sc_id == sc_id).execute().fetchall()
    )
    assert len(base_signoffs) == 1
    assert base_signoffs[0]["username"] == "bob"
    assert base_signoffs[0]["role"] == "releng"

    asset_scs = (
        dbo.release_assets.scheduled_changes.t.select(dbo.release_assets.scheduled_changes.sc_id)
        .where(dbo.release_assets.scheduled_changes.base_name == "Firefox-64.0-build1")
        .execute()
        .fetchall()
    )
    for sc in asset_scs:
        signoffs = (
            dbo.release_assets.scheduled_changes.signoffs.t.select()
            .where(dbo.release_assets.scheduled_changes.signoffs.sc_id == sc["sc_id"])
            .execute()
            .fetchall()
        )
        assert len(signoffs) == 1
        assert signoffs[0]["username"] == "bob"
        assert signoffs[0]["role"] == "releng"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_revoke_signoff(api):
    ret = api.delete("/v2/releases/Firefox-67.0-build1/signoff")
    assert ret.status_code == 200, ret.text

    sc_id = (
        dbo.releases_json.scheduled_changes.t.select(dbo.releases_json.scheduled_changes.sc_id)
        .where(dbo.releases_json.scheduled_changes.base_name == "Firefox-67.0-build1")
        .execute()
        .fetchone()["sc_id"]
    )
    base_signoffs = (
        dbo.releases_json.scheduled_changes.signoffs.t.select().where(dbo.releases_json.scheduled_changes.signoffs.sc_id == sc_id).execute().fetchall()
    )
    assert len(base_signoffs) == 0

    asset_scs = (
        dbo.release_assets.scheduled_changes.t.select(dbo.release_assets.scheduled_changes.sc_id)
        .where(dbo.release_assets.scheduled_changes.base_name == "Firefox-67.0-build1")
        .execute()
        .fetchall()
    )
    for sc in asset_scs:
        signoffs = (
            dbo.release_assets.scheduled_changes.signoffs.t.select()
            .where(dbo.release_assets.scheduled_changes.signoffs.sc_id == sc["sc_id"])
            .execute()
            .fetchall()
        )
        assert len(signoffs) == 0


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_enact_changes_missing_signoff(api):
    sc_id = (
        dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-66.0-build1").execute().fetchone().sc_id
    )
    dbo.releases_json.scheduled_changes.signoffs.t.delete().where(dbo.releases_json.scheduled_changes.signoffs.sc_id == sc_id).execute()
    for sc in (
        dbo.release_assets.scheduled_changes.t.select()
        .where(dbo.release_assets.scheduled_changes.base_name == "Firefox-66.0-build1")
        .where(dbo.release_assets.scheduled_changes.base_path == ".platforms.WINNT_x86_64-msvc.locales.en-US")
        .execute()
        .fetchall()
    ):
        dbo.release_assets.scheduled_changes.signoffs.t.delete().where(dbo.release_assets.scheduled_changes.signoffs.sc_id == sc_id).execute()
    ret = api.post("/v2/releases/Firefox-66.0-build1/enact")
    assert ret.status_code == 400
    assert "No Signoffs given" in ret.json()["exception"]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_enact_changes_no_scheduled_changes(api):
    ret = api.post("/v2/releases/Firefox-65.0-build1/enact")
    assert ret.status_code == 404


@pytest.mark.usefixtures("releases_db")
def test_enact_changes_no_permission(api, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    ret = api.post("/v2/releases/Firefox-67.0-build1/enact")
    assert ret.status_code == 403


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_enact_insert(api):
    ret = api.post("/v2/releases/Firefox-64.0-build1/enact")
    assert ret.status_code == 200

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-64.0-build1").execute().fetchone()
    assert base_sc["complete"] is True
    locale_scs = (
        dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.base_name == "Firefox-64.0-build1").execute().fetchall()
    )
    assert all([sc["complete"] for sc in locale_scs])

    base_row = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-64.0-build1").execute().fetchone()
    assert base_row is not None
    locale_rows = dbo.release_assets.t.select().where(dbo.release_assets.name == "Firefox-64.0-build1").execute().fetchall()
    assert len(locale_rows) == 5


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_enact_update(api):
    ret = api.post("/v2/releases/Firefox-66.0-build1/enact")
    assert ret.status_code == 200

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-66.0-build1").execute().fetchone()
    assert base_sc["complete"] is True
    locale_scs = (
        dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.base_name == "Firefox-66.0-build1").execute().fetchall()
    )
    assert all([sc["complete"] for sc in locale_scs])

    base_row = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-66.0-build1").execute().fetchone()
    assert base_row["data"]["hashFunction"] == "sha1024"
    assert base_row["data_version"] == 2
    locale_rows = dbo.release_assets.t.select().where(dbo.release_assets.name == "Firefox-66.0-build1").execute().fetchall()
    for row in locale_rows:
        if row["path"].endswith("en-US"):
            assert row["data"]["buildID"] == "123456789"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_enact_delete(api):
    ret = api.post("/v2/releases/Firefox-67.0-build1/enact")
    assert ret.status_code == 200

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-67.0-build1").execute().fetchone()
    assert base_sc["complete"] is True
    locale_scs = (
        dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.base_name == "Firefox-67.0-build1").execute().fetchall()
    )
    assert all([sc["complete"] for sc in locale_scs])

    base_row = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-67.0-build1").execute().fetchone()
    assert base_row is None
    locale_rows = dbo.release_assets.t.select().where(dbo.release_assets.name == "Firefox-67.0-build1").execute().fetchall()
    assert not any([locale["path"].endswith("en-US") for locale in locale_rows])


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_enact_changes_one_fails_all_revert(api):
    sc_id = (
        dbo.release_assets.scheduled_changes.t.select()
        .where(dbo.release_assets.scheduled_changes.base_name == "Firefox-66.0-build1")
        .where(dbo.release_assets.scheduled_changes.base_path == ".platforms.WINNT_x86_64-msvc.locales.en-US")
        .execute()
        .fetchone()
        .sc_id
    )
    dbo.release_assets.scheduled_changes.signoffs.t.delete().where(dbo.release_assets.scheduled_changes.signoffs.sc_id == sc_id).execute()

    ret = api.post("/v2/releases/Firefox-66.0-build1/enact")
    assert ret.status_code == 400
    assert "No Signoffs given" in ret.json()["exception"]

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.base_name == "Firefox-66.0-build1").execute().fetchone()
    assert base_sc["complete"] is False
    locale_scs = (
        dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.base_name == "Firefox-66.0-build1").execute().fetchall()
    )
    assert all([not sc["complete"] for sc in locale_scs])

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-66.0-build1").execute().fetchone().data
    assert base_blob["hashFunction"] == "sha512"
    locale_blobs = dbo.release_assets.t.select().where(dbo.release_assets.name == "Firefox-66.0-build1").execute().fetchall()
    for blob in locale_blobs:
        if blob["path"].endswith("en-US"):
            assert blob.data["buildID"] != "123456689"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_set_pin_succeeds(api):
    product = "Firefox"
    channel = "release"
    version = "66."
    ret = api.put("v2/releases/Firefox-56.0-build1/pinnable", json={"product": product, "channel": channel, "version": version})
    assert ret.status_code == 200

    mapping = dbo.pinnable_releases.getPinMapping(product=product, channel=channel, version=version)
    assert mapping == "Firefox-56.0-build1"

    ret = api.put("v2/releases/Firefox-66.0-build1/pinnable", json={"product": product, "channel": channel, "version": version})
    assert ret.status_code == 200

    mapping = dbo.pinnable_releases.getPinMapping(product=product, channel=channel, version=version)
    assert mapping == "Firefox-66.0-build1"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_schedule_pin_insert(api):
    product = "Firefox"
    channel = "release"
    version = "66."
    ret = api.put("v2/releases/Firefox-56.0-build1/pinnable", json={"product": product, "channel": channel, "version": version, "when": 1991639932000})
    assert ret.status_code == 200
    assert ret.json()["."]["change_type"] == "insert"

    base_sc = (
        dbo.pinnable_releases.scheduled_changes.t.select().where(dbo.pinnable_releases.scheduled_changes.sc_id == ret.json()["."]["sc_id"]).execute().fetchone()
    )
    base_sc_cond = (
        dbo.pinnable_releases.scheduled_changes.conditions.t.select()
        .where(dbo.pinnable_releases.scheduled_changes.conditions.sc_id == ret.json()["."]["sc_id"])
        .execute()
        .fetchone()
    )
    assert base_sc["base_product"] == product
    assert base_sc["base_channel"] == channel
    assert base_sc["base_version"] == version
    assert base_sc["base_mapping"] == "Firefox-56.0-build1"
    assert base_sc["change_type"] == "insert"
    assert base_sc_cond["when"] == 1991639932000


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_schedule_pin_update(api):
    product = "Firefox"
    channel = "release"
    version = "66."
    ret = api.put("v2/releases/Firefox-56.0-build1/pinnable", json={"product": product, "channel": channel, "version": version})
    assert ret.status_code == 200

    ret = api.put("v2/releases/Firefox-66.0-build1/pinnable", json={"product": product, "channel": channel, "version": version, "when": 1991639932000})
    assert ret.status_code == 200
    assert ret.json()["."]["change_type"] == "update"

    base_sc = (
        dbo.pinnable_releases.scheduled_changes.t.select().where(dbo.pinnable_releases.scheduled_changes.sc_id == ret.json()["."]["sc_id"]).execute().fetchone()
    )
    base_sc_cond = (
        dbo.pinnable_releases.scheduled_changes.conditions.t.select()
        .where(dbo.pinnable_releases.scheduled_changes.conditions.sc_id == ret.json()["."]["sc_id"])
        .execute()
        .fetchone()
    )
    assert base_sc["base_product"] == product
    assert base_sc["base_channel"] == channel
    assert base_sc["base_version"] == version
    assert base_sc["base_mapping"] == "Firefox-66.0-build1"
    assert base_sc["change_type"] == "update"
    assert base_sc_cond["when"] == 1991639932000


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_set_older_pin_does_nothing(api):
    product = "Firefox"
    channel = "release"
    ret = api.put("v2/releases/Firefox-66.0-build1/pinnable", json={"product": product, "channel": channel, "version": "66."})
    assert ret.status_code == 200
    ret = api.put("v2/releases/Firefox-66.0-build1/pinnable", json={"product": product, "channel": channel, "version": "66.1."})
    assert ret.status_code == 200
    mapping = dbo.pinnable_releases.getPinMapping(product=product, channel=channel, version="66.")
    assert mapping == "Firefox-66.0-build1"
    mapping = dbo.pinnable_releases.getPinMapping(product=product, channel=channel, version="66.1.")
    assert mapping == "Firefox-66.0-build1"

    # Attempting to set the '66.' pin to an earlier version should succeed but not result in a pinning change
    ret = api.put("v2/releases/Firefox-56.0-build1/pinnable", json={"product": product, "channel": channel, "version": "66."})
    assert ret.status_code == 200
    assert ret.json() == {"pin_not_set": True, "reason": "existing_pin_is_newer"}
    mapping = dbo.pinnable_releases.getPinMapping(product=product, channel=channel, version="66.")
    assert mapping == "Firefox-66.0-build1"

    # Attempting to set a different minor pin ('66.0.' instead of '66.1.') should work normally.
    ret = api.put("v2/releases/Firefox-56.0-build1/pinnable", json={"product": product, "channel": channel, "version": "66.0."})
    assert ret.status_code == 200
    mapping = dbo.pinnable_releases.getPinMapping(product=product, channel=channel, version="66.0.")
    assert mapping == "Firefox-56.0-build1"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
@pytest.mark.parametrize(
    "method,endpoint,metric",
    (
        pytest.param(
            "GET",
            "/v2/releases",
            "endpoint_releases_v2_get_all",
            id="get_all",
        ),
        pytest.param(
            "GET",
            "/v2/releases/Firefox-33.0-build1",
            "endpoint_releases_v2_get",
            id="get",
        ),
        pytest.param(
            "POST",
            "/v2/releases/Firefox-33.0-build1",
            "endpoint_releases_v2_update",
            id="update",
        ),
        pytest.param(
            "PUT",
            "/v2/releases/Firefox-33.0-build1",
            "endpoint_releases_v2_ensure",
            id="ensure",
        ),
        pytest.param(
            "DELETE",
            "/v2/releases/Firefox-33.0-build1",
            "endpoint_releases_v2_delete",
            id="delete",
        ),
    ),
)
def test_statsd(api, method, endpoint, metric):
    """Test that some of the releases v2 endpoints add stats correctly.
    Timings are handled centrally, so it's not worth the trouble to test
    every single one. Requests don't need to succeed for these to pass;
    they just need to be routable."""
    with mock.patch("auslib.web.admin.base.statsd.timer") as mocked_timer:
        api.request(method, endpoint)
        assert mocked_timer.call_count == 1
        mocked_timer.assert_has_calls([mock.call(metric)])


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_statsd_gcs_creation(api, firefox_62_0_build1):
    with mock.patch("auslib.db.statsd.timer") as mocked_timer:
        ret = api.put("/v2/releases/Firefox-62.0-build1", json={"blob": firefox_62_0_build1, "product": "Firefox"})
        assert ret.status_code == 200, ret.data
        # 20 locales to upload for + top level
        # a creation uploads twice
        # 21 * 2 = 42
        # plus 1 for the overall request
        assert mocked_timer.call_count == 43
        mocked_timer.assert_has_calls([mock.call("async_gcs_upload"), mock.call("endpoint_releases_v2_ensure")], any_order=True)


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_statsd_gcs_update(api):
    with mock.patch("auslib.db.statsd.timer") as mocked_timer:
        blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "22222222222"}}}}}

        old_data_versions = versions_dict()
        old_data_versions["."] = 1
        assert old_data_versions["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]
        ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": blob, "old_data_versions": old_data_versions})
        assert ret.status_code == 200, ret.data
        # one call for top level modification, one for the changed locale, one for overall request
        assert mocked_timer.call_count == 3
        mocked_timer.assert_has_calls([mock.call("async_gcs_upload"), mock.call("endpoint_releases_v2_update")], any_order=True)


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_statsd_gcs_delete(api):
    with mock.patch("auslib.db.statsd.timer") as mocked_timer:
        ret = api.delete("/v2/releases/Firefox-65.0-build1")
        assert ret.status_code == 200, ret.data

        # one call for top level, one call for each locale, one for overall request
        assert mocked_timer.call_count == 22
        mocked_timer.assert_has_calls([mock.call("async_gcs_upload"), mock.call("endpoint_releases_v2_delete")], any_order=True)
