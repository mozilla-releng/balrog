import time


def getMillisecondTimestamp():
    t = int(time.time() * 1000)
    return t
