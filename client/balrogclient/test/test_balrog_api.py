# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function

import logging

from requests import Session
from requests_mock import Adapter

from balrogclient.api import API

AUTH0_SECRETS = {"client_id": "some-client", "client_secret": "super-secret", "audience": "tests", "domain": "auth0.test"}


def test_log_lines_truncated(caplog):
    session = Session()
    adapter = Adapter()
    session.mount("https://", adapter)
    adapter.register_uri("POST", "https://auth0.test/oauth/token", json={"expires_in": 3600, "access_token": "the-token"})
    adapter.register_uri("GET", "https://api/")

    caplog.set_level(logging.DEBUG)

    api = API(AUTH0_SECRETS, session=session)
    api.do_request("https://api/", {"data": "a" * 100}, "GET")

    logs = [message.split(": ", 1)[1] for message in caplog.messages if message.startswith("Data sent: ")]
    assert logs == ['{"data": "' + "a" * 70 + "<...32 characters elided ...>"]
