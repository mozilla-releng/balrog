import operator
import re

from auslib.util.versions import MozillaVersion

operators = {">=": operator.ge, ">": operator.gt, "<": operator.lt, "<=": operator.le}


def strip_operator(value):
    return value.lstrip("<>=")


def has_operator(value):
    return value.startswith(("<", ">"))


def glob_op(value, operand):
    """Compare a string or StrictVersion against a glob stripped of its `*`.
    Currently only supported in version_compare."""
    return value.startswith(operand)


def get_op(pattern):
    if pattern.endswith(".*"):
        return glob_op, pattern.rstrip("*")
    # only alphanumeric characters means no operator
    if re.match(r"\w+", pattern):
        return operator.eq, pattern
    for op in operators:
        m = re.match(r"(%s)([\.\w]+)" % op, pattern)
        if m:
            op, operand = m.groups()
            return operators[op], operand


def string_compare(value, compstr):
    """Do a string comparison of a bare string with another,
    which may carry a comparison operator.
    eg string_compare('a', '>b') is False
    """
    opfunc, operand = get_op(compstr)
    return opfunc(value, operand)


def int_compare(value, compstr):
    """Do a int comparison of a bare int with another,
    which may carry a comparison operator.
    eg int_compare(1, '>2') is False
    """
    opfunc, operand = get_op(compstr)
    return opfunc(value, int(operand))


def version_compare(value, compstr, versionClass=MozillaVersion):
    """Do a version comparison between a string (representing a version),
    with another which may carry a comparison operator. A true version
    comparison is done.
    eg version_compare('1.1', '>1.0') is True
    """
    opfunc, operand = get_op(compstr)
    if opfunc is not glob_op:
        # `StrictVersion.__str__` drops the final digit if it's a 0. For example,
        #     str(StrictVersion(80.0.0)) -> "80.0"
        # This breaks if we want to match 80.0.0 (80.0) against `80.0.*`:
        #     "80.0".startswith("80.0.") -> False
        # Similarly, if we strip the final `.` from the glob, e.g.
        #     "80.0".startswith("80.0") -> True
        # then 80.10.0 will match 80.1.*:
        #     "80.10".startswith("80.1") -> True
        # We can either try to reverse engineer StrictVersion's intelligent
        # version string manipulation, or just not cast `value` to
        # `versionClass` if we're using `glob_op`.
        value = versionClass(value)
        # The glob operand doesn't match StrictVersion's strict version rules,
        # whether we strip the `*` from it or not, so casting it as a
        # `versionClass` will throw an exception unless we create a new
        # StrictVersion based class that accepts those versions.
        # Let's do a string comparison in `glob_op` instead.
        operand = versionClass(operand)
    return opfunc(value, operand)
