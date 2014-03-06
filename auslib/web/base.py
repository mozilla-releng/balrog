import logging
log = logging.getLogger(__name__)

from flask import Flask, make_response

from raven.contrib.flask import Sentry

from auslib.AUS import AUS

app = Flask(__name__)
AUS = AUS()
sentry = Sentry()

from auslib.web.views.client import ClientRequestView

@app.errorhandler(404)
def fourohfour(error):
    """We don't return 404s in AUS. Instead, we return empty XML files"""
    response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
    response.mimetype = 'text/xml'
    return response

@app.errorhandler(Exception)
def generic(error):
    # Log the error with Sentry before eating it (see bug 885173 for background)
    if sentry.client:
        sentry.captureException()
    response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
    response.mimetype = 'text/xml'
    return response

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
