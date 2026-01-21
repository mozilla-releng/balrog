import re

from auslib.errors import BadDataError

# Version/StrictVersion/LooseVersion classes are lifted from distutils which
# deprecated them


class Version:
    def __init__(self, vstring=None):
        if vstring:
            self.parse(vstring)

    def parse(self, vstring):
        return NotImplemented

    def __repr__(self):
        return "{} ('{}')".format(self.__class__.__name__, str(self))

    def __eq__(self, other):
        c = self._cmp(other)
        if c is NotImplemented:
            return c
        return c == 0

    def __lt__(self, other):
        c = self._cmp(other)
        if c is NotImplemented:
            return c
        return c < 0

    def __le__(self, other):
        c = self._cmp(other)
        if c is NotImplemented:
            return c
        return c <= 0

    def __gt__(self, other):
        c = self._cmp(other)
        if c is NotImplemented:
            return c
        return c > 0

    def __ge__(self, other):
        c = self._cmp(other)
        if c is NotImplemented:
            return c
        return c >= 0


class StrictVersion(Version):
    version_re = re.compile(r"^(\d+) \. (\d+) (\. (\d+))? ([ab](\d+))?$", re.VERBOSE | re.ASCII)

    def parse(self, vstring):
        match = self.version_re.match(vstring)
        if not match:
            raise ValueError("invalid version number '%s'" % vstring)

        (major, minor, patch, prerelease, prerelease_num) = match.group(1, 2, 4, 5, 6)

        if patch:
            self.version = tuple(map(int, [major, minor, patch]))
        else:
            self.version = tuple(map(int, [major, minor])) + (0,)

        if prerelease:
            self.prerelease = (prerelease[0], int(prerelease_num))
        else:
            self.prerelease = None

    def __str__(self):
        if self.version[2] == 0:
            vstring = ".".join(map(str, self.version[0:2]))
        else:
            vstring = ".".join(map(str, self.version))

        if self.prerelease:
            vstring = vstring + self.prerelease[0] + str(self.prerelease[1])

        return vstring

    def _cmp(self, other):
        if isinstance(other, str):
            other = StrictVersion(other)
        elif not isinstance(other, StrictVersion):
            return NotImplemented

        if self.version != other.version:
            # numeric versions don't match
            # prerelease stuff doesn't matter
            if self.version < other.version:
                return -1
            else:
                return 1

        # have to compare prerelease
        # case 1: neither has prerelease; they're equal
        # case 2: self has prerelease, other doesn't; other is greater
        # case 3: self doesn't have prerelease, other does: self is greater
        # case 4: both have prerelease: must compare them!

        if not self.prerelease and not other.prerelease:
            return 0
        elif self.prerelease and not other.prerelease:
            return -1
        elif not self.prerelease and other.prerelease:
            return 1
        elif self.prerelease and other.prerelease:
            if self.prerelease == other.prerelease:
                return 0
            elif self.prerelease < other.prerelease:
                return -1
            else:
                return 1
        else:
            assert False, "never get here"


class LooseVersion(Version):
    component_re = re.compile(r"(\d+ | [a-z]+ | \.)", re.VERBOSE)

    def parse(self, vstring):
        # I've given up on thinking I can reconstruct the version string
        # from the parsed tuple -- so I just store the string here for
        # use by __str__
        self.vstring = vstring
        components = [x for x in self.component_re.split(vstring) if x and x != "."]
        for i, obj in enumerate(components):
            try:
                components[i] = int(obj)
            except ValueError:
                pass

        self.version = components

    def __str__(self):
        return self.vstring

    def __repr__(self):
        return "LooseVersion ('%s')" % str(self)

    def _cmp(self, other):
        if isinstance(other, str):
            other = LooseVersion(other)
        elif not isinstance(other, LooseVersion):
            return NotImplemented

        if self.version == other.version:
            return 0
        if self.version < other.version:
            return -1
        if self.version > other.version:
            return 1


def FirefoxVPNVersion(version):
    """
    Versions of FirefoxVPN are x.y.z, except some old versions that are x.y.
    """
    try:
        return StrictVersion(version)
    except ValueError:
        raise BadDataError(f"Invalid app version {version}")


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
    except ValueError as e:
        raise BadDataError(e)


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
        return FirefoxVPNVersion

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
