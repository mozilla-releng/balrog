import pytest

from auslib.global_state import dbo


@pytest.fixture(scope='session')
def db_schema():
    """This fixture creates a fresh in-memory database, and then runs all the
    schema migration logic, and returns the schema metadata of the final DB
    state. It runs once per test session.
    """
    dbo.setDb('sqlite:///:memory:')
    dbo.create()
    return dbo.metadata


@pytest.fixture(scope='class')
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
