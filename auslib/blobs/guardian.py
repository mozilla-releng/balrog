from auslib.blobs.base import GenericBlob


class GuardianBlob(GenericBlob):
    jsonschema = "guardian.yml"

    def containsForbiddenDomain(self, product, whitelistedDomains):
        # TODO: really implement me
        return False

    def shouldServeUpdate(self, updateQuery):
        # TODO: implement me
        return True

    def getResponse(self, updateQuery, whilelistedDomains):
        # TODO: check whitelisted domains
        return {
            "version": self["version"],
            "url": self["url"],
            "required": self["required"],
        }
