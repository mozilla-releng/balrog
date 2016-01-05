import re
from auslib.blobs.base import Blob


INDENT = 4 * ' '
SETTING_TMPL = ('<setting id="%(id)s" '
                'lastModified="%(last_modified)s"/>')


class SettingsBlob(Blob):
    jsonschema = "settings.json"

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 2000

    def shouldServeUpdate(self, updateQuery):
        return True

    def createXML(self, updateQuery, update_type, whitelistedDomains,
                  specialForceHosts):
        xml = ['<?xml version="1.0"?>']
        xml.append('<updates>')
        if len(self['settings']) > 0:
            xml.append(INDENT + '<settings>')
            for id_, data in self['settings'].items():
                data['id'] = id_
                xml.append(INDENT * 2 + SETTING_TMPL % data)
            xml.append(INDENT + '</settings>')

        xml.append('</updates>')
        # ensure valid xml by using the right entity for ampersand
        return re.sub('&(?!amp;)', '&amp;', '\n'.join(xml))
