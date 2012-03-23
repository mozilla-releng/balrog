from flask import Flask, request

from auslib import version
from auslib.db import AUSDatabase

app = Flask(__name__)
db = AUSDatabase()

@app.errorhandler(500)
def isa(error):
    log.error("Caught ISA 500 error.")
    log.debug("Balrog version is: %s", version)
    log.debug("Request path is: %s", request.path)
    log.debug("Request environment is: %s", request.environ)
    log.debug("Request headers are: %s", request.headers)
    return error

# All of our View modules contain routing information that needs to be imported
# to be active.
from auslib.web.views import *
