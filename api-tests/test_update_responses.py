import pytest
import requests
from lxml import etree


def validate_responses_helper(dtd, urls):
    for url in urls:
        response = requests.get(url)
        root = etree.XML(response.text)
        valid = dtd.validate(root)

        if valid:
            assert True
        else:
            print(dtd.error_log.filter_from_errors())
            assert False


def test_update_addon_responses(server_url):
    print(server_url)
    addon_urls = [
        server_url + "/update/3/SystemAddons/44.0/20160310153207/Darwin_x86_64-gcc3-u-i386-x86_64/en-GB/release/Darwin%2014.5.0/default/default/update.xml",
    ]
    f = open('./api-tests/addons.dtd')
    dtd = etree.DTD(f)
    validate_responses_helper(dtd, addon_urls)


def test_update_patch_responses(server_url):
    patch_urls = [
        server_url + '/update/3/Firefox/50.0.1/20161123182536/WINNT_x86_64-msvc-x64/en-US/release/default/default/default/update.xml?force=1',
        server_url + '/update/3/Firefox/50.0.1/20161123182536/Darwin_x86_64-gcc3-u-i386-x86_64/en-US/release/default/default/default/update.xml?force=1',
        server_url + '/update/3/Firefox/50.0.1/20161123182536/Linux_x86_64-gcc3/en-US/release/default/default/default/update.xml?force=1',
    ]
    f = open('./api-tests/updates.dtd')
    dtd = etree.DTD(f)
    validate_responses_helper(dtd, patch_urls)


def test_update_with_no_addons():
    xml = '''
    <updates>
        <addons> </addons>
    </updates>
    '''
    f = open('./api-tests/addons.dtd')
    dtd = etree.DTD(f)
    root = etree.XML(xml)
    valid = dtd.validate(root)

    if valid:
        assert True
    else:
        print(dtd.error_log.filter_from_errors())
        assert False
