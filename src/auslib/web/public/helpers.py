import logging
from functools import wraps

from flask import current_app as app

from auslib.AUS import AUS
from auslib.global_state import cache, dbo
from auslib.util.autograph import make_hash, sign_hash

log = logging.getLogger(__name__)


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


def get_content_signature_headers(content):
    headers = {}
    if app.config.get("AUTOGRAPH_URL"):
        hash_ = make_hash(content)

        def sign():
            return sign_hash(
                app.config["AUTOGRAPH_URL"], app.config["AUTOGRAPH_KEYID"], app.config["AUTOGRAPH_USERNAME"], app.config["AUTOGRAPH_PASSWORD"], hash_
            )

        signature, x5u = cache.get("content_signatures", hash_, sign)
        headers = {"Content-Signature": f"x5u={x5u}; p384ecdsa={signature}"}
        log.debug("Added header: %s" % headers)
    return headers


AUS = AUS()
