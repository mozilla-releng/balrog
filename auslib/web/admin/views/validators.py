from jsonschema import draft4_format_checker
from jsonschema.compat import str_types
# To be able to Differentitate from wftForms.ValiddationError.
from jsonschema import ValidationError as JsonschemaValidationError
from auslib.util.comparison import get_op
from auslib.util.versions import MozillaVersion
from connexion.decorators.validation import RequestBodyValidator
from connexion.utils import all_json, is_null
from connexion import problem
import operator
import logging
import functools

logger = logging.getLogger(__name__)


class BalrogRequestBodyValidator(RequestBodyValidator):
    def __call__(self, func):
        """
        :type func: types.FunctionType
        :rtype: types.FunctionType
        """

        @functools.wraps(func)
        def wrapper(request):
            if all_json(self.consumes):
                data = request.json
                if data is None and len(request.body) > 0 and not self.is_null_value_valid:
                    # the body has contents that were not parsed as JSON
                    return problem(415,
                                   "Unsupported Media Type",
                                   "Invalid Content-type ({content_type}), expected JSON data".format(
                                       content_type=request.headers["Content-Type"]
                                   ))

                logger.debug("%s validating schema...", request.url)
                error = self.validate_schema(data, request.url)
                if error and not self.has_default:
                    return error

            response = func(request)
            return response

        return wrapper

    def validate_schema(self, data, url):
        # type: (dict, AnyStr) -> Union[ConnexionResponse, None]
        if self.is_null_value_valid and is_null(data):
            return None
        print data
        try:
            self.validator.validate(data)
        except JsonschemaValidationError as exception:
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


@draft4_format_checker.checks(format="buildID", raises=JsonschemaValidationError)
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
        raise JsonschemaValidationError("Invalid input for buildID : %s. No Operator or Match found." % field_value)
    return True


@draft4_format_checker.checks(format="version", raises=JsonschemaValidationError)
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
                raise JsonschemaValidationError('Invalid input for %s .Relational Operators are not allowed'
                                                ' when providing a list of versions.' % field_value)
            version = MozillaVersion(operand)
        except JsonschemaValidationError:
            raise
        except ValueError:
            raise JsonschemaValidationError("ValueError. Couldn't parse version for %s. Invalid '%s' input value"
                                            % (field_value, field_value))
        except:
            raise JsonschemaValidationError('Invalid input for %s . No Operator or Match found.' % field_value)
        # MozillaVersion doesn't error on empty strings
        if not hasattr(version, 'version'):
            raise JsonschemaValidationError("Couldn't parse the version for %s. No attribute 'version' was detected."
                                            % field_value)
    return True


@draft4_format_checker.checks(format="priority", raises=JsonschemaValidationError)
def priority_validator(field_value):
    logger.debug('starting in priority_validator: field data is %s' % field_value)
    if not isinstance(field_value, str_types) and not isinstance(field_value, int) and field_value is not None:
        return False
    # empty input is fine
    if field_value is None or field_value == '':
        return True
    try:
        x = int(field_value)
    except:
        raise JsonschemaValidationError('Invalid input %s for priority.Not an integer.' % field_value)
    if x < 0:
        raise JsonschemaValidationError("Priority field value %s shouldn't be less than 0" % field_value)
    return True


@draft4_format_checker.checks(format="backgroundRate", raises=JsonschemaValidationError)
def background_rate_validator(field_value):
    logger.debug('starting in backgroundRate_validator: field data is %s' % field_value)
    if not isinstance(field_value, str_types) and not isinstance(field_value, int) and field_value is not None:
        return False
    # empty input is fine
    if field_value is None or field_value == '':
        return True
    try:
        x = int(field_value)
    except:
        raise JsonschemaValidationError(message=('Invalid input %s for backgroundRate. Not an integer.' % field_value))
    if x < 0 or x > 100:
        raise JsonschemaValidationError(message="backgroundRate field value should be in range 0-100")
    return True
