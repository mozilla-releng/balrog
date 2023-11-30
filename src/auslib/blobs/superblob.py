from auslib.blobs.base import ServeUpdate, XMLBlob


class SuperBlob(XMLBlob):
    jsonschema = "superblob.yml"

    def __init__(self, **kwargs):
        XMLBlob.__init__(self, **kwargs)
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
        return ServeUpdate.Yes

    def containsForbiddenDomain(self, product, allowlistedDomains):
        # Since SuperBlobs don't have any URLs
        return False

    def getInnerHeaderXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        """
        :return: Header specific to GMP and systemaddons superblob
        """
        return "    <addons>"

    def getInnerFooterXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        return "    </addons>"
