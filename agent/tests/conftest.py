from unittest.mock import MagicMock

import pytest


@pytest.fixture
def fake_request():
    def fake_request_factory(return_values={}):
        async def do_fake_request(api_root, path, auth0_secrets, method="GET", data={}, headers={}, loop=None):
            if method == "GET":
                endpoint = path[1:]
                ret = return_values.get(endpoint, [])
                if "v2" in endpoint:
                    return ret
                else:
                    return {"count": len(ret), "scheduled_changes": ret}
            else:
                return ""

        return MagicMock(side_effect=do_fake_request)

    return fake_request_factory
