from connexion.decorators.validation import RequestBodyValidator
from connexion.utils import is_null
from connexion import problem
import logging
import jsonschema

from auslib.util.timestamp import getMillisecondTimestamp
# To enable shared jsonschema validators
import auslib.util.jsonschema_validators # noqa

logger = logging.getLogger(__name__)


class BalrogRequestBodyValidator(RequestBodyValidator):
    def validate_schema(self, data, url):
        # type: (dict, AnyStr) -> Union[ConnexionResponse, None]
        if self.is_null_value_valid and is_null(data):
            return None
        try:
            self.validator.validate(data)
        except jsonschema.ValidationError as exception:
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


def is_when_present_and_in_past_validator(what):
    """Validates if scheduled_change_time value i.e. 'when' field value is present in
    input dictionary/object and if its value is in past or not"""
    return what.get("when", None) and int(what.get("when")) < getMillisecondTimestamp()
