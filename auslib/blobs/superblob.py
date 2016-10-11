from auslib.blobs.base import Blob


class SuperBlob(Blob):
    jsonschema = "superblob.yml"

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 4000

    def getResponseProducts(self):
        return self["products"]

    def shouldServeUpdate(self, updateQuery):
        # Since a superblob update will always be returned.
        return True

    def containsForbiddenDomain(self, product, whitelistedDomains):
        # Since SuperBlobs don't have any URLs
        return False

    def getHeaderXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        return '    <addons>'

    def getFooterXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        return '    </addons>'
