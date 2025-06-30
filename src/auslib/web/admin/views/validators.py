# To enable shared jsonschema validators
import auslib.util.jsonschema_validators  # noqa
from auslib.util.timestamp import getMillisecondTimestamp


def is_when_present_and_in_past_validator(what):
    """Validates if scheduled_change_time value i.e. 'when' field value is present in
    input dictionary/object and if its value is in past or not"""
    return what.get("when", None) and int(what.get("when")) < getMillisecondTimestamp()
