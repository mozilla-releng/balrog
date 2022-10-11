import json
import logging
import operator

import jsonschema
from jsonschema.validators import Draft4Validator

from auslib.util.comparison import get_op, strip_operator
from auslib.util.versions import MozillaVersion

logger = logging.getLogger(__name__)


@Draft4Validator.FORMAT_CHECKER.checks(format="buildID", raises=jsonschema.ValidationError)
def operator_validator(field_value):
    logger.debug("starting in operator_validator: buildID is %s" % field_value)
    if not isinstance(field_value, str):
        return True
    # empty input is fine
    if field_value is None or field_value == "":
        return True
    try:
        op, operand = get_op(field_value)
        logger.debug("Got (%s, %s) from get_op", op, operand)
    except TypeError:
        # get_op field returns None if no operator or no match, can't be unpacked
        raise jsonschema.ValidationError("Invalid input for buildID : %s. No Operator or Match found." % field_value)
    try:
        int(strip_operator(field_value))
    except ValueError:
        raise jsonschema.ValidationError("Invalid input for buildID: must be an integer.")
    return True


@Draft4Validator.FORMAT_CHECKER.checks(format="version", raises=jsonschema.ValidationError)
def version_validator(field_value):
    logger.debug("starting in version_validator: version data is %s" % field_value)
    if not isinstance(field_value, str):
        return True
    # empty input is fine
    if field_value is None or field_value == "":
        return True
    rules_version_list = field_value.split(",")
    is_list_of_versions = len(rules_version_list) > 1
    for rule_version in rules_version_list:
        try:
            op, operand = get_op(rule_version)
            if is_list_of_versions and op != operator.eq:
                raise jsonschema.ValidationError(
                    "Invalid input for %s .Relational Operators are not allowed" " when providing a list of versions." % field_value
                )
            version = MozillaVersion(operand)
        except jsonschema.ValidationError:
            raise
        except ValueError:
            raise jsonschema.ValidationError("ValueError. Couldn't parse version for %s. Invalid '%s' input value" % (field_value, field_value))
        except Exception:
            raise jsonschema.ValidationError("Invalid input for %s . No Operator or Match found." % field_value)
        # MozillaVersion doesn't error on empty strings
        if not hasattr(version, "version"):
            raise jsonschema.ValidationError("Couldn't parse the version for %s. No attribute 'version' was detected." % field_value)
    return True


@Draft4Validator.FORMAT_CHECKER.checks(format="JSONStringField", raises=jsonschema.ValidationError)
def json_field_validator(field_value):
    logger.debug("starting in json_field_validator: input json is %s" % field_value)
    if not isinstance(field_value, str):
        return True
    # empty input is fine
    if field_value is None or field_value == "":
        return True
    try:
        json.loads(field_value)
    except ValueError as e:
        raise jsonschema.ValidationError("Not a valid json. Error: %s." % str(e.args[0]))
    return True


def integer_and_range_validator(field_name, field_value, min_val=None, max_val=None):
    if not isinstance(field_value, str) and not isinstance(field_value, int) and field_value is not None:
        return False
    # empty input is fine
    if field_value is None or field_value == "":
        return True
    try:
        x = int(field_value)
    except Exception:
        raise jsonschema.ValidationError(message="Invalid input for %s. Not an integer." % field_name)
    if min_val is not None and x < min_val:
        raise jsonschema.ValidationError(message="%s field value should be an integer >= %s" % (field_name, min_val))
    if max_val is not None and x > max_val:
        raise jsonschema.ValidationError(message="%s field value should be an integer <= %s" % (field_name, max_val))
    return True


@Draft4Validator.FORMAT_CHECKER.checks(format="telemetry_uptake", raises=jsonschema.ValidationError)
def telemetry_uptake_validator(field_value):
    if field_value is not None and field_value != "":
        logger.debug("starting in telemetry_uptake_validator: telemetry_uptake is %s" % field_value)
    return integer_and_range_validator("telemetry_uptake", field_value, 0)


@Draft4Validator.FORMAT_CHECKER.checks(format="when", raises=jsonschema.ValidationError)
def sc_when_validator(field_value):
    if field_value is not None and field_value != "":
        logger.debug("starting in sc_when_validator: when value: %s" % field_value)
    return integer_and_range_validator("when", field_value, 0)


@Draft4Validator.FORMAT_CHECKER.checks(format="priority", raises=jsonschema.ValidationError)
def priority_validator(field_value):
    if field_value is not None and field_value != "":
        logger.debug("starting in priority_validator: priority is %s" % field_value)
    return integer_and_range_validator("priority", field_value, 0)


@Draft4Validator.FORMAT_CHECKER.checks(format="backgroundRate", raises=jsonschema.ValidationError)
def background_rate_validator(field_value):
    if field_value is not None and field_value != "":
        logger.debug("starting in backgroundRate_validator: backgroundRate is %s" % field_value)
    return integer_and_range_validator("backgroundRate", field_value, 0, 100)


@Draft4Validator.FORMAT_CHECKER.checks(format="data_version", raises=jsonschema.ValidationError)
def data_version_validator(field_value):
    if field_value is not None and field_value != "":
        logger.debug("starting in data_version_validator: data_version is %s" % field_value)
    return integer_and_range_validator("data_version", field_value, 1)


@Draft4Validator.FORMAT_CHECKER.checks(format="rule_id", raises=jsonschema.ValidationError)
def rule_id_validator(field_value):
    if field_value is not None and field_value != "":
        logger.debug("starting in rule_id_validator: rule_id is %s" % field_value)
    return integer_and_range_validator("rule_id", field_value, 0)


@Draft4Validator.FORMAT_CHECKER.checks(format="signoffs_required", raises=jsonschema.ValidationError)
def signoffs_required_validator(field_value):
    if field_value is not None and field_value != "":
        logger.debug("starting in signoffs_required_validator: signoffs_required is %s" % field_value)
    return integer_and_range_validator("signoffs_required", field_value, 1)


# TODO: Remove this after Balrog properly supports unicode. This is kindof a hacky workaround
# for the problem described in https://bugzilla.mozilla.org/show_bug.cgi?id=1457893.
@Draft4Validator.FORMAT_CHECKER.checks(format="ascii", raises=jsonschema.ValidationError)
def ascii_validator(field_value):
    if field_value is None or field_value == "":
        return True
    try:
        field_value.encode("ascii")
    except UnicodeEncodeError:
        raise jsonschema.ValidationError("value must be ascii")

    return True
