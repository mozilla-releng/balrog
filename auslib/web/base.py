import logging
log = logging.getLogger(__name__)

from flask import Flask, make_response, send_from_directory, request

from auslib.AUS import AUS
from auslib.dockerflow import create_dockerflow_endpoints

app = Flask(__name__)
AUS = AUS()

from auslib.web.views.client import ClientRequestView


def heartbeat_database_function(dbo):
    # web has only a read access to the database. That's why we don't use
    # the default database function.
    # Counting the rules should be a trivial enough operation that it won't
    # cause notable load, but will verify that the database works.
    dbo.rules.countRules()

create_dockerflow_endpoints(app, heartbeat_database_function)


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

    # We don't want to eat exceptions from this special Dockerflow endpoint because
    # it's used by CloudOps' infrastructure to see whether or not the app is
    # functional. See https://github.com/mozilla-services/Dockerflow for additional
    # details.
    if request.path == "/__heartbeat__":
        return error

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
app.add_url_rule(
    '/update/6/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<systemCapabilities>/<distribution>/<distVersion>/update.xml',
    view_func=ClientRequestView.as_view('clientrequest6'),
    defaults={'queryVersion': 6},
)

# Routes to deal with edge cases.
# bug 1133250 - support for old-style nightly ESR versions
app.add_url_rule(
    '/update/3/<product>/<version>esrpre/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/update.xml',
    view_func=ClientRequestView.as_view('clientrequest_esrnightly'),
    defaults={'queryVersion': 3},
)
