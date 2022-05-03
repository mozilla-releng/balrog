import re
from distutils.version import LooseVersion, StrictVersion, Version

from auslib.errors import BadDataError


class PostModernMozillaVersion(StrictVersion):
    """A version class that supports Firefox versions 5.0 and up, which
    may have "a1" but not "b2" tags in them"""

    version_re = re.compile(
        r"""^(\d+) \. (\d+) (\. (\d+))?
                                (a(\d+))?$""",
        re.VERBOSE,
    )


class ModernMozillaVersion(StrictVersion):
    """A version class that is slightly less restrictive than StrictVersion.
    Instead of just allowing "a" or "b" as prerelease tags, it allows any
    alpha. This allows us to support the once-shipped "3.6.3plugin1" and
    similar versions."""

    version_re = re.compile(
        r"""^(\d+) \. (\d+) (\. (\d+))?
                                ([a-zA-Z]+(\d+))?$""",
        re.VERBOSE,
    )


class AncientMozillaVersion(StrictVersion):
    """A version class that is slightly less restrictive than StrictVersion.
    Instead of just allowing "a" or "b" as prerelease tags, it allows any
    alpha. This allows us to support the once-shipped "3.6.3plugin1" and
    similar versions.
    It also supports versions w.x.y.z by transmuting to w.x.z, which
    is useful for versions like 1.5.0.x and 2.0.0.y"""

    version_re = re.compile(
        r"""^(\d+) \. (\d+) \. \d (\. (\d+))
                                ([a-zA-Z]+(\d+))?$""",
        re.VERBOSE,
    )


class GlobVersionTuple(tuple):
    def __eq__(self, value):
        if len(value) < len(self):
            return False
        for i, j in enumerate(self):
            if j != value[i]:
                return False
        return True

    def __ne__(self, value):
        return not self.__eq__(value)


class GlobVersion(StrictVersion):
    """A version class that supports Firefox versions 5.0 and up, which ends
    with a glob `*`. Not really a StrictVersion at all, but it needs to be
    to compare with other MozillaVersions."""

    version_re = re.compile(
        r"""^(\d+) \. (\d+\.\*|\*)$""",
        re.VERBOSE,
    )
    prerelease = None

    def parse(self, vstring):
        self.vstring = vstring
        match = self.version_re.match(vstring)
        if not match:
            raise ValueError("invalid version number '%s'" % vstring)
        parts = [int(i) for i in vstring.split(".") if i != "*"]
        self.version = GlobVersionTuple(parts)

    def __eq__(self, value):
        return str(value).startswith(self.vstring.rstrip("*"))

    def __str__(self):
        return self.vstring


def MozillaVersion(version):
    try:
        if version.count(".") in (1, 2):
            if int(version.split(".")[0]) > 4:
                if version.endswith(".*"):
                    return GlobVersion(version)
                return PostModernMozillaVersion(version)
            else:
                return ModernMozillaVersion(version)
        else:
            return AncientMozillaVersion(version)
    except ValueError:
        raise BadDataError("Version number %s is invalid." % version)


def get_version_parts(version):
    return [int(v) for v in version.split(".")]


def increment_version(version):
    """Increments a version to its 'next' version by adding one to the last
    part of the version."""

    parts = get_version_parts(version)
    parts[-1] += 1
    return ".".join(map(str, parts))


def decrement_version(version):
    """Decrements a version to its 'previous' version by subtracting one from
    its last part. If the last part is 0, it is changed to 999, and the second
    last part is subtracted by one. This is repeated until subtraction happens
    or we run out of parts."""

    parts = get_version_parts(version)
    for i in reversed(range(len(parts))):
        if parts[i] == 0:
            if i == 0:
                raise BadDataError("Version number %s is invalid: all 0's." % version)
            # Horrible assumption! Doesn't work if incoming versions have parts
            # that are greater than 999. But that will never happen....
            parts[i] = 999
        else:
            parts[i] -= 1
            break
    return ".".join(map(str, parts))


def get_version_class(product):
    if product in ("FirefoxVPN", "Guardian"):
        return LooseVersion

    return MozillaVersion


class PinVersion(Version):
    """A version class that supports application update pins. These are used for
    pinning an install to a particular version (see Bug 1529943). Update pins
    are formatted like 'X.' or 'X.Y.', where X is the major version and Y is the
    minor version.

    Note that unlike the other version types in this file, this one does not
    derive from StrictVersion. This is because this is not a strict version and
    it should not be treated as such. '100.', for example, is equal to '100.0.0'
    and '100.99.99'. It is less than '101.0.0' and greater than '99.99.99'.
    Deriving from StrictVersion would allow StrictVersion's operators to operate
    on PinVersions, which would not function correctly.
    Despite these differences, the PinVersion interface is identical to that of
    StrictVersion and PinVersions can be compared to StrictVersions because
    PinVersion provides the necessary operators.

    This class is very similar to GlobVersion, but needs to be separate.
    GlobVersion comparisons must be made via
    auslib.util.comparison.version_compare, which only supports equality
    checking for GlobVersion."""

    version_re = re.compile(r"^(\d+) \. ((\d+) \.)?$", re.VERBOSE)

    def parse(self, vstring):
        match = self.version_re.match(vstring)
        if not match:
            raise ValueError(f"Invalid pin version '{vstring}'")

        version = list(match.group(1, 3))
        if version[-1] is None:
            version.pop()
        self.version = tuple(map(int, version))

    def __str__(self):
        vstring = ""
        for part in self.version:
            vstring += f"{part}."
        return vstring

    def _cmp(self, other):
        if not isinstance(other, StrictVersion):
            return NotImplemented
        if isinstance(other, GlobVersion):
            # This would require some extra handling. Since this type of
            # comparison isn't currently needed, explicitly do not handle it.
            return NotImplemented

        if len(other.version) < len(self.version):
            # StrictVersions should have a version tuple that is 3 elements
            # long, whereas PinVersions should have a version tuple 1 or 2
            # elements long. It's conceivable that we could subclass
            # StrictVersion in a way that breaks this assumption, in which case
            # we would need to determine what it means to compare, for example,
            # PinVersion("100.0.") and StrictVersion("100").
            raise ValueError("len(StrictVersion.version) is expected to be 3.")

        other_trimmed_version = other.version[: len(self.version)]
        if self.version < other_trimmed_version:
            return -1
        elif self.version > other_trimmed_version:
            return 1
        return 0
