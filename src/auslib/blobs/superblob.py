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

    def getReferencedReleases(self):
        """
        :return: The names of the Releases this SuperBlob serves by name (its
                 systemaddons "blobs" entries). "products" entries are product
                 names resolved through Rules, not Release names, so they are
                 intentionally excluded.
        """
        blobs = self.get("blobs")
        if not isinstance(blobs, (list, tuple)):
            return set()
        return set(blobs)

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
