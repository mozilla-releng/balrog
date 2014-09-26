import re

from auslib.AUS import containsForbiddenDomain
from auslib.blobs.base import Blob


class GMPBlobV1(Blob):
    format_ = {
        "name": None,
        "schema_version": None,
        "hashFunction": None,
        "vendors": {
            "*": {
                "version": None,
                "platforms": {
                    "*": {
                        "alias": None,
                        "filesize": None,
                        "hashValue": None,
                        "fileUrl": None
                    }
                }
            }
        }
    }

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 1000

    def getVendorsForPlatform(self, platform):
        for v in self["vendors"]:
            if platform in self["vendors"][v]["platforms"]:
                yield v

    def getResolvedPlatform(self, vendor, platform):
        return self['vendors'][vendor]['platforms'][platform].get('alias', platform)

    def getPlatformData(self, vendor, platform):
        platform = self.getResolvedPlatform(vendor, platform)
        return self['vendors'][vendor]['platforms'][platform]

    def shouldServeUpdate(self, updateQuery):
        # GMP updates should always be returned. It is the responsibility
        # of the client to decide whether or not any action needs to be taken.
        return True

    # Because specialForceHosts is only relevant to our own internal servers,
    # and these type of updates are always served externally, we don't process
    # them in GMP blobs.
    def createXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        buildTarget = updateQuery["buildTarget"]

        vendorXML = []
        for vendor in self.getVendorsForPlatform(buildTarget):
            vendorInfo = self["vendors"][vendor]
            platformData = self.getPlatformData(vendor, buildTarget)

            url = platformData["fileUrl"]
            if containsForbiddenDomain(url, whitelistedDomains):
                continue
            vendorXML.append('        <addon id="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%d" version="%s"/>' % \
                (vendor, url, self["hashFunction"], platformData["hashValue"],
                    platformData["filesize"], vendorInfo["version"]))

        xml = ['<?xml version="1.0"?>']
        xml.append('<updates>')
        if vendorXML:
            xml.append('    <addons>')
            xml.extend(vendorXML)
            xml.append('    </addons>')
        xml.append('</updates>')
        # ensure valid xml by using the right entity for ampersand
        return re.sub('&(?!amp;)','&amp;', '\n'.join(xml))
