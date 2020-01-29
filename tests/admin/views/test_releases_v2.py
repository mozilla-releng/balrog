from copy import deepcopy

import pytest

from auslib.global_state import dbo
from auslib.util.data_structures import infinite_defaultdict


def insert_release(release_data, product):
    release_data = deepcopy(release_data)
    if "platforms" in release_data:
        for pname, pdata in release_data["platforms"].items():
            if "locales" in pdata:
                for lname, ldata in pdata["locales"].items():
                    dbo.release_details.t.insert().execute(name=release_data["name"], path=f".platforms.{pname}.locales.{lname}", data=ldata, data_version=1)
                del release_data["platforms"][pname]["locales"]
    dbo.releases_json.t.insert().execute(
        name=release_data["name"], product=product, data=release_data, data_version=1,
    )


@pytest.fixture(scope="function")
def releases_db(db_schema, firefox_56_0_build1, firefox_60_0b3_build1, cdm_17):
    dbo.setDb("sqlite:///:memory:")
    db_schema.create_all(dbo.engine)
    dbo.permissions.t.insert().execute(permission="admin", username="bob", data_version=1)
    dbo.permissions.user_roles.t.insert().execute(username="bob", role="releng", data_version=1)
    dbo.productRequiredSignoffs.t.insert().execute(product="Firefox", channel="release", role="releng", signoffs_required=1, data_version=1)
    dbo.rules.t.insert().execute(
        rule_id=1, priority=100, product="Firefox", channel="release", mapping="Firefox-56.0-build1", update_type="minor", data_version=1
    )
    dbo.rules.t.insert().execute(
        rule_id=2, priority=100, product="Firefox", channel="beta", mapping="Firefox-60.0b3-build1", update_type="minor", data_version=1
    )
    insert_release(firefox_56_0_build1, "Firefox")
    insert_release(firefox_60_0b3_build1, "Firefox")
    insert_release(cdm_17, "CDM")


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_fails_when_signoff_required(api, firefox_56_0_build1):
    firefox_56_0_build1["detailsUrl"] = "https://newurl"
    firefox_56_0_build1["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]["buildID"] = "9999999999999"

    old_data_versions = infinite_defaultdict()
    old_data_versions["."] = 1
    for pname, pdata in firefox_56_0_build1["platforms"].items():
        for lname in pdata.get("locales", {}):
            old_data_versions["platforms"][pname]["locales"][lname] = 1

    ret = api.put("/v2/releases/Firefox-56.0-build1", json={"blob": firefox_56_0_build1, "old_data_versions": old_data_versions})
    assert ret.status_code == 400


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_succeeds(api, firefox_60_0b3_build1):
    firefox_60_0b3_build1["detailsUrl"] = "https://newurl"
    firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"

    old_data_versions = infinite_defaultdict()
    new_data_versions = infinite_defaultdict()
    old_data_versions["."] = 1
    new_data_versions["."] = 2
    for pname, pdata in firefox_60_0b3_build1["platforms"].items():
        for lname in pdata.get("locales", {}):
            old_data_versions["platforms"][pname]["locales"][lname] = 1
            new_data_versions["platforms"][pname]["locales"][lname] = 2

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute().fetchone().data
    locale_blob = (
        dbo.release_details.t.select()
        .where(dbo.release_details.name == "Firefox-60.0b3-build1")
        .where(dbo.release_details.path == ".platforms.Linux_x86_64-gcc3.locales.en-US")
        .execute()
        .fetchone()
        .data
    )
    assert base_blob["detailsUrl"] == "https://newurl"
    assert locale_blob["buildID"] == "9999999999999"
    assert "locales" not in base_blob["platforms"]["Linux_x86_64-gcc3"]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_removes_locales(api, firefox_60_0b3_build1):
    del firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]
    del firefox_60_0b3_build1["platforms"]["Linux_x86-gcc3"]["locales"]["af"]

    old_data_versions = infinite_defaultdict()
    new_data_versions = infinite_defaultdict()
    old_data_versions["."] = 1
    new_data_versions["."] = 2
    for pname, pdata in firefox_60_0b3_build1["platforms"].items():
        for lname in pdata.get("locales", {}):
            old_data_versions["platforms"][pname]["locales"][lname] = 1
            new_data_versions["platforms"][pname]["locales"][lname] = 2

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute().fetchone().data
    assert base_blob["detailsUrl"] == "https://newurl"
    removed_locales = (
        dbo.release_details.t.select()
        .where(dbo.release_details.name == "Firefox-60.0b3-build1")
        .where(dbo.release_details.path.in_((".platforms.Linux_x86_64-gcc3.locales.de", ".platforms.Linux_x86-gcc3.locales.af")))
        .execute()
        .fetchall()
    )
    assert not removed_locales


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_succeeds_for_nonsplit_release(api, cdm_17):
    cdm_17["vendors"]["gmp-eme-adobe"]["platforms"]["WINNT_x86-msvc"]["filesize"] = 5555555555

    ret = api.put("/v2/releases/CDM-17", json={"blob": cdm_17, "old_data_versions": {".": 1}})
    assert ret.status_code == 200, ret.data
    assert ret.json == {".": 2}

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "CDM-17").execute().fetchone().data
    assert base_blob == cdm_17


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_fails_when_signoff_required(api):
    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "999999999999999"}}}}}

    old_data_versions = {".": 1, "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": 1}}}}

    ret = api.post("/v2/releases/Firefox-56.0-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 400


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_succeeds(api):
    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "22222222222"}}}}}

    old_data_versions = {".": 1, "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": 1}}}}
    new_data_versions = {".": 2, "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": 2}}}}

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute().fetchone().data
    locale_blob = (
        dbo.release_details.t.select()
        .where(dbo.release_details.name == "Firefox-60.0b3-build1")
        .where(dbo.release_details.path == ".platforms.Darwin_x86_64-gcc3-u-i386-x86_64.locales.de")
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


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_succeeds_for_nonsplit_release(api, cdm_17):
    blob = {"vendors": {"gmp-eme-adobe": {"platforms": {"WINNT_x86-msvc": {"filesize": 5555555555}}}}}
    cdm_17["vendors"]["gmp-eme-adobe"]["platforms"]["WINNT_x86-msvc"]["filesize"] = 5555555555

    ret = api.post("/v2/releases/CDM-17", json={"blob": blob, "old_data_versions": {".": 1}})
    assert ret.status_code == 200, ret.data
    assert ret.json == {".": 2}

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "CDM-17").execute().fetchone().data
    assert base_blob == cdm_17
