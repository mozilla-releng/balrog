from copy import deepcopy

import pytest

from auslib.global_state import dbo
from auslib.util.data_structures import infinite_defaultdict

from ...fakes import FakeGCSHistory


def insert_release(release_data, product):
    base = infinite_defaultdict()
    for key in release_data:
        if key != "platforms":
            base[key] = release_data[key]
            continue

        for pname, pdata in release_data[key].items():
            for pkey in pdata:
                if pkey != "locales":
                    base[key][pname][pkey] = pdata[pkey]
                    continue

                for lname, ldata in pdata[pkey].items():
                    path = f".platforms.{pname}.locales.{lname}"
                    dbo.release_assets.t.insert().execute(name=release_data["name"], path=path, data=ldata, data_version=1)
                    dbo.release_assets.history.bucket.blobs[f"{release_data['name']}-{path}/None-1-bob.json"] = ""
                    dbo.release_assets.history.bucket.blobs[f"{release_data['name']}-{path}/1-2-bob.json"] = ldata

    dbo.releases_json.t.insert().execute(
        name=release_data["name"], product=product, data=base, data_version=1,
    )
    dbo.releases_json.history.bucket.blobs[f"{release_data['name']}/None-1-bob.json"] = ""
    dbo.releases_json.history.bucket.blobs[f"{release_data['name']}/1-2-bob.json"] = release_data


def get_release_history(name):
    return [(k, v) for k, v in dbo.releases_json.history.bucket.blobs.items() if k.startswith(f"{name}/")]


def get_release_assets_history(name, path):
    return [(k, v) for k, v in dbo.release_assets.history.bucket.blobs.items() if k.startswith(f"{name}-{path}/")]


# TODO: It would be great if we could session scope this, and have
# the database revert itself after every test (rather than rebuilding
# more or less from scratch)
@pytest.fixture(scope="function")
def releases_db(db_schema, firefox_56_0_build1, firefox_60_0b3_build1, cdm_17):
    dbo.setDb("sqlite:///:memory:", releases_history_buckets={"*": "fake"}, releases_history_class=FakeGCSHistory)
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
    dbo.rules.t.insert().execute(rule_id=3, priority=100, channel="beta", mapping="CDM-17", update_type="minor", data_version=1)
    insert_release(firefox_56_0_build1, "Firefox")
    insert_release(firefox_60_0b3_build1, "Firefox")
    insert_release(cdm_17, "CDM")


