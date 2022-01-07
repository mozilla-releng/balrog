import logging
import random
import time
from typing import Any, Callable, Dict, Optional

log = logging.getLogger(__name__)


# calculate_sleep_time {{{1
def calculate_sleep_time(attempt, delay_factor=5.0, randomization_factor=0.5, max_delay=120):
    """Calculate the sleep time between retries, in seconds.

    Based off of `taskcluster.utils.calculateSleepTime`, but with kwargs instead
    of constant `delay_factor`/`randomization_factor`/`max_delay`.  The taskcluster
    function generally slept for less than a second, which didn't always get
    past server issues.

    Args:
        attempt (int): the retry attempt number
        delay_factor (float, optional): a multiplier for the delay time.  Defaults to 5.
        randomization_factor (float, optional): a randomization multiplier for the
            delay time.  Defaults to .5.
        max_delay (float, optional): the max delay to sleep.  Defaults to 120 (seconds).

    Returns:
        float: the time to sleep, in seconds.

    """
    if attempt <= 0:
        return 0

    # We subtract one to get exponents: 1, 2, 3, 4, 5, ..
    delay = float(2 ** (attempt - 1)) * float(delay_factor)
    # Apply randomization factor.  Only increase the delay here.
    delay = delay * (randomization_factor * random.random() + 1)
    # Always limit with a maximum delay
    return min(delay, max_delay)


def retry_sync(func, attempts=5, sleeptime_callback=calculate_sleep_time, retry_exceptions=Exception, args=(), kwargs=None, sleeptime_kwargs=None):
    """Retry ``func``, where ``func`` is a regular function.

    Args:
        func (function): a function.
        attempts (int, optional): the number of attempts to make.  Default is 5.
        sleeptime_callback (function, optional): the function to use to determine
            how long to sleep after each attempt.  Defaults to ``calculateSleepTime``.
        retry_exceptions (list or exception, optional): the exception(s) to retry on.
            Defaults to ``Exception``.
        args (list, optional): the args to pass to ``func``.  Defaults to ()
        kwargs (dict, optional): the kwargs to pass to ``func``.  Defaults to
            {}.
        sleeptime_kwargs (dict, optional): the kwargs to pass to ``sleeptime_callback``.
            If None, use {}.  Defaults to None.

    Returns:
        object: the value from a successful ``function`` call

    Raises:
        Exception: the exception from a failed ``function`` call, either outside
            of the retry_exceptions, or one of those if we pass the max
            ``attempts``.

    """
    kwargs = kwargs or {}
    attempt = 1
    while True:
        try:
            return func(*args, **kwargs)
        except retry_exceptions:
            attempt += 1
            _check_number_of_attempts(attempt, attempts, func, "retry_sync")
            time.sleep(_define_sleep_time(sleeptime_kwargs, sleeptime_callback, attempt, func, "retry_sync"))


def _check_number_of_attempts(attempt: int, attempts: int, func: Callable[..., Any], retry_function_name: str) -> None:
    if attempt > attempts:
        log.warning("{}: {}: too many retries!".format(retry_function_name, func.__name__))
        raise


def _define_sleep_time(
    sleeptime_kwargs: Optional[Dict[str, Any]], sleeptime_callback: Callable[..., int], attempt: int, func: Callable[..., Any], retry_function_name: str
) -> float:
    sleeptime_kwargs = sleeptime_kwargs or {}
    sleep_time = sleeptime_callback(attempt, **sleeptime_kwargs)
    log.debug("{}: {}: sleeping {} seconds before retry".format(retry_function_name, func.__name__, sleep_time))
    return sleep_time
