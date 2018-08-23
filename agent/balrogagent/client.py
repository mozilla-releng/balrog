import aiohttp
import json
import logging
import os


default_headers = {
    "Accept-Encoding": "application/json",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_url(api_root, path):
    return api_root.rstrip("/") + path


async def request(api_root, path, method="GET", data={}, headers=default_headers, auth=None, loop=None):
    headers = headers.copy()
    url = get_url(api_root, path)
    csrf_url = get_url(api_root, "/csrf_token")
    data = data.copy()

    # Aiohttp does not allow cookie from urls that using IP address instead dns name,
    # so if for any reason agent needs point to IP address, the envvar "ALLOW_COOKIE_FROM_IP_URL"
    # should be set. (https://aiohttp.readthedocs.io/en/stable/client_advanced.html#cookie-safety)
    cookie_jar = aiohttp.CookieJar(unsafe=os.environ.get('ALLOW_COOKIE_FROM_IP_URL', False))

    async with aiohttp.ClientSession(loop=loop, cookie_jar=cookie_jar) as client:
        # CSRF tokens are only required for POST/PUT/DELETE.
        if method not in ("HEAD", "GET"):
            logging.debug("Sending %s request to %s", "HEAD", csrf_url)
            async with client.request("HEAD", csrf_url, auth=auth) as resp:
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
