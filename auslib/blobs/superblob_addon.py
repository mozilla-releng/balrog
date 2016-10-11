from auslib.blobs.base import Blob


class SuperBlobAddon(Blob):
    jsonschema = "superblob_addon.yml"

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 6000

    def getResponseBlobs(self):
        return self["blobs"]

    def shouldServeUpdate(self, updateQuery):
        # Since a superblob update will always be returned.
        return True

    def containsForbiddenDomain(self, product, whitelistedDomains):
        # Since SuperBlobs don't have any URLs
        return False

    def getHeaderXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        revision = self['revision']
        return '    <addons revision=%i>' % (revision)

    def getFooterXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        return '    </addons>'
