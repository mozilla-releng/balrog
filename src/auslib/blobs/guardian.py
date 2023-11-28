from auslib.AUS import isForbiddenUrl
from auslib.blobs.base import GenericBlob
from auslib.util.versions import LooseVersion


class GuardianBlob(GenericBlob):
    jsonschema = "guardian.yml"

    def containsForbiddenDomain(self, product, allowlistedDomains):
        urls = [p["fileUrl"] for p in self["platforms"].values()]
        return any([isForbiddenUrl(url, product, allowlistedDomains) for url in urls])

    def shouldServeUpdate(self, updateQuery):
        if updateQuery["buildTarget"] not in self.get("platforms", {}):
            return False
        if LooseVersion(updateQuery["version"]) >= LooseVersion(self["version"]):
            return False

        return True

    def getResponse(self, updateQuery, allowlistedDomains):
        url = self.get("platforms", {}).get(updateQuery["buildTarget"], {}).get("fileUrl")
        hashValue = self.get("platforms", {}).get(updateQuery["buildTarget"], {}).get("hashValue")
        if not url:
            return {}

        if isForbiddenUrl(url, updateQuery["product"], allowlistedDomains):
            return {}

        return {"version": self["version"], "url": url, "required": self["required"], "hashFunction": self["hashFunction"], "hashValue": hashValue}
