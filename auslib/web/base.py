import logging
log = logging.getLogger(__name__)

from flask import Flask, make_response, request

from auslib import version
from auslib.AUS import AUS3

app = Flask(__name__)
AUS = AUS3()

from auslib.web.views.client import ClientRequestView

@app.errorhandler(404)
def fourohfour(error):
    """We don't return 404s in AUS. Instead, we return empty XML files"""
    response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
    response.mimetype = 'text/xml'
    return response

@app.errorhandler(500)
def isa(error):
    log.error("Caught ISE 500 error.")
    log.debug("Balrog version is: %s", version)
    log.debug("Request path is: %s", request.path)
    log.debug("Request environment is: %s", request.environ)
    log.debug("Request headers are: %s", request.headers)
    return error

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
