from auslib.AUS import isForbiddenUrl
from auslib.blobs.base import ServeUpdate, XMLBlob
from auslib.errors import BadDataError


class SystemAddonsBlob(XMLBlob):
    jsonschema = "systemaddons.yml"

    def __init__(self, **kwargs):
        XMLBlob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 5000

    def getAddonsForPlatform(self, platform):
        for v in self.get("addons", {}):
            platforms = self["addons"].get(v, {}).get("platforms", {})
            if platform in platforms or "default" in platforms:
                yield v

    def getResolvedPlatform(self, addon, platform):
        platforms = self.get("addons", {}).get(addon, {}).get("platforms", {})
        if platform in platforms:
            return self.get("addons", {}).get(addon, {}).get("platforms", {}).get(platform, {}).get("alias", platform)
        if "default" in platforms:
            return "default"
        raise BadDataError("No platform '%s' or default in addon '%s'", platform, addon)

    def getPlatformData(self, addon, platform):
        platform = self.getResolvedPlatform(addon, platform)
        return self.get("addons", {}).get(addon, {}).get("platforms", {}).get(platform)

    def shouldServeUpdate(self, updateQuery):
        # SystemAddon updates should always be returned. It is the responsibility
        # of the client to decide whether or not any action needs to be taken,
        # similar to GMP
        return ServeUpdate.Yes

    # If there are are no updates, we have a special response for SystemAddons
    # blobs. We return <updates></updates>, without the addons tags.
    def hasUpdates(self, updateQuery, allowlistedDomains):
        buildTarget = updateQuery["buildTarget"]
        for addon in sorted(self.getAddonsForPlatform(buildTarget)):
            # Checking if the addon update is to be served
            platformData = self.getPlatformData(addon, buildTarget)
            url = platformData["fileUrl"]
            # There might be no updates even if we have response products if
            # they are not served from allowlisted domains
            if isForbiddenUrl(url, updateQuery["product"], allowlistedDomains):
                continue
            return True
        return False

    # Because specialForceHosts is only relevant to our own internal servers,
    # and these type of updates are always served externally, we don't process
    # them in SystemAddon blobs, similar to GMP.
    def getInnerXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        # In case we have an uninstall blob, we won't have the addons section
        if self.get("addons") is None:
            return []
        buildTarget = updateQuery["buildTarget"]

        addonXML = []
        for addon in sorted(self.getAddonsForPlatform(buildTarget)):
            addonInfo = self["addons"][addon]
            platformData = self.getPlatformData(addon, buildTarget)

            url = platformData["fileUrl"]
            if isForbiddenUrl(url, updateQuery["product"], allowlistedDomains):
                continue
            addonXML.append(
                '        <addon id="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s" version="%s"/>'
                % (addon, url, self["hashFunction"], platformData["hashValue"], platformData["filesize"], addonInfo["version"])
            )

        return addonXML

    def getInnerHeaderXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        if self.get("uninstall", False) or self.hasUpdates(updateQuery, allowlistedDomains):
            return "    <addons>"
        else:
            return ""

    def getInnerFooterXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        if self.get("uninstall", False) or self.hasUpdates(updateQuery, allowlistedDomains):
            return "    </addons>"
        else:
            return ""

    def containsForbiddenDomain(self, product, allowlistedDomains):
        """Returns True if the blob contains any file URLs that contain a
        domain that we're not allowed to serve updates to."""

        for addon in self.get("addons", {}).values():
            for platform in addon.get("platforms", {}).values():
                if "fileUrl" in platform:
                    if isForbiddenUrl(platform["fileUrl"], product, allowlistedDomains):
                        return True

        return False
