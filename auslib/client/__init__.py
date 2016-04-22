import logging
import sys

if sys.version_info >= (3, 5):
    from .client_py35 import *  # noqa
else:
    logging.warning("No client available for this version of Python.")
