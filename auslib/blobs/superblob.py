from auslib.blobs.base import Blob


class SuperBlob(Blob):
    jsonschema = "superblob.yml"

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 4000

    def getResponseProducts(self):
        """
        :return: Product in case of GMP supreblob
        """
        return self.get("products")

    def getResponseBlobs(self):
        """
        :return: Blob names in case of systemaddon Blobs
        """
        return self.get("blobs")

    def shouldServeUpdate(self, updateQuery):
        # Since a superblob update will always be returned.
        return True

    def containsForbiddenDomain(self, product, whitelistedDomains):
        # Since SuperBlobs don't have any URLs
        return False

    def getInnerHeaderXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        """
        :return: Header specific to GMP and systemaddons superblob
        """
        if not self.get("products"):
            revision = self['revision']
            # In case of systemaddons superblob
            return '    <addons revision=\"%i\">' % (revision)
        else:
            # In case of GMP superblob
            return '    <addons>'

    def getInnerFooterXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        return '    </addons>'
