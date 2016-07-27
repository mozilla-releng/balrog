import json


default_headers = {
    "Accept-Encoding": "application/json",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_url(api_root, path):
    return api_root.rstrip("/") + path


async def request(session, api_root, path, method="GET", data=None, headers=default_headers):
    url = get_url(api_root, path)
    if data:
        data = data.copy()

    resp = await session.request(method, url, data=json.dumps(data), headers=headers)
    # Raises on 400 code or higher, we can assume things are good if we make it past this.
    resp.raise_for_status()
    # TODO: is it okay that an async function is not returning a coroutine?
    # We need this to be async so we can await the request above, but we
    # want callers to have access to the raw response so they can check
    # headers or stream the response if they choose.
    return resp
