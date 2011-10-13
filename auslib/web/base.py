from flask import Flask

from auslib.db import AUSDatabase

app = Flask(__name__)
db = AUSDatabase()

# All of our View modules contain routing information that needs to be imported
# to be active.
from auslib.web.views.permissions import *
