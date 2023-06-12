#!/usr/bin/env python

import json
import logging
import time

import requests
import requests.auth

log = logging.getLogger(__name__)


# TODO: better --env=local support (I get SSL errors)
# TODO: some POST/DELETEs? disallow on production??


class AdhocBalrogTester:
    BASE_URLS = {
        "local-admin": "https://localhost:8010",
        "local-public": "https://localhost:9010",
        "local-ui": "https://localhost:9000",
        "production-admin": "https://aus4-admin.mozilla.org",
        "production-public": "https://aus5.mozilla.org",
        "production-ui": "https://balrog.services.mozilla.com",
        "staging-admin": "https://admin-stage.balrog.nonprod.cloudops.mozgcp.net",
        "staging-public": "https://stage.balrog.nonprod.cloudops.mozgcp.net",
        "staging-ui": "https://balrog-admin-static-stage.stage.mozaws.net",
    }

    def __init__(self, environment="staging", test_level=2):
        self.session = requests.Session()
        # TODO: should we do this...?
        # access_token = _get_auth0_token(auth0_secrets, session=session)
        # session.auth = BearerAuth(access_token)
        self.headers = {"User-Agent": "adhoc-tester.py"}
        self.environment = environment
        self.test_level = test_level

    def balrog_request(self, method, url, *args, **kwargs):
        log.info(f"Balrog request to {url} via {method.upper()}")
        if self.environment == "local":
            kwargs["verify"] = False
        data = kwargs.get("json", kwargs.get("data"))
        if data:
            log.debug(f"Data sent: {data}")
        resp = self.session.request(method, url, *args, **kwargs)
        try:
            resp.raise_for_status()
            if "content-signature" in resp.headers:
                log.info("  found content-signature: " + resp.headers["content-signature"])
            if resp.content:
                try:
                    resp_data = resp.json()
                    log.debug("Received: %s", json.dumps(resp_data, indent=2))
                    return resp_data
                except json.decoder.JSONDecodeError:
                    return resp.content
            else:
                return
        except requests.HTTPError as exc:
            log.error("Caught HTTPError: %s", exc.response.content)
            raise
        finally:
            stats = {
                "timestamp": time.time(),
                "method": method.upper(),
                "url": url,
                "status_code": resp.status_code,
                "elapsed_secs": resp.elapsed.total_seconds(),
            }
            log.debug("REQUEST STATS: %s", json.dumps(stats))
        return

    def make_url(self, environment, interface, append):
        destination = environment + "-" + interface
        base = self.BASE_URLS[destination]
        return "/".join([base, append])

    def version(self, environment, interface):
        url = self.make_url(environment, interface, "__version__")
        version = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {environment}-{interface} version: {version["version"]}')

    def heartbeat(self, environment, interface):
        url = self.make_url(environment, interface, "__heartbeat__")
        heartbeat = self.balrog_request("GET", url, headers=self.headers)
        log.info(f"  {environment}-{interface} heartbeat: {heartbeat}")
        url = self.make_url(environment, interface, "__lbheartbeat__")
        heartbeat = self.balrog_request("GET", url, headers=self.headers)
        log.info(f"  {environment}-{interface} load balancer heartbeat: {heartbeat}")

    def admin_releases(self, environment, interface):
        url = self.make_url(environment, interface, "releases")
        releases = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {len(releases["releases"])} releases found')
        url = self.make_url(environment, interface, "api/releases")
        releases = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {len(releases["releases"])} api/releases found')
        url = self.make_url(environment, interface, "api/v2/releases")
        releases = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {len(releases["releases"])} api/v2/releases found')
        if test_level > 2:
            for r in releases["releases"][-10:]:
                log.info(f'{r["name"]} ({r["product"]}, {r["data_version"]})')
                url = self.make_url(environment, interface, f'api/v2/releases/{r["name"]}')
                self.balrog_request("GET", url, headers=self.headers)

    def admin_scheduled_changes(self, environment, interface):
        url = self.make_url(environment, interface, "scheduled_changes/emergency_shutoff")
        resp = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {resp["count"]} scheduled changes')
        url = self.make_url(environment, interface, "scheduled_changes/required_signoffs/permissions")
        resp = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {resp["count"]} scheduled changes')
        url = self.make_url(environment, interface, "scheduled_changes/required_signoffs/product")
        resp = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {resp["count"]} scheduled changes')
        url = self.make_url(environment, interface, "scheduled_changes/releases")
        resp = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {resp["count"]} scheduled changes')
        url = self.make_url(environment, interface, "scheduled_changes/rules")
        resp = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {resp["count"]} scheduled changes')

    def public_updates(self, environment, interface):
        # TODO many other interesting and important endpoints
        url = self.make_url(
            environment,
            interface,
            "update/3/GMP/85.0/20200518093924/WINNT_x86_64-msvc-x64/en-US/release/Windows_NT%2010.0.0.0.18363.1016%20(x64)/default/default/update.xml",
        )
        resp = self.balrog_request("GET", url, headers=self.headers)
        log.info(f"  GMP update found, length: {len(resp)}")  # XML blob

    def public_releases(self, environment, interface):
        url = self.make_url(environment, interface, "api/v1/releases")
        releases = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {len(releases["releases"])} api/v1/releases found')
        url = self.make_url(environment, interface, "api/v1/releases?name_prefix=Firefox")
        releases = self.balrog_request("GET", url, headers=self.headers)
        log.info(f'  {len(releases["releases"])} api/v1/releases starting with "Firefox" found')
        if test_level > 2:
            for r in releases["releases"][-10:]:
                log.info(f'{r["name"]} ({r["product"]}, {r["data_version"]})')
                url = self.make_url(environment, interface, f'api/v1/releases/{r["name"]}')
                self.balrog_request("GET", url, headers=self.headers)

    def run_tests_admin(self):
        interface = "admin"
        log.info(f"Running {interface} tests...")
        self.heartbeat(self.environment, interface)
        self.version(self.environment, interface)
        if test_level > 1:
            self.admin_releases(self.environment, interface)
            self.admin_scheduled_changes(self.environment, interface)

    def run_tests_public(self):
        interface = "public"
        log.info(f"Running {interface} tests...")
        self.heartbeat(self.environment, interface)
        self.version(self.environment, interface)
        if test_level > 1:
            self.public_updates(self.environment, interface)
            self.public_releases(self.environment, interface)

    def run_tests(self):
        self.run_tests_public()
        log.info("")
        self.run_tests_admin()


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-i", "--interface", dest="interface", choices=["admin", "public"], default="public")
    parser.add_option("-e", "--env", dest="env", choices=["local", "staging", "production"], default="staging")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="verbose output")
    parser.add_option("-q", "--quiet", dest="quiet", action="store_true", help="less output")
    parser.add_option("-f", "--fast", dest="fast", action="store_true", help="fewer tests")
    parser.add_option("-a", "--all", dest="all", action="store_true", help="all tests")

    options, args = parser.parse_args()

    log_level = logging.INFO
    if options.verbose:
        log_level = logging.DEBUG
    elif options.quiet:
        log_level = logging.WARNING
    logging.basicConfig(level=log_level, format="%(message)s")

    test_level = 2
    if options.all:
        test_level = 3
    elif options.fast:
        test_level = 1

    adhoc = AdhocBalrogTester(options.env, test_level)
    adhoc.run_tests()
