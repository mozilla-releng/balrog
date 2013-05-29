import difflib

import requests

from mozilla_buildtools.retry import retry


def compare_snippets(url1, url2, retries=3, timeout=10, diff=True):
    cfg = {'danger_mode': True}
    xml1 = retry(requests.get, sleeptime=5, attempts=retries, args=(url1,),
                 retry_exceptions=(requests.HTTPError, requests.ConnectionError),
                 kwargs={'timeout': timeout, 'config': cfg})
    xml1 = xml1.content.splitlines()
    xml2 = retry(requests.get, sleeptime=5, attempts=retries, args=(url2,),
                 retry_exceptions=(requests.HTTPError, requests.ConnectionError),
                 kwargs={'timeout': timeout, 'config': cfg})
    xml2 = xml2.content.splitlines()
    ret = [url1, xml1, url2, xml2]
    if xml1 != xml2:
        if diff:
            difflines = []
            for line in difflib.unified_diff(xml1, xml2, url1, url2, lineterm=""):
                difflines.append(line)
            ret.append(difflines)
        else:
            ret.append(True)
    else:
        ret.append(False)
    return ret
