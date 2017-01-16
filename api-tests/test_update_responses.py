import requests
from io import StringIO
from lxml import etree


def test_update_addon_responses():
    addon_urls = [
        'https://aus5.mozilla.org/update/3/SystemAddons/44.0/20160310153207/Darwin_x86_64-gcc3-u-i386-x86_64/en-GB/release/Darwin%2014.5.0/default/default/update.xml',
    ]
    dtd_info = """
    <!ELEMENT updates (addons) >
    <!ELEMENT addons (addon+) >
    <!ELEMENT addon (#PCDATA)>
    <!ATTLIST addon
    id CDATA #REQUIRED
    URL CDATA #REQUIRED
    hashFunction CDATA #REQUIRED
    hashValue CDATA #REQUIRED
    size CDATA #REQUIRED
    version CDATA #REQUIRED >
    """
    f = StringIO(dtd_info)
    dtd = etree.DTD(f)

    for url in addon_urls:
        response = requests.get(url)
        root = etree.XML(response.text)
        assert dtd.validate(root)


def test_update_patch_responses():
    patch_urls = [
        'https://aus5.mozilla.org/update/3/Firefox/50.0.1/20161123182536/WINNT_x86_64-msvc-x64/en-US/release/default/default/default/update.xml?force=1',
        'https://aus5.mozilla.org/update/3/Firefox/50.0.1/20161123182536/Darwin_x86_64-gcc3-u-i386-x86_64/en-US/release/default/default/default/update.xml?force=1',
        'https://aus5.mozilla.org/update/3/Firefox/50.0.1/20161123182536/Linux_x86_64-gcc3/en-US/release/default/default/default/update.xml?force=1',
    ]

    dtd_info = """
    <!ELEMENT updates (update) >
    <!ELEMENT update (patch+) >
    <!ATTLIST update
    type CDATA #REQUIRED
    displayVersion CDATA #REQUIRED
    appVersion CDATA #REQUIRED
    platformVersion CDATA #REQUIRED
    buildID CDATA #REQUIRED
    detailsURL CDATA #REQUIRED >
    <!ELEMENT patch (#PCDATA)>
    <!ATTLIST patch
    type CDATA #REQUIRED
    URL CDATA #REQUIRED
    hashFunction CDATA #REQUIRED
    hashValue CDATA #REQUIRED
    size CDATA #REQUIRED >
    """
    f = StringIO(dtd_info)
    dtd = etree.DTD(f)

    for url in patch_urls:
        response = requests.get(url)
        root = etree.XML(response.text)
        assert dtd.validate(root)