@pytest.mark.usefixtures("releases_db")
def test_get_releases(api):
    ret = api.get("/v2/releases")
    assert ret.status_code == 200, ret.data
    expected = {
        "releases": [
            {
                "name": "Firefox-56.0-build1",
                "product": "Firefox",
                "data_version": 1,
                "read_only": False,
                "rule_info": {"1": {"product": "Firefox", "channel": "release"}},
            },
            {
                "name": "Firefox-60.0b3-build1",
                "product": "Firefox",
                "data_version": 1,
                "read_only": False,
                "rule_info": {"2": {"product": "Firefox", "channel": "beta"}},
            },
            {"name": "CDM-17", "product": "CDM", "data_version": 1, "read_only": False, "rule_info": {"3": {"product": None, "channel": "beta"}}},
        ]
    }
    assert ret.json == expected


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_fails_when_signoff_required(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["detailsUrl"] = "https://newurl"
    firefox_56_0_build1["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]["buildID"] = "9999999999999"

    old_data_versions = infinite_defaultdict()
    old_data_versions["."] = 1
    for pname, pdata in firefox_56_0_build1["platforms"].items():
        for lname in pdata.get("locales", {}):
            old_data_versions["platforms"][pname]["locales"][lname] = 1

    ret = api.put("/v2/releases/Firefox-56.0-build1", json={"blob": firefox_56_0_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 400


@pytest.mark.usefixtures("releases_db")
def test_overwrite_fails_without_permission(api, firefox_60_0b3_build1, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    firefox_60_0b3_build1["detailsUrl"] = "https://newurl"
    firefox_60_0b3_build1["platforms"]["Darwin_x86_64-gcc3-u-i386-x86_64"]["locales"]["de"]["buildID"] = "9999999999999"

    old_data_versions = infinite_defaultdict()
    old_data_versions["."] = 1
    for pname, pdata in firefox_60_0b3_build1["platforms"].items():
        for lname in pdata.get("locales", {}):
            old_data_versions["platforms"][pname]["locales"][lname] = 1

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 403, ret.data


@pytest.mark.usefixtures("releases_db")
def test_overwrite_fails_without_permission_new_release(api, firefox_62_0_build1, mock_verified_userinfo):
    mock_verified_userinfo("notbob")

    ret = api.put("/v2/releases/Firefox-62.0-build1", json={"blob": firefox_62_0_build1, "product": "Firefox"})
    assert ret.status_code == 403, ret.data


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_fails_for_invalid_release(api):
    # Only submit a portion of what's needed to have a valid blob
    data = {"platforms": {"Linux_x86_64-gcc3": {"platforms": {"de": {"appVersion": "65.0", "buildID": "9090909090990", "displayVersion": "65.0"}}}}}

    ret = api.put("/v2/releases/Firefox-65.0-build1", json={"blob": data})
    assert ret.status_code == 400, ret.data


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_fails_for_readonly_release(api, firefox_60_0b3_build1):
    dbo.releases_json.t.update(values={"read_only": True}).where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute()

    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
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

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 400, ret.data
    assert "Cannot overwrite" in ret.json["exception"]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_succeeds(api, firefox_60_0b3_build1):
    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    firefox_60_0b3_build1["detailsUrl"] = "https://newurl"
    firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"

    old_data_versions = infinite_defaultdict()
    old_data_versions["."] = 1
    old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"] = 1
    new_data_versions = infinite_defaultdict()
    new_data_versions["."] = 2
    new_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"] = 2

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions

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
def test_overwrite_succeeds_for_new_release(api, firefox_62_0_build1):
    new_data_versions = infinite_defaultdict()
    new_data_versions["."] = 1
    for pname, pdata in firefox_62_0_build1["platforms"].items():
        for lname in pdata.get("locales", {}):
            new_data_versions["platforms"][pname]["locales"][lname] = 1

    ret = api.put("/v2/releases/Firefox-62.0-build1", json={"blob": firefox_62_0_build1, "product": "Firefox"})
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions

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
def test_overwrite_removes_locales(api, firefox_60_0b3_build1):
    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    del firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]
    del firefox_60_0b3_build1["platforms"]["Linux_x86-gcc3"]["locales"]["af"]

    old_data_versions = infinite_defaultdict()
    old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"] = 1
    old_data_versions["platforms"]["Linux_x86-gcc3"]["locales"]["af"] = 1

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.data
    assert ret.json == {}

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
def test_overwrite_remove_add_and_update_locales(api, firefox_60_0b3_build1):
    firefox_60_0b3_build1 = deepcopy(firefox_60_0b3_build1)
    newde = firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]
    del firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]
    firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["af"]["buildID"] = "7777777777"

    old_data_versions = infinite_defaultdict()
    new_data_versions = infinite_defaultdict()
    old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["af"] = 1
    old_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"] = 1
    new_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["af"] = 2
    new_data_versions["platforms"]["Linux_x86_64-gcc3"]["locales"]["newde"] = 1

    firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["newde"] = newde

    ret = api.put("/v2/releases/Firefox-60.0b3-build1", json={"blob": firefox_60_0b3_build1, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions

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
def test_overwrite_succeeds_for_nonsplit_release(api, cdm_17):
    cdm_17 = deepcopy(cdm_17)
    cdm_17["vendors"]["gmp-eme-adobe"]["platforms"]["WINNT_x86-msvc"]["filesize"] = 5555555555

    ret = api.put("/v2/releases/CDM-17", json={"blob": cdm_17, "product": "CDM", "old_data_versions": {".": 1}})
    assert ret.status_code == 200, ret.data
    assert ret.json == {".": 2}

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "CDM-17").execute().fetchone().data
    assert base_blob == cdm_17
    history = get_release_history("CDM-17")
    assert len(history) == 3
    # Check to make sure "changed_by" was set
    assert "-bob.json" in history[2][0]


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_fails_when_release_doesnt_exist(api):
    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "999999999999999"}}}}}

    old_data_versions = {".": 1, "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": 1}}}}

    ret = api.post("/v2/releases/Firefox-58.0-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 404


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_fails_when_signoff_required(api):
    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "999999999999999"}}}}}

    old_data_versions = {".": 1, "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": 1}}}}

    ret = api.post("/v2/releases/Firefox-56.0-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 400


@pytest.mark.usefixtures("releases_db")
def test_update_fails_without_permission(api, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    blob = {"detailsUrl": "https://newurl", "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": {"buildID": "999999999999999"}}}}}

    old_data_versions = {".": 1, "platforms": {"Darwin_x86_64-gcc3-u-i386-x86_64": {"locales": {"de": 1}}}}

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": blob, "old_data_versions": old_data_versions})
    assert ret.status_code == 403, ret.data


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_fails_for_invalid_release_base(api):
    # Add an invalid parameter to the blob
    data = {"foo": "foo"}
    old_data_versions = {".": 1}

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": data, "old_data_versions": old_data_versions})
    assert ret.status_code == 400, ret.data
    assert ret.json["detail"] == "Invalid Blob", ret.json


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_fails_for_invalid_release_locale(api):
    # add an invalid key to a locale section
    data = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"de": {"foo": "foo"}}}}}
    old_data_versions = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"de": 1}}}}

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": data, "old_data_versions": old_data_versions})
    assert ret.status_code == 400, ret.data
    assert ret.json["detail"] == "Invalid Blob", ret.json


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_fails_for_readonly_release(api, firefox_60_0b3_build1):
    dbo.releases_json.t.update(values={"read_only": True}).where(dbo.releases_json.name == "Firefox-60.0b3-build1").execute()

    data = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"de": {"buildID": "333333333333"}}}}}
    old_data_versions = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"de": 1}}}}

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": data, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 400, ret.data
    assert "Cannot update" in ret.json["exception"]


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
def test_update_add_and_update_locales(api, firefox_60_0b3_build1):
    blob = {
        "platforms": {
            "Linux_x86_64-gcc3": {
                "locales": {"af": {"buildID": "7777777777"}, "newde": firefox_60_0b3_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["de"]}
            }
        }
    }

    old_data_versions = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"af": 1}}}}
    new_data_versions = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"af": 2, "newde": 1}}}}

    ret = api.post("/v2/releases/Firefox-60.0b3-build1", json={"blob": blob, "product": "Firefox", "old_data_versions": old_data_versions})
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions

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
def test_update_succeeds_for_nonsplit_release(api, cdm_17):
    cdm_17 = deepcopy(cdm_17)
    blob = {"vendors": {"gmp-eme-adobe": {"platforms": {"WINNT_x86-msvc": {"filesize": 5555555555}}}}}
    cdm_17["vendors"]["gmp-eme-adobe"]["platforms"]["WINNT_x86-msvc"]["filesize"] = 5555555555

    ret = api.post("/v2/releases/CDM-17", json={"blob": blob, "old_data_versions": {".": 1}})
    assert ret.status_code == 200, ret.data
    assert ret.json == {".": 2}

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "CDM-17").execute().fetchone().data
    assert base_blob == cdm_17
    history = get_release_history("CDM-17")
    assert len(history) == 3
    # Check to make sure "changed_by" was set
    assert "-bob.json" in history[2][0]


