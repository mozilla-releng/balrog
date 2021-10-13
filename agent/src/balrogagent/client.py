import json
import logging
import time

import aiohttp

default_headers = {"Accept-Encoding": "application/json", "Accept": "application/json", "Content-Type": "application/json"}
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
            return entry["access_token"]

    logging.debug("Refreshing, getting new token")
    url = "https://{}/oauth/token".format(secrets["domain"])
    payload = dict(client_id=secrets["client_id"], client_secret=secrets["client_secret"], audience=secrets["audience"], grant_type="client_credentials")
    async with aiohttp.ClientSession(loop=loop) as client:
        async with client.request("POST", url, json=payload) as resp:
            resp.raise_for_status()
            response = await resp.json()
            # In order to know exact expiration we would need to decode the token, what
            # requires more dependencies. Instead we use the returned "expires_in" in
            # order to guess the expiry.
            _token_cache[cache_key] = response
            _token_cache[cache_key]["exp"] = time.time() + response["expires_in"]
            return _token_cache[cache_key]["access_token"]


def get_url(api_root, path):
    return api_root.rstrip("/") + path


async def request(api_root, path, auth0_secrets, method="GET", data={}, headers=default_headers, loop=None):
    headers = headers.copy()
    url = get_url(api_root, path)
    access_token = await _get_auth0_token(auth0_secrets, loop)
    headers["Authorization"] = "Bearer {}".format(access_token)

    async with aiohttp.ClientSession(loop=loop) as client:
        logging.debug("Sending %s request to %s", method, url)
        async with client.request(method, url, data=json.dumps(data), headers=headers) as resp:
            # Raises on 400 code or higher, we can assume things are good if we make it past this.
            resp.raise_for_status()
            return await resp.json()
