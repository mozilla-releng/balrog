import json
import logging


default_headers = {
    "Accept-Encoding": "application/json",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_url(api_root, path):
    return api_root.rstrip("/") + path


async def request(session, api_root, path, method="GET", data={}, headers=default_headers):
    headers = headers.copy()
    url = get_url(api_root, path)
    csrf_url = get_url(api_root, "/csrf_token")
    data = data.copy()

    # TODO: sometimes getting "unclosed response" and "unclosed connection" errors.
    logging.debug("Sending %s request to %s", "HEAD", csrf_url)
    resp = await session.request("HEAD", csrf_url)
    resp.raise_for_status()
    data["csrf_token"] = resp.headers["X-CSRF-Token"]
    resp.close()

    logging.debug("Sending %s request to %s", method, url)
    resp = await session.request(method, url, data=json.dumps(data), headers=headers)
    # Raises on 400 code or higher, we can assume things are good if we make it past this.
    resp.raise_for_status()
    # TODO: is it okay that an async function is not returning a coroutine?
    # We need this to be async so we can await the request above, but we
    # want callers to have access to the raw response so they can check
    # headers or stream the response if they choose.
    return resp
