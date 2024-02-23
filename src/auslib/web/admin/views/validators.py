import logging

from auslib.util.timestamp import getMillisecondTimestamp

logger = logging.getLogger(__name__)


def is_when_present_and_in_past_validator(what):
    """Validates if scheduled_change_time value i.e. 'when' field value is present in
    input dictionary/object and if its value is in past or not"""
    return what.get("when", None) and int(what.get("when")) < getMillisecondTimestamp()
