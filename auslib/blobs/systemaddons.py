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

    # If there are are no updates, we have a special response for SystemAddons
    # blobs. We return <updates></updates>, without the addons tags.
    def hasUpdates(self, updateQuery, whitelistedDomains):
        buildTarget = updateQuery["buildTarget"]
        for addon in sorted(self.getAddonsForPlatform(buildTarget)):
            # Checking if the addon update is to be served
            platformData = self.getPlatformData(addon, buildTarget)
            url = platformData["fileUrl"]
            # There might be no updates even if we have response products if
            # they are not served from whitelisted domains
            if isForbiddenUrl(url, updateQuery["product"], whitelistedDomains):
                continue
            return True
        return False

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

    def getHeaderXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        if self.get("uninstall", False) or self.hasUpdates(updateQuery, whitelistedDomains):
            return '    <addons>'
        else:
            return None

    def getFooterXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        if self.get("uninstall", False) or self.hasUpdates(updateQuery, whitelistedDomains):
            return '    </addons>'
        else:
            return None

    def containsForbiddenDomain(self, product, whitelistedDomains):
        """Returns True if the blob contains any file URLs that contain a
           domain that we're not allowed to serve updates to."""

        for addon in self.get('addons', {}).values():
            for platform in addon.get('platforms', {}).values():
                if 'fileUrl' in platform:
                    if isForbiddenUrl(platform["fileUrl"], product, whitelistedDomains):
                        return True

        return False
