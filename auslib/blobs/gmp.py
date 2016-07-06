from auslib.AUS import isForbiddenUrl
from auslib.blobs.base import Blob
from auslib.errors import BadDataError


class GMPBlobV1(Blob):
    jsonschema = "gmp.yml"

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 1000

    def getVendorsForPlatform(self, platform):
        for v in self["vendors"]:
            if platform in self["vendors"][v]["platforms"] or "default" in self["vendors"][v]["platforms"]:
                yield v

    def getResolvedPlatform(self, vendor, platform):
        if platform in self['vendors'][vendor]['platforms']:
            return self['vendors'][vendor]['platforms'][platform].get('alias', platform)
        if "default" in self['vendors'][vendor]['platforms']:
            return "default"
        raise BadDataError("No platform '%s' or default in vendor '%s'", platform, vendor)

    def getPlatformData(self, vendor, platform):
        platform = self.getResolvedPlatform(vendor, platform)
        try:
            return self['vendors'][vendor]['platforms'][platform]
        except KeyError:
            raise BadDataError("No platform '%s' in vendor '%s'", platform, vendor)

    def shouldServeUpdate(self, updateQuery):
        # GMP updates should always be returned. It is the responsibility
        # of the client to decide whether or not any action needs to be taken.
        return True

    def getHeaderXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        return '    <addons>'

    def getFooterXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        return '    </addons>'

    # Because specialForceHosts is only relevant to our own internal servers,
    # and these type of updates are always served externally, we don't process
    # them in GMP blobs.
    def getInnerXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        buildTarget = updateQuery["buildTarget"]

        vendorXML = []
        for vendor in sorted(self.getVendorsForPlatform(buildTarget)):
            vendorInfo = self["vendors"][vendor]
            platformData = self.getPlatformData(vendor, buildTarget)

            url = platformData["fileUrl"]
            if isForbiddenUrl(url, updateQuery["product"], whitelistedDomains):
                continue
            vendorXML.append('        <addon id="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s" version="%s"/>' %
                             (vendor, url, self["hashFunction"], platformData["hashValue"],
                              platformData["filesize"], vendorInfo["version"]))

        return vendorXML
