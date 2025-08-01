import logging
from typing import AnyStr, Union

import jsonschema
from connexion.decorators.validation import RequestBodyValidator
from connexion.exceptions import BadRequestProblem
from connexion.lifecycle import ConnexionResponse
from connexion.utils import is_null

# To enable shared jsonschema validators
import auslib.util.jsonschema_validators  # noqa
from auslib.util.timestamp import getMillisecondTimestamp

logger = logging.getLogger(__name__)


class BalrogRequestBodyValidator(RequestBodyValidator):
    def validate_schema(self, data: dict, url: AnyStr) -> Union[ConnexionResponse, None]:
        """This function is largely based on https://github.com/zalando/connexion/blob/master/connexion/decorators/validation.py
        and should largely be kept in line with it."""
        if self.is_null_value_valid and is_null(data):
            return None
        try:
            self.validator.validate(data)
        except jsonschema.ValidationError as exception:
            # Add field name to the error response
            exception_field = ""
            for i in exception.path:
                exception_field = i + ": "
            if exception.__cause__ is not None:
                exception_message = exception.__cause__.message + " " + exception_field + exception.message
            else:
                exception_message = exception_field + exception.message
            # Some exceptions could contain unicode characters - if we don't replace them
            # we could end up with a UnicodeEncodeError.
            logger.warning("{url} validation error: {error}".format(url=url, error=exception_message.encode("utf-8", "replace")))
            raise BadRequestProblem(detail=exception_message)

        return None


def is_when_present_and_in_past_validator(what):
    """Validates if scheduled_change_time value i.e. 'when' field value is present in
    input dictionary/object and if its value is in past or not"""
    return what.get("when", None) and int(what.get("when")) < getMillisecondTimestamp()
