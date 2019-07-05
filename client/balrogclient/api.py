"""
Balrog API wrapper
"""

import json
import logging
import time

import requests
import requests.auth

# Refresh the tokens 5 minutes before they expire
REFRESH_THRESHOLD = 5 * 60
_token_cache = {}


def _json_log_data(data):
    log = json.dumps(data)
    if len(log) > 100:
        log = log[:80] + "<...{} characters elided ...>".format(len(log) - 80)
    return log


def is_csrf_token_expired(token):
    """Checks whether a CSRF token is still valid

    Expects a token of the form "YYYYMMDDHHMMSS##..."

    Returns:
        True if the token has expired
        False if the token is still valid
    """
    from datetime import datetime

    expiry = token.split("##")[0]
    if expiry <= datetime.now().strftime("%Y%m%d%H%M%S"):
        return True
    return False


def _get_auth0_token(secrets, session):
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
    headers = {"Content-Type": "application/json"}
    request = session.post(url, data=json.dumps(payload), headers=headers)
    response = request.json()
    # In order to know exact expiration we would need to decode the token, what
    # requires more dependencies. Instead we use the returned "expires_in" in
    # order to guess the expiry.
    _token_cache[cache_key] = response
    _token_cache[cache_key]["exp"] = time.time() + response["expires_in"]
    return _token_cache[cache_key]["access_token"]


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, access_token):
        self.access_token = access_token

    def __eq__(self, other):
        return self.access_token == getattr(other, "access_token", None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer {}".format(self.access_token)
        return r


class API(object):
    """A class that knows how to make requests to a Balrog server, including
       pre-retrieving CSRF tokens and data versions.

       url_template: The URL to submit to when request() is called. Standard
                     Python string interpolation can be used here in
                     combination with url_template_vars.
       prerequest_url_template: Before submitting the real request, a HEAD
                                operation will be done on this URL. If the
                                HEAD request succeeds, it is expected that
                                there will be X-CSRF-Token and X-Data-Version
                                headers in the response. If the HEAD request
                                results in a 404, another HEAD request to
                                /csrf_token will be made in attempt to get a
                                CSRF Token. This URL can use string
                                interpolation the same way url_template can.
                                In some cases this may be the same as the
                                url_template.
    """

    verify = False
    url_template = None
    prerequest_url_template = None
    url_template_vars = None

    def __init__(self, auth0_secrets, api_root="https://aus4-admin-dev.allizom.org/api", ca_certs=True, timeout=60, raise_exceptions=True, session=None):
        """ Creates an API object which wraps REST API of Balrog server.

        api_root: API root URL of balrog server
        ca_certs: CA bundle. It follows python-requests `verify' usage.
                  If set to False, no SSL verification is done.
                  If set to True, it tries to load a CA bundle from certifi
                  module.
                  If set to string, puthon-requests uses it as a pth to path to
                  CA bundle.
        timeout : request timeout
        raise_exceptions: controls exception handling of python-requests.
        session: requests esssion to use for API calls
        """
        self.api_root = api_root.rstrip("/")
        self.verify = ca_certs
        self.timeout = timeout
        self.raise_exceptions = raise_exceptions
        self.session = session or requests.session()
        self.csrf_token = None
        self.auth0_secrets = auth0_secrets

    def request(self, data=None, method="GET"):
        url = self.api_root + self.url_template % self.url_template_vars
        prerequest_url = self.api_root + self.prerequest_url_template % self.url_template_vars
        # If we'll be modifying things, do a GET first to get a CSRF token
        # and possibly a data_version.
        if method != "GET" and method != "HEAD":
            # Use the URL of the resource we're going to modify first,
            # because we'll need a CSRF token, and maybe its data version.
            try:
                res = self.do_request(prerequest_url, None, "HEAD")
                # If a data_version was specified we shouldn't overwrite it
                # because the caller may be acting on a modified version of
                # a specific older version of the data.
                if "data_version" not in data:
                    data["data_version"] = int(res.headers["X-Data-Version"])
                # We may already have a non-expired CSRF token, but it's
                # faster/easier just to set it again even if we do, since
                # we've already made the request.
                data["csrf_token"] = self.csrf_token = res.headers["X-CSRF-Token"]
            except requests.HTTPError as excp:
                # However, if the resource doesn't exist yet we may as well
                # not bother doing another request solely for a token unless
                # we don't have a valid one already.
                if excp.response.status_code != 404:
                    raise
                if not self.csrf_token or is_csrf_token_expired(self.csrf_token):
                    res = self.do_request(self.api_root + "/csrf_token", None, "HEAD")
                    data["csrf_token"] = self.csrf_token = res.headers["X-CSRF-Token"]

        return self.do_request(url, data, method)

    def do_request(self, url, data, method):
        logging.debug("Balrog request to %s", url)
        if data is not None and "csrf_token" in data:
            sanitised_data = data.copy()
            del sanitised_data["csrf_token"]
            logging.debug("Data sent: %s", _json_log_data(sanitised_data))
        else:
            logging.debug("Data sent: %s", _json_log_data(data))
        headers = {"Accept-Encoding": "application/json", "Accept": "application/json", "Content-Type": "application/json", "Referer": self.api_root}
        before = time.time()
        access_token = _get_auth0_token(self.auth0_secrets, session=self.session)
        auth = BearerAuth(access_token)
        # Don't dump data to json unless it actually exists. Otherwise we end up with a string of
        # 'None', which is not intended, and is not actually supported by some servers for HEAD/GET
        # requests.
        if data:
            data = json.dumps(data)
        req = self.session.request(method=method, url=url, data=data, timeout=self.timeout, verify=self.verify, auth=auth, headers=headers)
        try:
            if self.raise_exceptions:
                req.raise_for_status()
            return req
        except requests.HTTPError as excp:
            logging.error("Caught HTTPError: %s", excp.response.content)
            raise
        finally:
            stats = {"timestamp": time.time(), "method": method, "url": url, "status_code": req.status_code, "elapsed_secs": time.time() - before}
            logging.debug("REQUEST STATS: %s", json.dumps(stats))

    def get_data(self):
        resp = self.request()
        return (json.loads(resp.content), int(resp.headers["X-Data-Version"]))


class Release(API):
    url_template = "/releases/%(name)s"
    prerequest_url_template = "/releases/%(name)s"

    def __init__(self, name, **kwargs):
        super(Release, self).__init__(**kwargs)
        self.name = name
        self.url_template_vars = dict(name=name)

    def update_release(self, product, hashFunction, releaseData, data_version=None, schemaVersion=None):
        data = dict(name=self.name, product=product, hashFunction=hashFunction, data=releaseData)
        if data_version:
            data["data_version"] = data_version
        if schemaVersion:
            data["schema_version"] = schemaVersion
        return self.request(method="POST", data=data)


class SingleLocale(API):
    url_template = "/releases/%(name)s/builds/%(build_target)s/%(locale)s"
    prerequest_url_template = "/releases/%(name)s"

    def __init__(self, name, build_target, locale, **kwargs):
        super(SingleLocale, self).__init__(**kwargs)
        self.name = name
        self.build_target = build_target
        self.locale = locale
        self.url_template_vars = dict(name=name, build_target=build_target, locale=locale)
        # keep a copy to be used in get_data()
        self.release_kwargs = kwargs

    def get_data(self):
        data, data_version = {}, None
        # If the locale-specific API end point returns 404, we have to use the
        # top level blob to get the data version. Because this requires 2 not
        # atomic HTTP requests, we start with the top level blob and use its
        # data version.
        top_level = Release(name=self.name, **self.release_kwargs)
        # Use data version from the top level blob
        try:
            _, data_version = top_level.get_data()
        except requests.HTTPError as excp:
            if excp.response.status_code == 404:
                # top level blob doesn't exist, assume there is no data
                return data, data_version
            else:
                raise
        # Got data version. Try to get data from the locale specific blob.
        # Using data version from the top level blob prevents possible race
        # conditions if another client updates the locale blob between the
        # first request and the call below.
        try:
            data, _ = super(SingleLocale, self).get_data()
            return data, data_version
        except requests.HTTPError as excp:
            if excp.response.status_code == 404:
                # locale blob doesn't exist, no data
                return data, data_version
            else:
                raise

    def update_build(self, product, hashFunction, buildData, alias=None, schemaVersion=None, data_version=None):
        data = dict(product=product, data=buildData, hashFunction=hashFunction)
        if alias:
            data["alias"] = alias
        if data_version:
            data["data_version"] = data_version
        if schemaVersion:
            data["schema_version"] = schemaVersion

        return self.request(method="PUT", data=data)


class Rule(API):
    """Update Balrog rules"""

    url_template = "/rules/%(rule_id)s"
    prerequest_url_template = "/rules/%(rule_id)s"

    def __init__(self, rule_id, **kwargs):
        super(Rule, self).__init__(**kwargs)
        self.rule_id = rule_id
        self.url_template_vars = dict(rule_id=rule_id)

    def update_rule(self, **rule_data):
        """wrapper for self.request"""
        return self.request(method="POST", data=rule_data)


class ScheduledRuleChange(API):
    """Update Balrog rules"""

    url_template = "/scheduled_changes/rules"
    prerequest_url_template = "/rules/%(rule_id)s"

    def __init__(self, rule_id, **kwargs):
        super(ScheduledRuleChange, self).__init__(**kwargs)
        self.rule_id = rule_id
        self.url_template_vars = dict(rule_id=rule_id)

    def add_scheduled_rule_change(self, **rule_data):
        """wrapper for self.request"""
        return self.request(method="POST", data=rule_data)
