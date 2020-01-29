import json
from pathlib import Path

import pytest
from hypothesis import settings

from auslib.global_state import dbo

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
def firefox_56_0_build1():
    blob = json.load(open(Path(__file__).parent / "data/Firefox-56.0-build1.json"))
    return blob


@pytest.fixture(scope="session")
def firefox_60_0b3_build1():
    blob = json.load(open(Path(__file__).parent / "data/Firefox-60.0b3-build1.json"))
    return blob


@pytest.fixture(scope="session")
def cdm_17():
    blob = json.load(open(Path(__file__).parent / "data/CDM-17.json"))
    return blob
