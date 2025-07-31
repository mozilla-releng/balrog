import jose.jwt
import requests
from auth0.authentication import Users as auth0_Users
from repoze.lru import lru_cache

from auslib.util.statsd import statsd


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_access_token(request):
    if "access_token" in request.form:
        return request.form["access_token"]
    if "access_token" in request.args:
        return request.args["access_token"]

    # For a gracefully transition, we will temporarily be accepting both
    # HTTP Auth (which will overwrite the Authorization header) and
    # a Bearer token. During this period, we need to look for a Bearer
    # token in both headers. Once clients switch to Authorization
    # we will remove support for X-Authorization.
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing", "description": "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header", "description": "Authorization header must start with Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header", "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header", "description": "Authorization header must be Bearer token"}, 401)

    token = parts[1]
    return token


# Cache this for 1 hour. Without this, we'd need to restart the admin app
# to pick up changes to the keys.
@lru_cache(2048, timeout=3600)
def get_jwks(auth_domain):
    jwks_url = "https://{}/.well-known/jwks.json".format(auth_domain)
    req = requests.get(jwks_url)
    req.raise_for_status()
    return req.json()


@lru_cache(2048)
def get_additional_userinfo(auth_domain, access_token):
    with statsd.timer("auth0_userinfo"):
        return auth0_Users(auth_domain).userinfo(access_token)


def verified_userinfo(request, auth_domain, auth_audience):
    jwks = get_jwks(auth_domain)
    access_token = get_access_token(request)
    try:
        unverified_header = jose.jwt.get_unverified_header(access_token)
    except jose.jwt.JWTError:
        raise AuthError({"code": "invalid_header", "description": "Invalid header. Use an RS256 signed JWT Access Token"}, 401)
    if unverified_header["alg"] == "HS256":
        raise AuthError({"code": "invalid_header", "description": "Invalid header. Use an RS256 signed JWT Access Token"}, 401)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {"kty": key["kty"], "kid": key["kid"], "use": key["use"], "n": key["n"], "e": key["e"]}
    if rsa_key:
        try:
            payload = jose.jwt.decode(access_token, rsa_key, algorithms=["RS256"], audience=auth_audience, issuer="https://{}/".format(auth_domain))
            if "gty" in payload:
                # The gty field being present means it is a machine token
                # azp in machine tokens is their clientId, which is the closest
                # thing we have to an e-mail address for them
                payload["email"] = payload.get("azp")
            else:
                # Otherwise, assume it's a human, and gather additional information
                # about them.
                payload.update(get_additional_userinfo(auth_domain, access_token))
            if not payload.get("email"):
                raise AuthError({"code": "no_email", "description": "no email address found in access or id tokens"}, 401)
            return payload
        except jose.jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired", "description": "token is expired"}, 401)
        except jose.jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims", "description": "incorrect claims, please check the audience and issuer"}, 401)
        except ValueError:
            raise AuthError({"code": "incomplete_validation", "description": "couldn't find additional userinfo from access token"}, 401)
    else:
        raise AuthError({"code": "invalid_key", "description": "Unable to find RSA key."}, 401)
