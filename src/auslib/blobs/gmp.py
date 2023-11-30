from auslib.AUS import isForbiddenUrl
from auslib.blobs.base import ServeUpdate, XMLBlob
from auslib.errors import BadDataError
from auslib.util.hashes import getHashLen


class GMPBlobV1(XMLBlob):
    jsonschema = "gmp.yml"

    def __init__(self, **kwargs):
        XMLBlob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 1000

    def validate(self, product, allowlistedDomains):
        XMLBlob.validate(self, product, allowlistedDomains)
        for vendor in self["vendors"]:
            for platform in self["vendors"][vendor].get("platforms", {}).values():
                if "hashValue" in platform:
                    actualLen = len(platform["hashValue"])
                    requiredLen = getHashLen(self["hashFunction"])
                    if actualLen != requiredLen:
                        raise ValueError(
                            "The hashValue length is different from the required length of {} for {}.".format(
                                getHashLen(self["hashFunction"]), self["hashFunction"].lower()
                            )
                        )

    def getVendorsForPlatform(self, platform):
        for v in self["vendors"]:
            if platform in self["vendors"][v]["platforms"] or "default" in self["vendors"][v]["platforms"]:
                yield v

    def getResolvedPlatform(self, vendor, platform):
        if platform in self["vendors"][vendor]["platforms"]:
            return self["vendors"][vendor]["platforms"][platform].get("alias", platform)
        if "default" in self["vendors"][vendor]["platforms"]:
            return "default"
        raise BadDataError("No platform '%s' or default in vendor '%s'", platform, vendor)

    def getPlatformData(self, vendor, platform):
        platform = self.getResolvedPlatform(vendor, platform)
        try:
            return self["vendors"][vendor]["platforms"][platform]
        except KeyError:
            raise BadDataError("No platform '%s' in vendor '%s'", platform, vendor)

    def shouldServeUpdate(self, updateQuery):
        # GMP updates should always be returned. It is the responsibility
        # of the client to decide whether or not any action needs to be taken.
        return ServeUpdate.Yes

    def getInnerHeaderXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        return "    <addons>"

    def getInnerFooterXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        return "    </addons>"

    # Because specialForceHosts is only relevant to our own internal servers,
    # and these type of updates are always served externally, we don't process
    # them in GMP blobs.
    def getInnerXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        buildTarget = updateQuery["buildTarget"]

        vendorXML = []
        for vendor in sorted(self.getVendorsForPlatform(buildTarget)):
            vendorInfo = self["vendors"][vendor]
            platformData = self.getPlatformData(vendor, buildTarget)

            url = platformData["fileUrl"]
            if isForbiddenUrl(url, updateQuery["product"], allowlistedDomains):
                continue
            vendorXML.append(
                '        <addon id="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s" version="%s"/>'
                % (vendor, url, self["hashFunction"], platformData["hashValue"], platformData["filesize"], vendorInfo["version"])
            )

        return vendorXML

    def containsForbiddenDomain(self, product, allowlistedDomains):
        """Returns True if the blob contains any file URLs that contain a
        domain that we're not allowed to serve updates to."""
        for vendor in self.get("vendors", {}).values():
            for platform in vendor.get("platforms", {}).values():
                if "fileUrl" in platform:
                    if isForbiddenUrl(platform["fileUrl"], product, allowlistedDomains):
                        return True
        return False
