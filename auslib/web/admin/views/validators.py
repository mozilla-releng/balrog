from jsonschema import draft4_format_checker
from jsonschema.compat import str_types
# To be able to Differentitate from wftForms.ValidationError.
from jsonschema import ValidationError as JsonSchemaValidationError
from auslib.util.comparison import get_op
from auslib.util.timestamp import getMillisecondTimestamp
from auslib.util.versions import MozillaVersion
from connexion.decorators.validation import RequestBodyValidator
from connexion.utils import is_null
from connexion import problem
import operator
import json
import logging

logger = logging.getLogger(__name__)


class BalrogRequestBodyValidator(RequestBodyValidator):
    def validate_schema(self, data, url):
        # type: (dict, AnyStr) -> Union[ConnexionResponse, None]
        if self.is_null_value_valid and is_null(data):
            return None
        try:
            self.validator.validate(data)
        except JsonSchemaValidationError as exception:
            # Add field name to the error response
            exception_field = ''
            for i in exception.path:
                exception_field = i + ': '
            if exception.__cause__ is not None:
                exception_message = str(exception.__cause__.message) + ' ' + exception_field + str(exception.message)
            else:
                exception_message = exception_field + str(exception.message)
            logger.error("{url} validation error: {error}".
                         format(url=url, error=exception_message))
            return problem(400, 'Bad Request', exception_message)

        return None


@draft4_format_checker.checks(format="buildID", raises=JsonSchemaValidationError)
def operator_validator(field_value):
    logger.debug('starting in operator_validator: buildID is %s' % field_value)
    if not isinstance(field_value, str_types):
        return True
    # empty input is fine
    if field_value is None or field_value == '':
        return True
    try:
        op, operand = get_op(field_value)
        logger.debug('Got (%s, %s) from get_op', op, operand)
    except TypeError:
        # get_op field returns None if no operator or no match, can't be unpacked
        raise JsonSchemaValidationError("Invalid input for buildID : %s. No Operator or Match found." % field_value)
    return True


@draft4_format_checker.checks(format="version", raises=JsonSchemaValidationError)
def version_validator(field_value):
    logger.debug('starting in version_validator: version data is %s' % field_value)
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
                raise JsonSchemaValidationError('Invalid input for %s .Relational Operators are not allowed'
                                                ' when providing a list of versions.' % field_value)
            version = MozillaVersion(operand)
        except JsonSchemaValidationError:
            raise
        except ValueError:
            raise JsonSchemaValidationError("ValueError. Couldn't parse version for %s. Invalid '%s' input value"
                                            % (field_value, field_value))
        except:
            raise JsonSchemaValidationError('Invalid input for %s . No Operator or Match found.' % field_value)
        # MozillaVersion doesn't error on empty strings
        if not hasattr(version, 'version'):
            raise JsonSchemaValidationError("Couldn't parse the version for %s. No attribute 'version' was detected."
                                            % field_value)
    return True


@draft4_format_checker.checks(format="JSONStringField", raises=JsonSchemaValidationError)
def json_field_validator(field_value):
    logger.debug('starting in json_field_validator: input json is %s' % field_value)
    if not isinstance(field_value, str_types):
        return True
    # empty input is fine
    if field_value is None or field_value == '':
        return True
    try:
        json.loads(field_value)
    except ValueError as e:
        raise JsonSchemaValidationError("Not a valid json. Error: %s." % str(e.args[0]))
    return True


def integer_and_range_validator(field_name, field_value, min_val=None, max_val=None):
    if not isinstance(field_value, str_types) and not isinstance(field_value, int) and field_value is not None:
        return False
    # empty input is fine
    if field_value is None or field_value == '':
        return True
    try:
        x = int(field_value)
    except:
        raise JsonSchemaValidationError(message="Invalid input for %s. Not an integer." % field_name)
    if min_val is not None and x < min_val:
        raise JsonSchemaValidationError(message="%s field value should be an integer >= %s" % (field_name, min_val))
    if max_val is not None and x > max_val:
        raise JsonSchemaValidationError(message="%s field value should be an integer <= %s" % (field_name, max_val))
    return True


@draft4_format_checker.checks(format="telemetry_uptake", raises=JsonSchemaValidationError)
def telemetry_uptake_validator(field_value):
    if field_value is not None and field_value != '':
        logger.debug('starting in telemetry_uptake_validator: telemetry_uptake is %s' % field_value)
    return integer_and_range_validator("telemetry_uptake", field_value, 0)


@draft4_format_checker.checks(format="when", raises=JsonSchemaValidationError)
def sc_when_validator(field_value):
    if field_value is not None and field_value != '':
        logger.debug('starting in sc_when_validator: when value: %s' % field_value)
    return integer_and_range_validator("when", field_value, 0)


@draft4_format_checker.checks(format="data_version", raises=JsonSchemaValidationError)
def data_version_validator(field_value):
    if field_value is not None and field_value != '':
        logger.debug('starting in data_version_validator: data_version is %s' % field_value)
    return integer_and_range_validator("data_version", field_value, 1)


@draft4_format_checker.checks(format="rule_id", raises=JsonSchemaValidationError)
def rule_id_validator(field_value):
    if field_value is not None and field_value != '':
        logger.debug('starting in rule_id_validator: rule_id is %s' % field_value)
    return integer_and_range_validator("rule_id", field_value, 0)


@draft4_format_checker.checks(format="data_version", raises=JsonSchemaValidationError)
def data_version_validator(field_value):
    if field_value is not None and field_value != '':
        logger.debug('starting in data_version_validator: data_version is %s' % field_value)
    return integer_and_range_validator("data_version", field_value, 1)


@draft4_format_checker.checks(format="rule_id", raises=JsonSchemaValidationError)
def rule_id_validator(field_value):
    if field_value is not None and field_value != '':
        logger.debug('starting in rule_id_validator: rule_id is %s' % field_value)
    return integer_and_range_validator("rule_id", field_value, 0)


@draft4_format_checker.checks(format="signoffs_required", raises=JsonSchemaValidationError)
def signoffs_required_validator(field_value):
    if field_value is not None and field_value != '':
        logger.debug('starting in signoffs_required_validator: signoffs_required is %s' % field_value)
    return integer_and_range_validator("signoffs_required", field_value, 1)


def is_when_present_and_in_past_validator(what):
    """Validates if scheduled_change_time value i.e. 'when' field value is present in
    input dictionary/object and if its value is in past or not"""
    return what.get("when", None) and int(what.get("when")) < getMillisecondTimestamp()
