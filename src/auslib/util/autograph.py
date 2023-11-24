from base64 import b64encode
from hashlib import sha384

import requests
from requests_hawk import HawkAuth

from auslib.util.retry import retry_sync

SIGNATURE_PREFIX = "Content-Signature:\x00"


def make_hash(content):
    assert isinstance(content, str)
    templated = f"{SIGNATURE_PREFIX}{content}".encode("ascii")
    return sha384(templated).digest()


def _sign_hash(autograph_uri, keyid, id_, key, hash_):
    auth = HawkAuth(id=id_, key=key)
    with requests.Session() as session:
        body = [{"input": b64encode(hash_).decode("ascii"), "keyid": keyid}]
        r = session.post(f"{autograph_uri}/sign/hash", json=body, auth=auth)
        r.raise_for_status()
        response = r.json()
        if len(response) != 1:
            raise Exception("Response is not length 1, cannot parse it")
        return response[0]["signature"], response[0]["x5u"]


def sign_hash(autograph_uri, keyid, id, key, hash):
    return retry_sync(_sign_hash, args=(autograph_uri, keyid, id, key, hash), attempts=3, sleeptime_kwargs={"delay_factor": 2.0})
