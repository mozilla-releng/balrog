import sys

if sys.version_info.major == 2:
    # No in-repo client for python 2 yet
    pass
elif sys.version_info.major == 3:
    if sys.version_info.minor == 5:
        from .client_py35 import *
    else:
        raise Exception("Python 3.5 is required.")
