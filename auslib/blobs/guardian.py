from auslib.AUS import isForbiddenUrl
from auslib.blobs.base import GenericBlob


class GuardianBlob(GenericBlob):
    jsonschema = "guardian.yml"

    def containsForbiddenDomain(self, product, whitelistedDomains):
        return isForbiddenUrl(self["url"], product, whitelistedDomains)

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
