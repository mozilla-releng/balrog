from auslib.blobs.base import Blob


class WhitelistBlobV1(Blob):
    jsonschema = "whitelist.yml"

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 3000

    def isWhitelisted(self, requestIMEI):
        self.log.debug("Checking to see if IMEI '%s' is whitelisted", requestIMEI)
        if any(listItem['imei'] == requestIMEI for listItem in self['whitelist']):
            self.log.debug("IMEI is whitelisted")
            return True
        self.log.debug("IMEI not whitelisted")
        return False

    def shouldServeUpdate(self, updateQuery):
        self.log.debug(updateQuery)
        requestIMEI = updateQuery.get('IMEI')
        if requestIMEI is not None:
            return self.isWhitelisted(requestIMEI)
        return False

    def containsForbiddenDomain(self, product, whitelistedDomains):
        # Since WhitelistBlobs have no URLs
        return False
