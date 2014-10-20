from distutils.version import StrictVersion
import re


class ModernMozillaVersion(StrictVersion):
    """A version class that is slightly less restrictive than StrictVersion.
       Instead of just allowing "a" or "b" as prerelease tags, it allows any
       alpha. This allows us to support the once-shipped "3.6.3plugin1" and
       similar versions."""
    version_re = re.compile(r"""^(\d+) \. (\d+) (\. (\d+))?
                                ([a-zA-Z]+(\d+))?$""", re.VERBOSE)


class AncientMozillaVersion(StrictVersion):
    """A version class that is slightly less restrictive than StrictVersion.
       Instead of just allowing "a" or "b" as prerelease tags, it allows any
       alpha. This allows us to support the once-shipped "3.6.3plugin1" and
       similar versions.
       It also supports versions w.x.y.z by transmuting to w.x.z, which
       is useful for versions like 1.5.0.x and 2.0.0.y"""
    version_re = re.compile(r"""^(\d+) \. (\d+) \. \d (\. (\d+))
                                ([a-zA-Z]+(\d+))?$""", re.VERBOSE)


def MozillaVersion(version):
    try:
        return ModernMozillaVersion(version)
    except ValueError:
        if version.count('.') == 3:
            return AncientMozillaVersion(version)
        else:
            raise
