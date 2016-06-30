from auslib.AUS import isForbiddenUrl
from auslib.blobs.base import Blob
from auslib.errors import BadDataError


class SystemAddonsBlob(Blob):
    jsonschema = "systemaddons.yml"

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 5000

    def getAddonsForPlatform(self, platform):
        for v in self["addons"]:
            if platform in self["addons"][v]["platforms"] or "default" in self["addons"][v]["platforms"]:
                yield v

    def getResolvedPlatform(self, addon, platform):
        if platform in self['addons'][addon]['platforms']:
            return self['addons'][addon]['platforms'][platform].get('alias', platform)
        if "default" in self['addons'][addon]['platforms']:
            return "default"
        raise BadDataError("No platform '%s' or default in addon '%s'",
                           platform, addon)

    def getPlatformData(self, addon, platform):
        platform = self.getResolvedPlatform(addon, platform)
        try:
            return self['addons'][addon]['platforms'][platform]
        except KeyError:
            raise BadDataError("No platform '%s' in addon '%s'", platform,
                               addon)

    def shouldServeUpdate(self, updateQuery):
        # SystemAddon updates should always be returned. It is the responsibility
        # of the client to decide whether or not any action needs to be taken,
        # similar to GMP
        return True

    # Because specialForceHosts is only relevant to our own internal servers,
    # and these type of updates are always served externally, we don't process
    # them in SystemAddon blobs, similar to GMP.
    def getInnerXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        # In case we have an uninstall blob, we won't have the addons section
        if self.get('addons') is None:
            return []
        buildTarget = updateQuery["buildTarget"]

        addonXML = []
        for addon in sorted(self.getAddonsForPlatform(buildTarget)):
            addonInfo = self["addons"][addon]
            platformData = self.getPlatformData(addon, buildTarget)

            url = platformData["fileUrl"]
            if isForbiddenUrl(url, updateQuery["product"], whitelistedDomains):
                continue
            addonXML.append('        <addon id="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s" version="%s"/>' %
                            (addon, url, self["hashFunction"], platformData["hashValue"],
                             platformData["filesize"], addonInfo["version"]))

        return addonXML

    def getHeaderXML(self, updateQuery, update_type):
        if self.get("uninstall", False):
            return '    <addons>'
        return None

    def getFooterXML(self):
        if self.get("uninstall", False):
            return '    </addons>'
        return None
