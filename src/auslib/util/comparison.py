import operator
import re

from auslib.util.versions import MozillaVersion

operators = {">=": operator.ge, ">": operator.gt, "<": operator.lt, "<=": operator.le}


def strip_operator(value):
    return value.lstrip("<>=")


def has_operator(value):
    return value.startswith(("<", ">"))


def either_eq(value, operand):
    """The order of eq matters with GlobVersion; test both orders.

    Nightly: because StrictVersion also compares self.prerelease,
             StrictVersion("70.0a1") != GlobVersion("70.*"), but
             GlobVersion("70.*") == StrictVersion("70.0a1")

    dot-0: because StrictVersion can drop the trailing .0,
           GlobVersion("80.0.*") != StrictVersion("80.0.0"), but
           StrictVersion("80.0.0") == GlobVersion("80.0.*")

    Because of this, let's test eq in both directions.

    """
    return operator.eq(value, operand) or operator.eq(operand, value)


def get_op(pattern):
    # ending with a glob means either_eq
    if pattern.endswith("*"):
        return either_eq, pattern
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
    value = versionClass(value)
    operand = versionClass(operand)
    return opfunc(value, operand)
