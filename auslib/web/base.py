import logging
log = logging.getLogger(__name__)

from flask import Flask, make_response, send_from_directory

from raven.contrib.flask import Sentry

from auslib.AUS import AUS

app = Flask(__name__)
AUS = AUS()
sentry = Sentry()

from auslib.errors import BadDataError
from auslib.web.views.client import ClientRequestView


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
    a 200 response with no updates is returned, because that's what the client
    expects. See bugs 885173 and 1069454 for additional background."""

    if not isinstance(error, BadDataError):
        if sentry.client:
            sentry.captureException()
    log.debug('Hit exception, sending an empty response')
    response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
    response.mimetype = 'text/xml'
    return response

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, "robots.txt")

app.add_url_rule(
    '/update/2/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/update.xml',
    view_func=ClientRequestView.as_view('clientrequest'),
    defaults={'queryVersion': 2},
)
app.add_url_rule(
    '/update/3/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/update.xml',
    view_func=ClientRequestView.as_view('clientrequest'),
    defaults={'queryVersion': 3},
)
app.add_url_rule(
    '/update/4/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/<platformVersion>/update.xml',
    view_func=ClientRequestView.as_view('clientrequest'),
    defaults={'queryVersion': 4},
)