@pytest.mark.usefixtures("releases_db")
def test_overwrite_add_scheduled_change_fails_without_permission(api, firefox_56_0_build1, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["displayVersion"] = "sixty five dot oh"

    old_data_versions = {".": 1}

    ret = api.put(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": firefox_56_0_build1, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1681639932000},
    )
    assert ret.status_code == 403, ret.data


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_add_scheduled_change_base_only(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["displayVersion"] = "sixty five dot oh"

    old_data_versions = {".": 1}
    new_data_versions = {".": {"sc_id": 1, "data_version": 1, "change_type": "update"}}

    ret = api.put(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": firefox_56_0_build1, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1681639932000},
    )
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions, ret.json

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-56.0-build1").execute().fetchone()["data"]
    assert base_blob["displayVersion"] == "56.0"

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.sc_id == 1).execute().fetchone()
    base_sc_cond = (
        dbo.releases_json.scheduled_changes.conditions.t.select().where(dbo.releases_json.scheduled_changes.conditions.sc_id == 1).execute().fetchone()
    )
    base_sc_signoffs = (
        dbo.releases_json.scheduled_changes.signoffs.t.select().where(dbo.releases_json.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
    )
    assert base_sc["scheduled_by"] == "bob"
    assert base_sc["complete"] is False
    assert base_sc["data_version"] == 1
    assert base_sc["base_name"] == "Firefox-56.0-build1"
    assert base_sc["base_data"]["displayVersion"] == "sixty five dot oh"
    assert "locales" not in base_sc["base_data"]["platforms"]["Linux_x86_64-gcc3"]
    assert base_sc["base_product"] == "Firefox"
    assert base_sc["base_data_version"] == 1
    assert base_sc_cond["when"] == 1681639932000
    assert len(base_sc_signoffs) == 1
    assert base_sc_signoffs[0]["username"] == "bob"
    assert base_sc_signoffs[0]["role"] == "releng"

    locale_sc = (
        dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.base_name == "Firefox-56.0-build1").execute().fetchall()
    )
    assert len(locale_sc) == 0


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_add_scheduled_change_locale_only(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"

    old_data_versions = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": 1}}}}
    new_data_versions = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": {"sc_id": 1, "data_version": 1, "change_type": "update"}}}}}

    ret = api.put(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": firefox_56_0_build1, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1681639932000},
    )
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions, ret.json

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.sc_id == 1).execute().fetchall()
    assert len(base_sc) == 0

    locale_sc = dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.sc_id == 1).execute().fetchone()
    locale_sc_cond = (
        dbo.release_assets.scheduled_changes.conditions.t.select().where(dbo.release_assets.scheduled_changes.conditions.sc_id == 1).execute().fetchone()
    )
    locale_sc_signoffs = (
        dbo.release_assets.scheduled_changes.signoffs.t.select().where(dbo.release_assets.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
    )
    assert locale_sc["scheduled_by"] == "bob"
    assert locale_sc["complete"] is False
    assert locale_sc["data_version"] == 1
    assert locale_sc["base_name"] == "Firefox-56.0-build1"
    assert locale_sc["base_path"] == ".platforms.Linux_x86_64-gcc3.locales.en-US"
    assert locale_sc["base_data"] == firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    assert locale_sc["base_data_version"] == 1
    assert locale_sc_cond["when"] == 1681639932000
    assert len(locale_sc_signoffs) == 1
    assert locale_sc_signoffs[0]["username"] == "bob"
    assert locale_sc_signoffs[0]["role"] == "releng"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_overwrite_add_scheduled_change_base_and_locale(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["displayVersion"] = "fifty six dot oh"
    firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"

    old_data_versions = {".": 1, "platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": 1}}}}
    new_data_versions = {
        ".": {"sc_id": 1, "data_version": 1, "change_type": "update"},
        "platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": {"sc_id": 1, "data_version": 1, "change_type": "update"}}}},
    }

    ret = api.put(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": firefox_56_0_build1, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1681639932000},
    )
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions, ret.json

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-56.0-build1").execute().fetchone()["data"]
    assert base_blob["displayVersion"] == "56.0"

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.sc_id == 1).execute().fetchone()
    base_sc_cond = (
        dbo.releases_json.scheduled_changes.conditions.t.select().where(dbo.releases_json.scheduled_changes.conditions.sc_id == 1).execute().fetchone()
    )
    base_sc_signoffs = (
        dbo.releases_json.scheduled_changes.signoffs.t.select().where(dbo.releases_json.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
    )
    assert base_sc["scheduled_by"] == "bob"
    assert base_sc["complete"] is False
    assert base_sc["data_version"] == 1
    assert base_sc["base_name"] == "Firefox-56.0-build1"
    assert base_sc["base_data"]["displayVersion"] == "fifty six dot oh"
    assert "locales" not in base_sc["base_data"]["platforms"]["Linux_x86_64-gcc3"]
    assert base_sc["base_product"] == "Firefox"
    assert base_sc["base_data_version"] == 1
    assert base_sc_cond["when"] == 1681639932000
    assert len(base_sc_signoffs) == 1
    assert base_sc_signoffs[0]["username"] == "bob"
    assert base_sc_signoffs[0]["role"] == "releng"

    locale_sc = dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.sc_id == 1).execute().fetchone()
    locale_sc_cond = (
        dbo.release_assets.scheduled_changes.conditions.t.select().where(dbo.release_assets.scheduled_changes.conditions.sc_id == 1).execute().fetchone()
    )
    locale_sc_signoffs = (
        dbo.release_assets.scheduled_changes.signoffs.t.select().where(dbo.release_assets.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
    )
    assert locale_sc["scheduled_by"] == "bob"
    assert locale_sc["complete"] is False
    assert locale_sc["data_version"] == 1
    assert locale_sc["base_name"] == "Firefox-56.0-build1"
    assert locale_sc["base_path"] == ".platforms.Linux_x86_64-gcc3.locales.en-US"
    assert locale_sc["base_data"] == firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    assert locale_sc["base_data_version"] == 1
    assert locale_sc_cond["when"] == 1681639932000
    assert len(locale_sc_signoffs) == 1
    assert locale_sc_signoffs[0]["username"] == "bob"
    assert locale_sc_signoffs[0]["role"] == "releng"


@pytest.mark.usefixtures("releases_db")
def test_update_add_scheduled_change_fails_without_permission(api, firefox_56_0_build1, mock_verified_userinfo):
    mock_verified_userinfo("notbob")
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["displayVersion"] = "fifty six dot oh"

    old_data_versions = {".": 1}

    ret = api.post(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": {"displayVersion": "fifty six dot oh"}, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1681639932000},
    )
    assert ret.status_code == 403, ret.data


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_add_scheduled_change_base_only(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["displayVersion"] = "fifty six dot oh"

    old_data_versions = {".": 1}
    new_data_versions = {".": {"sc_id": 1, "data_version": 1, "change_type": "update"}}

    ret = api.post(
        "/v2/releases/Firefox-56.0-build1",
        json={"blob": {"displayVersion": "fifty six dot oh"}, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1681639932000},
    )
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions, ret.json

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-56.0-build1").execute().fetchone()["data"]
    assert base_blob["displayVersion"] == "56.0"

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.sc_id == 1).execute().fetchone()
    base_sc_cond = (
        dbo.releases_json.scheduled_changes.conditions.t.select().where(dbo.releases_json.scheduled_changes.conditions.sc_id == 1).execute().fetchone()
    )
    base_sc_signoffs = (
        dbo.releases_json.scheduled_changes.signoffs.t.select().where(dbo.releases_json.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
    )
    assert base_sc["scheduled_by"] == "bob"
    assert base_sc["complete"] is False
    assert base_sc["data_version"] == 1
    assert base_sc["base_name"] == "Firefox-56.0-build1"
    assert base_sc["base_data"]["displayVersion"] == "fifty six dot oh"
    assert "locales" not in base_sc["base_data"]["platforms"]["Linux_x86_64-gcc3"]
    assert base_sc["base_product"] == "Firefox"
    assert base_sc["base_data_version"] == 1
    assert base_sc_cond["when"] == 1681639932000
    assert len(base_sc_signoffs) == 1
    assert base_sc_signoffs[0]["username"] == "bob"
    assert base_sc_signoffs[0]["role"] == "releng"

    locale_sc = (
        dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.base_name == "Firefox-56.0-build1").execute().fetchall()
    )
    assert len(locale_sc) == 0


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_add_scheduled_change_locale_only(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"
    blob = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": {"buildID": "9999999999999"}}}}}

    old_data_versions = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": 1}}}}
    new_data_versions = {"platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": {"sc_id": 1, "data_version": 1, "change_type": "update"}}}}}

    ret = api.post(
        "/v2/releases/Firefox-56.0-build1", json={"blob": blob, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1681639932000},
    )
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions, ret.json

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.sc_id == 1).execute().fetchall()
    assert len(base_sc) == 0

    locale_sc = dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.sc_id == 1).execute().fetchone()
    locale_sc_cond = (
        dbo.release_assets.scheduled_changes.conditions.t.select().where(dbo.release_assets.scheduled_changes.conditions.sc_id == 1).execute().fetchone()
    )
    locale_sc_signoffs = (
        dbo.release_assets.scheduled_changes.signoffs.t.select().where(dbo.release_assets.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
    )
    assert locale_sc["scheduled_by"] == "bob"
    assert locale_sc["complete"] is False
    assert locale_sc["data_version"] == 1
    assert locale_sc["base_name"] == "Firefox-56.0-build1"
    assert locale_sc["base_path"] == ".platforms.Linux_x86_64-gcc3.locales.en-US"
    assert locale_sc["base_data"] == firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    assert locale_sc["base_data_version"] == 1
    assert locale_sc_cond["when"] == 1681639932000
    assert len(locale_sc_signoffs) == 1
    assert locale_sc_signoffs[0]["username"] == "bob"
    assert locale_sc_signoffs[0]["role"] == "releng"


@pytest.mark.usefixtures("releases_db", "mock_verified_userinfo")
def test_update_add_scheduled_change_base_and_locale(api, firefox_56_0_build1):
    firefox_56_0_build1 = deepcopy(firefox_56_0_build1)
    firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]["buildID"] = "9999999999999"
    blob = {"displayVersion": "fifty six dot oh", "platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": {"buildID": "9999999999999"}}}}}

    old_data_versions = {".": 1, "platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": 1}}}}
    new_data_versions = {
        ".": {"sc_id": 1, "data_version": 1, "change_type": "update"},
        "platforms": {"Linux_x86_64-gcc3": {"locales": {"en-US": {"sc_id": 1, "data_version": 1, "change_type": "update"}}}},
    }

    ret = api.post(
        "/v2/releases/Firefox-56.0-build1", json={"blob": blob, "product": "Firefox", "old_data_versions": old_data_versions, "when": 1681639932000},
    )
    assert ret.status_code == 200, ret.data
    assert ret.json == new_data_versions, ret.json

    base_blob = dbo.releases_json.t.select().where(dbo.releases_json.name == "Firefox-56.0-build1").execute().fetchone()["data"]
    assert base_blob["displayVersion"] == "56.0"

    base_sc = dbo.releases_json.scheduled_changes.t.select().where(dbo.releases_json.scheduled_changes.sc_id == 1).execute().fetchone()
    base_sc_cond = (
        dbo.releases_json.scheduled_changes.conditions.t.select().where(dbo.releases_json.scheduled_changes.conditions.sc_id == 1).execute().fetchone()
    )
    base_sc_signoffs = (
        dbo.releases_json.scheduled_changes.signoffs.t.select().where(dbo.releases_json.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
    )
    assert base_sc["scheduled_by"] == "bob"
    assert base_sc["complete"] is False
    assert base_sc["data_version"] == 1
    assert base_sc["base_name"] == "Firefox-56.0-build1"
    assert base_sc["base_data"]["displayVersion"] == "fifty six dot oh"
    assert "locales" not in base_sc["base_data"]["platforms"]["Linux_x86_64-gcc3"]
    assert base_sc["base_product"] == "Firefox"
    assert base_sc["base_data_version"] == 1
    assert base_sc_cond["when"] == 1681639932000
    assert len(base_sc_signoffs) == 1
    assert base_sc_signoffs[0]["username"] == "bob"
    assert base_sc_signoffs[0]["role"] == "releng"

    locale_sc = dbo.release_assets.scheduled_changes.t.select().where(dbo.release_assets.scheduled_changes.sc_id == 1).execute().fetchone()
    locale_sc_cond = (
        dbo.release_assets.scheduled_changes.conditions.t.select().where(dbo.release_assets.scheduled_changes.conditions.sc_id == 1).execute().fetchone()
    )
    locale_sc_signoffs = (
        dbo.release_assets.scheduled_changes.signoffs.t.select().where(dbo.release_assets.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
    )
    assert locale_sc["scheduled_by"] == "bob"
    assert locale_sc["complete"] is False
    assert locale_sc["data_version"] == 1
    assert locale_sc["base_name"] == "Firefox-56.0-build1"
    assert locale_sc["base_path"] == ".platforms.Linux_x86_64-gcc3.locales.en-US"
    assert locale_sc["base_data"] == firefox_56_0_build1["platforms"]["Linux_x86_64-gcc3"]["locales"]["en-US"]
    assert locale_sc["base_data_version"] == 1
    assert locale_sc_cond["when"] == 1681639932000
    assert len(locale_sc_signoffs) == 1
    assert locale_sc_signoffs[0]["username"] == "bob"
    assert locale_sc_signoffs[0]["role"] == "releng"
