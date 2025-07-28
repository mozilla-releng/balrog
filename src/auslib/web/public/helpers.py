import logging
from functools import wraps

from flask import current_app as app

from auslib.AUS import AUS
from auslib.global_state import cache, dbo
from auslib.services.releases import get_release_blob
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


def get_content_signature_headers(content, product):
    headers = {}
    if product:
        product += "_"
    if app.config.get("AUTOGRAPH_%sURL" % product):
        hash_ = make_hash(content)

        keyref = "AUTOGRAPH_%sKEYID" % product

        def sign():
            return sign_hash(
                app.config["AUTOGRAPH_%sURL" % product],
                app.config[keyref],
                app.config["AUTOGRAPH_%sUSERNAME" % product],
                app.config["AUTOGRAPH_%sPASSWORD" % product],
                hash_,
            )

        # cache with hash+keyref since headers will change based on the key
        signature, x5u = cache.get("content_signatures", f"{hash_}{keyref}", sign)
        headers = {"Content-Signature": f"x5u={x5u}; p384ecdsa={signature}"}
        log.debug("Added header: %s" % headers)
    return headers


def warm_caches():
    """Fetch all releases pointed at by a rule. This is intended to run at app
    startup, to ensure that it has all necessary information is in memory before
    it begins serving requests."""
    mapped_releases = set()
    for rule in dbo.rules.select(columns=[dbo.rules.mapping, dbo.rules.fallbackMapping], distinct=True):
        if rule["mapping"]:
            mapped_releases.add(rule["mapping"])
        if rule["fallbackMapping"]:
            mapped_releases.add(rule["fallbackMapping"])

    for release in mapped_releases:
        blob = get_release_blob(release)
        if not blob:
            continue

        for referenced_release in blob.getReferencedReleases():
            get_release_blob(referenced_release)


AUS = AUS()
