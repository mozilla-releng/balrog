from functools import wraps

from auslib.AUS import AUS
from auslib.global_state import dbo


def with_transaction(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with dbo.begin() as transaction:
            return f(*args, transaction=transaction, **kwargs)

    return wrapper


def get_aus_metadata_headers(eval_metadata):
    headers = {
        "Rule-ID": eval_metadata["rule_id"],
        "Rule-Data-Version": eval_metadata["rule_data_version"],
    }
    return headers


AUS = AUS()
