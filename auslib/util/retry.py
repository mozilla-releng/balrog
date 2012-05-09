from sqlalchemy.exc import SQLAlchemyError

from mozilla_buildtools.retry import retry as upstream_retry

# The upstream retry actually has arguments of "args" and "kwargs", so we have to
# use different names to collect arguments
def retry(*a, **kw):
    if not kw.get('sleeptime'):
        kw['sleeptime'] = 5
    if not kw.get('retry_exceptions'):
        kw['retry_exceptions'] = (SQLAlchemyError,)
    return upstream_retry(*a, **kw)
