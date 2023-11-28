import json
from copy import deepcopy
from pathlib import Path

import pytest
from hypothesis import settings

from auslib.global_state import dbo
from auslib.util.data_structures import deep_dict, infinite_defaultdict

# Disable hypothesis testing deadlines
settings.register_profile("ci", deadline=None)
settings.load_profile("ci")


@pytest.fixture(scope="session")
def db_schema():
    """This fixture creates a fresh in-memory database, and then runs all the
    schema migration logic, and returns the schema metadata of the final DB
    state. It runs once per test session.
    """
    dbo.setDb("sqlite:///:memory:")
    dbo.create()
    return dbo.metadata


@pytest.fixture(scope="class")
def current_db_schema(request, db_schema):
    """This fixture is meant to be used as a class decorator, and adds a
    `metadata` attribute to the class. In the class' initialization (e.g. in
    the setUp() method), the metadata can be used to quickly create the table
    scheams without having to run all the migration logic. For example:

    @pytest.mark.usefixtures('current_db_schema')
    class TestFoo(unittest.TestCase):
        def setUp(self):
            self.db = AUSDatabase(self.dburi)
            self.metadata.create_all(self.db.engine)
    """
    request.cls.metadata = db_schema


@pytest.fixture(scope="session")
def insert_release():
    def do_insert_release(release_data, product, history=True):
        name = release_data["name"]
        base = deep_dict(4, {})
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
                        dbo.release_assets.t.insert().execute(name=name, path=path, data=ldata, data_version=1)
                        if history:
                            dbo.release_assets.history.bucket.blobs[f"{name}-{path}/None-1-bob.json"] = ""
                            dbo.release_assets.history.bucket.blobs[f"{name}-{path}/1-2-bob.json"] = ldata

        dbo.releases_json.t.insert().execute(
            name=name,
            product=product,
            data=base,
            data_version=1,
        )
        if history:
            dbo.releases_json.history.bucket.blobs[f"{name}/None-1-bob.json"] = ""
            dbo.releases_json.history.bucket.blobs[f"{name}/1-2-bob.json"] = release_data

    return do_insert_release


@pytest.fixture(scope="session")
def insert_release_sc():
    def do_insert_release_sc(release_data, product, change_type="update", signoff_user=None, signoff_role=None):
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
                        if lname != "en-US":
                            continue

                        path = f".platforms.{pname}.locales.{lname}"
                        data = {}
                        if change_type != "delete":
                            data["base_data"] = deepcopy(ldata)
                            data["base_data"]["buildID"] = "123456789"
                        ret = dbo.release_assets.scheduled_changes.t.insert().execute(
                            base_name=release_data["name"],
                            base_path=path,
                            base_data_version=1,
                            data_version=1,
                            scheduled_by="bob",
                            change_type=change_type,
                            **data,
                        )
                        dbo.release_assets.scheduled_changes.conditions.t.insert().execute(
                            sc_id=ret.inserted_primary_key[0], when=2222222222000, data_version=1
                        )
                        if signoff_user and signoff_role:
                            dbo.release_assets.scheduled_changes.signoffs.t.insert().execute(
                                sc_id=ret.inserted_primary_key[0], username=signoff_user, role=signoff_role
                            )

        data = {}
        if change_type != "delete":
            data["base_data"] = deepcopy(base)
            data["base_data"]["hashFunction"] = "sha1024"
        ret = dbo.releases_json.scheduled_changes.t.insert().execute(
            base_name=release_data["name"], base_product=product, base_data_version=1, data_version=1, scheduled_by="bob", change_type=change_type, **data
        )
        dbo.releases_json.scheduled_changes.conditions.t.insert().execute(sc_id=ret.inserted_primary_key[0], when=2222222222000, data_version=1)
        if signoff_user and signoff_role:
            dbo.releases_json.scheduled_changes.signoffs.t.insert().execute(sc_id=ret.inserted_primary_key[0], username=signoff_user, role=signoff_role)

    return do_insert_release_sc


@pytest.fixture(scope="session")
def firefox_54_0_1_build1():
    with open(Path(__file__).parent / "data/Firefox-54.0.1-build1.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def firefox_56_0_build1():
    with open(Path(__file__).parent / "data/Firefox-56.0-build1.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def firefox_60_0b3_build1():
    with open(Path(__file__).parent / "data/Firefox-60.0b3-build1.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def firefox_62_0_build1():
    with open(Path(__file__).parent / "data/Firefox-62.0-build1.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def firefox_64_0_build1():
    with open(Path(__file__).parent / "data/Firefox-64.0-build1.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def firefox_65_0_build1():
    with open(Path(__file__).parent / "data/Firefox-65.0-build1.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def firefox_66_0_build1():
    with open(Path(__file__).parent / "data/Firefox-66.0-build1.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def firefox_67_0_build1():
    with open(Path(__file__).parent / "data/Firefox-67.0-build1.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def firefox_100_0_build1():
    with open(Path(__file__).parent / "data/Firefox-100.0-build1.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def cdm_16():
    with open(Path(__file__).parent / "data/CDM-16.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def cdm_17():
    with open(Path(__file__).parent / "data/CDM-17.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def superblob_e8f4a19():
    with open(Path(__file__).parent / "data/Superblob-e8f4a19cfd695bf0eb66a2115313c31cc23a2369c0dc7b736d2f66d9075d7c66.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def hotfix_bug_1548973_1_1_4():
    with open(Path(__file__).parent / "data/hotfix-bug-1548973@mozilla.org-1.1.4.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def timecop_1_0():
    with open(Path(__file__).parent / "data/timecop@mozilla.com-1.0.json") as f:
        return json.load(f)
