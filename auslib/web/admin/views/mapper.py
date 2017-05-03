from auslib.web.admin.views.csrf import CSRFView
from auslib.web.admin.views.rules import RulesAPIView
from auslib.web.admin.views.permissions import UsersView
from jsonschema import draft4_format_checker
from jsonschema.compat import str_types
from wtforms.validators import ValidationError
from auslib.util.comparison import get_op
from auslib.util.versions import MozillaVersion
import operator
import logging

log = logging.getLogger(__name__)


def csrf_get():
    return CSRFView().get()


def rules_get():
    return RulesAPIView().get()


def rules_post():
    return RulesAPIView().post()


def users_get():
    return UsersView().get()


@draft4_format_checker.checks(format="buildID", raises=ValidationError)
def operator_validator(field_value):
    log.debug('starting in operator_validator: buildID is %s' % field_value)
    if not isinstance(field_value, str_types):
        return True
    # empty input is fine
    if field_value is None or field_value == '':
        return True
    try:
        op, operand = get_op(field_value)
        log.debug('Got (%s, %s) from get_op', op, operand)
    except TypeError:
        # get_op field returns None if no operator or no match, can't be unpacked
        raise ValidationError("Invalid input for buildID : %s. No Operator or Match found." % field_value)
    return True


@draft4_format_checker.checks(format="version", raises=ValidationError)
def version_validator(field_value):
    log.debug('starting in version_validator: version data is %s' % field_value)
    if not isinstance(field_value, str_types):
        return True
    # empty input is fine
    if field_value is None or field_value == '':
        return True
    rules_version_list = field_value.split(",")
    is_list_of_versions = len(rules_version_list) > 1
    for rule_version in rules_version_list:
        try:
            op, operand = get_op(rule_version)
            if is_list_of_versions and op != operator.eq:
                raise ValidationError('Invalid input for %s .Relational Operators are not allowed'
                                      ' when providing a list of versions.' % field_value)
            version = MozillaVersion(operand)
        except ValidationError:
            raise
        except ValueError:
            raise ValidationError("ValueError. Couldn't parse version for %s. Invalid '%s' input value"
                                  % (field_value, field_value))
        except:
            raise ValidationError('Invalid input for %s . No Operator or Match found.' % field_value)
        # MozillaVersion doesn't error on empty strings
        if not hasattr(version, 'version'):
            raise ValidationError("Couldn't parse the version for %s. No attribute 'version' was detected."
                                  % field_value)
    return True
