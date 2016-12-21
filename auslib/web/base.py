import logging
log = logging.getLogger(__name__)

from flask import Flask, make_response, send_from_directory, abort

from raven.contrib.flask import Sentry

from auslib.AUS import AUS
from auslib.dockerflow import create_dockerflow_endpoints

app = Flask(__name__)
AUS = AUS()
sentry = Sentry()

from auslib.web.views.client import ClientRequestView
from auslib.errors import BadDataError


def heartbeat_database_function(dbo):
    # web has only a read access to the database. That's why we don't use
    # the default database function.
    # Counting the rules should be a trivial enough operation that it won't
    # cause notable load, but will verify that the database works.
    return dbo.rules.countRules()

create_dockerflow_endpoints(app, heartbeat_database_function)


@app.errorhandler(404)
def fourohfour(error):
    """We don't return 404s in AUS. Instead, we return empty XML files"""
    response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
    response.mimetype = 'text/xml'
    return response


@app.errorhandler(Exception)
def generic(error):
    """Deals with any unhandled exceptions. If the exception is not a
    BadDataError, it will be sent to Sentry. Regardless of the exception,
    a 500 response is returned."""

    if not isinstance(error, BadDataError):
        if sentry.client:
            sentry.captureException()

    raise Exception(error)


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, "robots.txt")


@app.route('/update/1/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/update.xml')
@app.route('/update/2/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/update.xml')
@app.route('/update/3/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/update.xml')
@app.route('/update/4/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/%MOZ_VERSION%'
           '/update.xml')
@app.route('/update/5/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%DISTRIBUTION%/%DISTRIBUTION_VERSION%/%IMEI%/update.xml')
@app.route('/update/6/%PRODUCT%/%VERSION%/%BUILD_ID%/%BUILD_TARGET%/%LOCALE%/%CHANNEL%/%OS_VERSION%/%SYSTEM_CAPABILITIES%/%DISTRIBUTION%'
           '/%DISTRIBUTION_VERSION%/update.xml')
def unsubstituted_url_variables():
    abort(404)


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
