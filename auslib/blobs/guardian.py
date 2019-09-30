from auslib.blobs.base import GenericBlob


class GuardianBlob(GenericBlob):
    jsonschema = "guardian.yml"

    def getResponse(self, updateQuery, whilelistedDomains):
        # TODO: check whitelisted domains
        return {
            "version": self["version"],
            "url": self["url"],
        }
