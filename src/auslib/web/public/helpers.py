from functools import wraps

from auslib.AUS import AUS
from auslib.global_state import dbo


def with_transaction(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with dbo.begin() as transaction:
            return f(*args, transaction=transaction, **kwargs)

    return wrapper


AUS = AUS()
