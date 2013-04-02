import difflib

import requests


def compare_snippets(server1, server2, paths, diff=True, retries=3, timeout=10,
                     raise_exceptions=True):
    cfg = {'max_retries': retries, 'danger_mode': raise_exceptions}
    for path in paths:
        url1 = '%s/%s' % (server1, path)
        url2 = '%s/%s' % (server2, path)
        xml1 = requests.get(url1, timeout=timeout, config=cfg).content.splitlines()
        xml2 = requests.get(url2, timeout=timeout, config=cfg).content.splitlines()
        if xml1 != xml2:
            if diff:
                yield (url1, xml1, url2, xml2, difflib.unified_diff(xml1, xml2, lineterm=""))
            else:
                yield (url1, xml1, url2, xml2)
