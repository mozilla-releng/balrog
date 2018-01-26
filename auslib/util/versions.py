from distutils.version import StrictVersion
import re

from auslib.errors import BadDataError


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
        pass
    try:
        if version.count('.') == 3:
            return AncientMozillaVersion(version)
    except ValueError:
        pass
    raise BadDataError("Version number %s is invalid." % version)


def increment_version(version):
    """Increments a version to its 'next' version by adding one to the last
    part of the version."""

    parts = map(int, version.split("."))
    parts[-1] += 1
    return ".".join(map(str, parts))


def decrement_version(version):
    """Decrements a version to its 'previous' version by subtracting one from
    its last part. If the last part is 0, it is changed to 99, and the second
    last part is subtracted by one. This is repeated until subtraction happens
    or we run out of parts."""

    parts = map(int, version.split("."))
    for i in reversed(range(len(parts))):
        if parts[i] == 0:
            # Horrible assumption! Doesn't work if incoming versions have parts
            # that are greater than 99. But that will never happen....
            parts[i] = 99
        else:
            parts[i] -= 1
            break
    return ".".join(map(str, parts))
