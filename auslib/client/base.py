from flask import Flask, make_response

from auslib.AUS import AUS3

app = Flask(__name__)
AUS = AUS3()

@app.errorhandler(404)
def fourohfour(error):
    """We don't return 404s in AUS. Instead, we return empty XML files"""
    response = make_response('<?xml version="1.0"?>\n<updates>\n</updates>')
    response.mimetype = 'text/xml'
    return response

from auslib.client.views.client import *
