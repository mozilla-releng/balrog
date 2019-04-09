# auslib is a library that contains two different webapps. Both of them share
# a single database model, and some code (release blobs, for example), need
# to have access to the database to do their jobs. Because of this, it's
# convenient to have the database object accessible in single place for both
# apps, which is why the "dbo" variable below exists. This DbWrapper class
# exists solely to defer the AUSDatabase object import to work around circular
# dependency issues that would occur if it were imported at parse time instead
# of runtime.


class DbWrapper(object):
    def __init__(self):
        self.db = None

    def setDb(self, dburi):
        from auslib.db import AUSDatabase

        self.db = AUSDatabase(dburi)

    def __getattr__(self, name):
        if not self.db:
            raise RuntimeError("No database configured")
        return getattr(self.db, name)


dbo = DbWrapper()

# Similar to the above, we have a complication around having two separate
# applications existing in the same library. This cache class is a simple
# wrapper that does nothing if caching is disabled, and uses a 3rd party
# caching library if it is enabled.
from auslib.util.cache import MaybeCacher

cache = MaybeCacher()
