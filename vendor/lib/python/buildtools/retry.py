import time

import logging
log = logging.getLogger(__name__)

def retry(action, attempts=5, sleeptime=60, retry_exceptions=(Exception,),
          cleanup=None, args=(), kwargs={}):
    """Call `action' a maximum of `attempts' times until it succeeds,
        defaulting to 5. `sleeptime' is the number of seconds to wait
        between attempts, defaulting to 0. `retry_exceptions' is a tuple
        of Exceptions that should be caught. If exceptions other than those
        listed in `retry_exceptions' are raised from `action', they will be
        raised immediately. If `cleanup' is provided and callable it will
        be called immediately after an Exception is caught. No arguments
        will be passed to it. If your cleanup function requires arguments
        it is recommended that you wrap it in an argumentless function.
        `args' and `kwargs' are a tuple and dict of arguments to pass onto
        to `callable'"""
    assert callable(action)
    assert not cleanup or callable(cleanup)
    n = 1
    while n <= attempts:
        try:
            log.info("Calling %s with args: %s, kwargs: %s, attempt #%d" % \
              (action, str(args), str(kwargs), n))
            return action(*args, **kwargs)
        except retry_exceptions:
            if cleanup:
                cleanup()
            if n == attempts:
                log.info("Giving up on %s" % action)
                raise
            if sleeptime > 0:
                log.info("Failed, sleeping %d seconds before retrying" % sleeptime)
                time.sleep(sleeptime)
            continue
        finally:
            n += 1
