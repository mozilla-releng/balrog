from auslib.blobs.base import Blob


class SuperBlob(Blob):
    jsonschema = "superblob.yml"

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 4000

    def getResponseProducts(self):
        if self.get("products", False):
            return self["products"]
        else:
            return None

    def getResponseBlobs(self):
        if self.get("blobs", False):
            return self["blobs"]
        else:
            return None

    def shouldServeUpdate(self, updateQuery):
        # Since a superblob update will always be returned.
        return True

    def containsForbiddenDomain(self, product, whitelistedDomains):
        # Since SuperBlobs don't have any URLs
        return False

    def getHeaderXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        if self.get("revision", False):
            revision = self['revision']
            return '    <addons revision=\"%i\">' % (revision)
        else:
            return '    <addons'

    def getFooterXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        return '    </addons>'
