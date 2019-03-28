import aiohttp
import json
import logging
import os
import time


default_headers = {
    "Accept-Encoding": "application/json",
    "Accept": "application/json",
    "Content-Type": "application/json",
}
# Refresh the tokens 5 minutes before they expire
REFRESH_THRESHOLD = 5 * 60
_token_cache = {}


async def _get_auth0_token(secrets, loop=None):
    """Get Auth0 token

    See https://auth0.com/docs/api/authentication#regular-web-app-login-flow43 for the description
    """
    cache_key = "{}-{}-{}".format(secrets["client_id"], secrets["client_secret"], secrets["audience"])
    if cache_key in _token_cache:
        entry = _token_cache[cache_key]
        expiration = entry["exp"]
        if expiration - time.time() > REFRESH_THRESHOLD:
            logging.debug("Using cached token")
            return entry['access_token']

    logging.debug("Refreshing, getting new token")
    url = "https://{}/oauth/token".format(secrets["domain"])
    payload = dict(
        client_id=secrets["client_id"],
        client_secret=secrets["client_secret"],
        audience=secrets["audience"],
        grant_type='client_credentials',
    )
    async with aiohttp.ClientSession(loop=loop) as client:
        async with client.request("POST", url, json=payload) as resp:
            resp.raise_for_status()
            response = await resp.json()
            # In order to know exact expiration we would need to decode the token, what
            # requires more dependencies. Instead we use the returned "expires_in" in
            # order to guess the expiry.
            _token_cache[cache_key] = response
            _token_cache[cache_key]["exp"] = time.time() + response["expires_in"]
            return _token_cache[cache_key]['access_token']


def get_url(api_root, path):
    return api_root.rstrip("/") + path


async def request(api_root, path, method="GET", data={}, headers=default_headers,
                  auth=None, auth0_secrets=None, loop=None):
    headers = headers.copy()
    url = get_url(api_root, path)
    csrf_url = get_url(api_root, "/csrf_token")
    data = data.copy()
    if auth0_secrets:
        access_token = await _get_auth0_token(auth0_secrets, loop)
        headers["Authorization"] = "Bearer {}".format(access_token)

    # Aiohttp does not allow cookie from urls that using IP address instead dns name,
    # so if for any reason agent needs point to IP address, the envvar "ALLOW_COOKIE_FROM_IP_URL"
    # should be set. (https://aiohttp.readthedocs.io/en/stable/client_advanced.html#cookie-safety)
    cookie_jar = aiohttp.CookieJar(unsafe=os.environ.get('ALLOW_COOKIE_FROM_IP_URL', False))

    async with aiohttp.ClientSession(loop=loop, cookie_jar=cookie_jar) as client:
        # CSRF tokens are only required for POST/PUT/DELETE.
        if method not in ("HEAD", "GET"):
            logging.debug("Sending %s request to %s", "HEAD", csrf_url)
            async with client.request("HEAD", csrf_url, auth=auth, headers=headers) as resp:
                resp.raise_for_status()
                data["csrf_token"] = resp.headers["X-CSRF-Token"]

        # Workaround for https://bugzilla.mozilla.org/show_bug.cgi?id=1471109
        # In our deployed environments, the Agent doesn't connect to admin over
        # https, which means it won't send back the session token by default,
        # which breaks csrf token validation. Changing the cookies to insecure
        # will let them be sent back, but it's a horrible back.
        # Checking for this specific api_root makes sure it's only enabled for
        # our deployed environments.
        if api_root == "http://localhost:81/api":
            for c in client.cookie_jar:
                c["secure"] = False

        logging.debug("Sending %s request to %s", method, url)
        async with client.request(method, url, data=json.dumps(data), headers=headers, auth=auth) as resp:
            # Raises on 400 code or higher, we can assume things are good if we make it past this.
            resp.raise_for_status()
            return (await resp.json())
