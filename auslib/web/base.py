import logging
log = logging.getLogger(__name__)

from flask import Flask, make_response, send_from_directory

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

# TODO: kill this with fire, brimstone, and extreme prejudice when bug 1013354 is fixed.
from auslib import dbo
from flask import Response
@app.route("/update/3/GMP/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/update.xml")
def hackyH264URLs(version, buildID, buildTarget, **crap):
    try:
        blob = dbo.db.releases.getReleaseBlob("HackyH264Blob")
    except KeyError:
        response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
        response.mimetype = 'text/xml'
        return response

    xml = blob.get("ftpFilenames", {}).get("completes", {}).get("%s-%s" % (version, buildTarget))
    if xml:
        resp = make_response('<?xml version="1.0"?>\n' + xml)
        resp.mimetype = "text/xml"
        return resp
    else:
        response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
        response.mimetype = 'text/xml'
        return response
