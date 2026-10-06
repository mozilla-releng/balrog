import json
import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from werkzeug.datastructures import Headers, ImmutableMultiDict

import auslib.util.auth
from auslib.util.auth import AuthError, verified_userinfo

AUTH_DOMAIN = "balrog.example.com"
AUTH_AUDIENCE = "balrog-audience"
KID = "test-key"


class FakeRequest:
    def __init__(self, token):
        self.form = ImmutableMultiDict()
        self.args = ImmutableMultiDict()
        self.headers = Headers({"Authorization": f"Bearer {token}"})


@pytest.fixture(scope="module")
def private_key():
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture(autouse=True)
def mock_jwks(monkeypatch, private_key):
    jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(private_key.public_key()))
    jwk.update({"kid": KID, "use": "sig"})
    monkeypatch.setattr(auslib.util.auth, "get_jwks", lambda domain: {"keys": [jwk]})
    monkeypatch.setattr(auslib.util.auth, "get_additional_userinfo", lambda domain, token: {"email": "human@example.com"})


def make_token(key, kid=KID, algorithm="RS256", **overrides):
    claims = {
        "iss": f"https://{AUTH_DOMAIN}/",
        "aud": AUTH_AUDIENCE,
        "exp": int(time.time()) + 3600,
        "sub": "someone",
    }
    claims.update(overrides)
    claims = {k: v for k, v in claims.items() if v is not None}
    return jwt.encode(claims, key, algorithm=algorithm, headers={"kid": kid})


def test_machine_token(private_key):
    token = make_token(private_key, gty="client-credentials", azp="my-client")
    payload = verified_userinfo(FakeRequest(token), AUTH_DOMAIN, AUTH_AUDIENCE)
    assert payload["email"] == "my-client"


def test_human_token(private_key):
    token = make_token(private_key)
    payload = verified_userinfo(FakeRequest(token), AUTH_DOMAIN, AUTH_AUDIENCE)
    assert payload["email"] == "human@example.com"
    assert payload["sub"] == "someone"


@pytest.mark.parametrize(
    "overrides,code",
    [
        ({"exp": int(time.time()) - 60}, "token_expired"),
        ({"aud": "wrong-audience"}, "invalid_claims"),
        ({"aud": None}, "invalid_claims"),
        ({"iss": "https://evil.example.com/"}, "invalid_claims"),
        ({"nbf": int(time.time()) + 3600}, "invalid_claims"),
    ],
)
def test_bad_claims(private_key, overrides, code):
    token = make_token(private_key, **overrides)
    with pytest.raises(AuthError) as excinfo:
        verified_userinfo(FakeRequest(token), AUTH_DOMAIN, AUTH_AUDIENCE)
    assert excinfo.value.error["code"] == code
    assert excinfo.value.status_code == 401


def test_bad_signature():
    other_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    token = make_token(other_key)
    with pytest.raises(AuthError) as excinfo:
        verified_userinfo(FakeRequest(token), AUTH_DOMAIN, AUTH_AUDIENCE)
    assert excinfo.value.error["code"] == "invalid_token"


def test_unknown_kid(private_key):
    token = make_token(private_key, kid="other-key")
    with pytest.raises(AuthError) as excinfo:
        verified_userinfo(FakeRequest(token), AUTH_DOMAIN, AUTH_AUDIENCE)
    assert excinfo.value.error["code"] == "invalid_key"


def test_hs256_rejected():
    token = make_token("a-shared-secret-that-is-long-enough-for-hs256", algorithm="HS256")
    with pytest.raises(AuthError) as excinfo:
        verified_userinfo(FakeRequest(token), AUTH_DOMAIN, AUTH_AUDIENCE)
    assert excinfo.value.error["code"] == "invalid_header"


def test_garbage_token():
    with pytest.raises(AuthError) as excinfo:
        verified_userinfo(FakeRequest("not-a-jwt"), AUTH_DOMAIN, AUTH_AUDIENCE)
    assert excinfo.value.error["code"] == "invalid_header"
