from distutils.version import StrictVersion
import re

class MozillaVersion(StrictVersion):
    """A version class that is slightly less restrictive than StrictVersion.
       Instead of just allowing "a" or "b" as prerelease tags, it allows any
       alpha. This allows us to support the once-shipped "3.6.3plugin1" and
       similar versions."""
    version_re = re.compile(r'^(\d+) \. (\d+) (\. (\d+))? ([a-zA-Z]+(\d+))?$', re.VERBOSE)
