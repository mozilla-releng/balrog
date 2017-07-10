import operator
import re

from auslib.util.versions import MozillaVersion

operators = {
    '>=': operator.ge,
    '>': operator.gt,
    '<': operator.lt,
    '<=': operator.le,
}


def get_op(pattern):
    # only alphanumeric characters means no operator
    if re.match('\w+', pattern):
        return operator.eq, pattern
    for op in operators:
        m = re.match('(%s)([\.\w]+)' % op, pattern)
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


def version_compare(value, compstr):
    """Do a version comparison between a string (representing a version),
    with another which may carry a comparison operator. A true version
    comparison is done.
      eg version_compare('1.1', '>1.0') is True
    """
    opfunc, operand = get_op(compstr)
    value = MozillaVersion(value)
    operand = MozillaVersion(operand)
    return opfunc(value, operand)
