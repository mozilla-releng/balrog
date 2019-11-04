from distutils.version import LooseVersion

from auslib.AUS import isForbiddenUrl
from auslib.blobs.base import GenericBlob


class GuardianBlob(GenericBlob):
    jsonschema = "guardian.yml"

    def containsForbiddenDomain(self, product, whitelistedDomains):
        urls = [p["fileUrl"] for p in self["platforms"].values()]
        return any([isForbiddenUrl(url, product, whitelistedDomains) for url in urls])

    def shouldServeUpdate(self, updateQuery):
        if updateQuery["buildTarget"] not in self.get("platforms", {}):
            return False
        if LooseVersion(updateQuery["version"]) >= LooseVersion(self["version"]):
            return False

        return True

    def getResponse(self, updateQuery, whitelistedDomains):
        url = self.get("platforms", {}).get(updateQuery["buildTarget"], {}).get("fileUrl")
        hashValue = self.get("platforms", {}).get(updateQuery["buildTarget"], {}).get("hashValue")
        if not url:
            return {}

        if isForbiddenUrl(url, updateQuery["product"], whitelistedDomains):
            return {}

        return {
            "version": self["version"],
            "url": url,
            "required": self["required"],
            "hashFunction": self["hashFunction"],
            "hashValue": hashValue,
        }
