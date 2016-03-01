from os import path

import logging
log = logging.getLogger(__name__)

from flask import Flask, make_response, send_from_directory, jsonify

from auslib.AUS import AUS
from auslib.global_state import dbo

app = Flask(__name__)
AUS = AUS()

from auslib.web.views.client import ClientRequestView


@app.errorhandler(404)
def fourohfour(error):
    """We don't return 404s in AUS. Instead, we return empty XML files"""
    response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
    response.mimetype = 'text/xml'
    return response


@app.errorhandler(Exception)
def generic(error):
    """Deals with any unhandled exceptions. Regardless of the exception,
    a 200 response with no updates is returned, because that's what the client
    expects. See bugs 885173 and 1069454 for additional background."""

    log.debug('Hit exception, sending an empty response', exc_info=True)
    response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
    response.mimetype = 'text/xml'
    return response


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, "robots.txt")

# The "main" routes. 99% of requests will come in through these.
app.add_url_rule(
    "/update/1/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/update.xml",
    view_func=ClientRequestView.as_view("clientrequest1"),
    # Underlying code depends on osVersion being set. Since this route only
    # exists to support ancient queries, and all newer versions have osVersion
    # in them it's easier to set this here than make the all of the underlying
    # code support queries without it.
    defaults={"queryVersion": 2, "osVersion": ""},
)
app.add_url_rule(
    '/update/2/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/update.xml',
    view_func=ClientRequestView.as_view('clientrequest2'),
    defaults={'queryVersion': 2},
)
app.add_url_rule(
    '/update/3/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/update.xml',
    view_func=ClientRequestView.as_view('clientrequest3'),
    defaults={'queryVersion': 3},
)
app.add_url_rule(
    '/update/4/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/<platformVersion>/update.xml',
    view_func=ClientRequestView.as_view('clientrequest4'),
    defaults={'queryVersion': 4},
)
app.add_url_rule(
    '/update/5/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/<IMEI>/update.xml',
    view_func=ClientRequestView.as_view('clientrequest5'),
    defaults={'queryVersion': 5},
)

# Routes to deal with edge cases.
# bug 1133250 - support for old-style nightly ESR versions
app.add_url_rule(
    '/update/3/<product>/<version>esrpre/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/update.xml',
    view_func=ClientRequestView.as_view('clientrequest_esrnightly'),
    defaults={'queryVersion': 3},
)


# Endpoints required by CloudOps as part of the Dockerflow spec: https://github.com/mozilla-services/Dockerflow

version_json = None


@app.route("/__version__")
def version():
    version_file = app.config.get("VERSION_FILE")
    if version_file and path.exists(version_file):
        with open(app.config["VERSION_FILE"]) as f:
            version_json = f.read()
        return Response(version_json, mimetype="application/json")
    else:
        return jsonify({
            "source": "https://github.com/mozilla/balrog",
            "version": "unknown",
            "commit": "unknown",
        })


@app.route("/__heartbeat__")
def heartbeat():
    """Per the Dockerflow spec:
    Respond to /__heartbeat__ with a HTTP 200 or 5xx on error. This should
    depend on services like the database to also ensure they are healthy."""
    # Counting the rules should be a trivial enough operation that it won't
    # cause notable load, but will verify that the database works.
    dbo.rules.countRules()
    return "OK!"


@app.route("/__lbheartbeat__")
def lbheartbeat():
    """Per the Dockerflow spec:
    Respond to /__lbheartbeat__ with an HTTP 200. This is for load balancer
    checks and should not check any dependent services."""
    return "OK!"
