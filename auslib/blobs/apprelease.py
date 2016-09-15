from auslib.global_state import dbo
from auslib.AUS import isForbiddenUrl, getFallbackChannel
from auslib.blobs.base import Blob
from auslib.errors import BadDataError
from auslib.util.versions import MozillaVersion


class ReleaseBlobBase(Blob):

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)

    def matchesUpdateQuery(self, updateQuery):
        self.log.debug("Trying to match update query to %s" % self["name"])
        buildTarget = updateQuery["buildTarget"]
        buildID = updateQuery["buildID"]
        locale = updateQuery["locale"]

        if buildTarget in self["platforms"]:
            try:
                releaseBuildID = self.getBuildID(buildTarget, locale)
            # Platform doesn't exist in release, clearly it's not a match!
            except BadDataError:
                return False
            self.log.debug("releasePlat buildID is: %s", releaseBuildID)
            if buildID == releaseBuildID:
                self.log.debug("Query matched!")
                return True

    def getResolvedPlatform(self, platform):
        try:
            return self['platforms'][platform].get('alias', platform)
        except KeyError:
            raise BadDataError("Can't find platform '%s'", platform)

    def getPlatformData(self, platform):
        platform = self.getResolvedPlatform(platform)
        try:
            return self['platforms'][platform]
        except KeyError:
            raise BadDataError("Can't find platform '%s'", platform)

    def getLocaleData(self, platform, locale):
        platformData = self.getPlatformData(platform)
        try:
            return platformData["locales"][locale]
        except KeyError:
            raise BadDataError("Can't find locale '%s' in '%s'", locale, platform)

    def getLocaleOrTopLevelParam(self, platform, locale, param):
        try:
            platform = self.getResolvedPlatform(platform)
            return self['platforms'][platform]['locales'][locale][param]
        except (BadDataError, KeyError):
            try:
                return self[param]
            except (BadDataError, KeyError):
                return None

    def getBuildID(self, platform, locale):
        platform = self.getResolvedPlatform(platform)
        if locale not in self['platforms'].get(platform, {}) \
                                          .get('locales', {}):
            raise BadDataError("No such locale '%s' in platform '%s'" % (locale, platform))
        try:
            return self['platforms'][platform]['locales'][locale]['buildID']
        except KeyError:
            if platform not in self['platforms']:
                raise BadDataError("No such platform '%s'" % (platform))
            if 'buildID' not in self['platforms'][platform].keys():
                raise BadDataError("No buildID for platform '%s'" % (platform))
            return self['platforms'][platform]['buildID']

    def _getFromRelease(self, patch):
        # "*" is a special case for the "from" field that means "any release".
        # Because we know it doesn't exist in the database it's wasteful to
        # even attempt to look it up.
        if patch["from"] != "*":
            try:
                return dbo.releases.getReleaseBlob(name=patch["from"])
            except KeyError:
                # Release doesn't exist
                return None
        else:
            return None

    def _getSpecificPatchXML(self, patchKey, patchType, patch, updateQuery, whitelistedDomains, specialForceHosts):
        fromRelease = self._getFromRelease(patch)
        # don't return an update if we don't match the from restriction
        if fromRelease and not fromRelease.matchesUpdateQuery(updateQuery):
            return None
        # don't return an update if an older release isn't in the DB for some reason
        if patch['from'] != '*' and fromRelease is None:
            return None

        url = self._getUrl(updateQuery, patchKey, patch, specialForceHosts)
        # TODO: should be raising a bigger alarm here, or aborting
        # the update entirely? Right now, another patch type could still
        # return an update. Eg, the partial could contain a forbidden domain
        # but the complete could still return an update from an accepted one.
        if isForbiddenUrl(url, updateQuery['product'], whitelistedDomains):
            return None

        return '        <patch type="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s"/>' % \
            (patchType, url, self["hashFunction"], patch["hashValue"], patch["filesize"])

    def getHeaderXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        buildTarget = updateQuery["buildTarget"]
        locale = updateQuery["locale"]
        return self._getUpdateLineXML(buildTarget, locale, update_type)

    def getFooterXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        return '    </update>'

    def getInnerXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        """This method, along with getHeaderXML and getFooterXML are the entry point
           for update XML creation for all Gecko app blobs. However, the XML and
           underlying data has changed over time, so there is a lot of indirection
           and calls factored out to subclasses. Below is a brief description of the
           flow of control that should help in understanding this code. Inner methods
           that are shared between blob versions live in Mixin classes so that they can
           be easily shared. Inner methods that only apply to a single blob
           version live on concrete blob classes (but should be moved if they
           need to be shared in the future).
           * getInnerXML, getFooterXML and getHeaderXML called by web layer,
             live on this base class. The V1 blob class override them to
             support bug 1113475, but still calls the base class one to do most of the work.
           ** _getUpdateLineXML() called to get information that is independent
              of specific MARs. Most notably, version information changed
              starting with V2 blobs.
           ** _getPatchesXML() called to get the information that describes
              specific MARs. Where in the blob this information comes from
              changed significantly starting with V3 blobs.
           *** _getSpecificPatchXML() called to translate MAR information into
               XML. This transformation in blob version independent, so it
               lives on the base class to avoid duplication.
           **** _getUrl() called to figure out what the MAR URL is for a
                specific patch. This changed starting with V4 blobs. V3 and
                earlier use SeparatedFileUrlsMixin, V4 and later use
                UnifiedFileUrlsMixin.
           ***** _getFtpFilename/_getBouncerProduct called to substitute some
                 paths with real information. This is another part of the blob
                 format that changed starting with V3 blobs. It was later
                 deprecated in V4 and thus not used for UnifiedFileUrlsMixin
                 blobs.
        """

        buildTarget = updateQuery["buildTarget"]
        locale = updateQuery["locale"]
        localeData = self.getLocaleData(buildTarget, locale)

        patches = self._getPatchesXML(localeData, updateQuery, whitelistedDomains, specialForceHosts)
        return patches

    def shouldServeUpdate(self, updateQuery):
        buildTarget = updateQuery['buildTarget']
        locale = updateQuery['locale']
        releaseVersion = self.getApplicationVersion(buildTarget, locale)
        if not releaseVersion:
            self.log.debug("Matching rule has no application version, will not serve update.")
            return False
        releaseVersion = MozillaVersion(releaseVersion)
        queryVersion = MozillaVersion(updateQuery['version'])
        if queryVersion > releaseVersion:
            self.log.debug("Matching rule has older version than request, will not serve update.")
            return False
        elif releaseVersion == queryVersion:
            if updateQuery['buildID'] >= self.getBuildID(updateQuery['buildTarget'], updateQuery['locale']):
                self.log.debug("Matching rule has older buildid than request, will not serve update.")
                return False
        if updateQuery['buildTarget'] not in self['platforms'].keys():
            return False

        return True

    def containsForbiddenDomain(self, product, whitelistedDomains):
        """Returns True if the blob contains any file URLs that contain a
           domain that we're not allowed to serve updates to."""
        # Check the top level URLs, if the exist.
        for c in self.get('fileUrls', {}).values():
            # New-style
            if isinstance(c, dict):
                for from_ in c.values():
                    for url in from_.values():
                        if isForbiddenUrl(url, product, whitelistedDomains):
                            return True
            # Old-style
            else:
                if isForbiddenUrl(c, product, whitelistedDomains):
                    return True

        # And also the locale-level URLs.
        for platform in self.get('platforms', {}).values():
            for locale in platform.get('locales', {}).values():
                for type_ in ('partial', 'complete'):
                    if type_ in locale and 'fileUrl' in locale[type_]:
                        if isForbiddenUrl(locale[type_]['fileUrl'], product,
                                          whitelistedDomains):
                            return True
                for type_ in ('partials', 'completes'):
                    for update in locale.get(type_, {}):
                        if 'fileUrl' in update:
                            if isForbiddenUrl(update["fileUrl"], product,
                                              whitelistedDomains):
                                return True

        return False


class SeparatedFileUrlsMixin(object):

    def _getFtpFilename(self, patchKey, from_):
        return self.get("ftpFilenames", {}).get(patchKey, "")

    def _getBouncerProduct(self, patchKey, from_):
        return self.get("bouncerProducts", {}).get(patchKey, "")

    def _getUrl(self, updateQuery, patchKey, patch, specialForceHosts):
        platformData = self.getPlatformData(updateQuery["buildTarget"])
        if 'fileUrl' in patch:
            url = patch['fileUrl']
        else:
            ftpFilename = self._getFtpFilename(patchKey, patch["from"])
            bouncerProduct = self._getBouncerProduct(patchKey, patch["from"])

            # When we're using a fallback channel it's unlikely
            # we'll have a fileUrl specifically for it, but we
            # should try nonetheless. Non-fallback cases shouldn't
            # be hitting any exceptions here.
            try:
                url = self['fileUrls'][updateQuery['channel']]
            except KeyError:
                try:
                    url = self['fileUrls'][getFallbackChannel(updateQuery['channel'])]
                except KeyError:
                    self.log.debug("Couldn't find fileUrl for")
                    raise

            url = url.replace('%LOCALE%', updateQuery['locale'])
            url = url.replace('%OS_FTP%', platformData['OS_FTP'])
            url = url.replace('%FILENAME%', ftpFilename)
            url = url.replace('%PRODUCT%', bouncerProduct)
            url = url.replace('%OS_BOUNCER%', platformData['OS_BOUNCER'])
        # pass on forcing for special hosts (eg download.m.o for mozilla metrics)
        if updateQuery['force']:
            url = self.processSpecialForceHosts(url, specialForceHosts)

        return url


class SingleUpdateXMLMixin(object):

    def _getPatchesXML(self, localeData, updateQuery, whitelistedDomains, specialForceHosts):
        patches = []
        for patchKey in ("complete", "partial"):
            patch = localeData.get(patchKey)
            if not patch:
                continue

            xml = self._getSpecificPatchXML(patchKey, patchKey, patch, updateQuery, whitelistedDomains, specialForceHosts)
            if xml:
                patches.append(xml)

        return patches


class ReleaseBlobV1(ReleaseBlobBase, SingleUpdateXMLMixin, SeparatedFileUrlsMixin):
    """ This is the legacy format for apps based on Gecko 1.8.0 to 1.9.2, which
    translates to
     * Firefox 1.5 to 3.6.x
     * Thunderbird 1.5 to 3.1.y

    It was deprecated by https://bugzilla.mozilla.org/show_bug.cgi?id=530872 during
    Gecko 2.0 development (aka 1.9.3).
    """
    jsonschema = "apprelease-v1.yml"

    def __init__(self, **kwargs):
        # ensure schema_version is set if we init ReleaseBlobV1 directly
        Blob.__init__(self, **kwargs)
        if 'schema_version' not in self.keys():
            self['schema_version'] = 1

    def getAppv(self, platform, locale):
        return self.getLocaleOrTopLevelParam(platform, locale, 'appv')

    def getExtv(self, platform, locale):
        return self.getLocaleOrTopLevelParam(platform, locale, 'extv')

    def getApplicationVersion(self, platform, locale):
        """ We used extv as the application version for v1 schema, while appv
        may have been a pretty version for users to see"""
        return self.getExtv(platform, locale)

    # TODO: kill me when aus3.m.o is dead, and snippet tests have been
    # converted to unit tests.
    def createSnippets(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        snippets = {}
        buildTarget = updateQuery["buildTarget"]
        locale = updateQuery["locale"]
        localeData = self.getLocaleData(buildTarget, locale)
        for patchKey in ("partial", "complete"):
            patch = localeData.get(patchKey)
            if not patch:
                continue

            fromRelease = self._getFromRelease(patch)
            if fromRelease and not fromRelease.matchesUpdateQuery(updateQuery):
                continue

            url = self._getUrl(updateQuery, patchKey, patch, specialForceHosts)
            if isForbiddenUrl(url, updateQuery['product'], whitelistedDomains):
                break

            snippet = [
                "version=1",
                "type=%s" % patchKey,
                "url=%s" % url,
                "hashFunction=%s" % self["hashFunction"],
                "hashValue=%s" % patch["hashValue"],
                "size=%s" % patch["filesize"],
                "build=%s" % self.getBuildID(buildTarget, locale),
                "appv=%s" % self.getAppv(buildTarget, locale),
                "extv=%s" % self.getExtv(buildTarget, locale),
            ]
            if "detailsUrl" in self:
                details = self["detailsUrl"].replace("%LOCALE%", updateQuery["locale"])
                snippet.append("detailsUrl=%s" % details)
            if "licenseUrl" in self:
                license = self["licenseUrl"].replace("%LOCALE%", updateQuery["locale"])
                snippet.append("licenseUrl=%s" % license)
            if update_type == "major":
                snippet.append("updateType=major")
            snippets[patchKey] = "\n".join(snippet) + "\n"

        if self.get("fakePartials") and "complete" in snippets and "partial" not in snippets:
            partial = snippets["complete"]
            partial = partial.replace("type=complete", "type=partial")
            snippets["partial"] = partial

        for s in snippets.keys():
            self.log.debug('%s\n%s' % (s, snippets[s].rstrip()))
        return snippets

    def _getUpdateLineXML(self, buildTarget, locale, update_type):
        appv = self.getAppv(buildTarget, locale)
        extv = self.getExtv(buildTarget, locale)
        buildid = self.getBuildID(buildTarget, locale)

        updateLine = '    <update type="%s" version="%s" extensionVersion="%s" buildID="%s"' % \
            (update_type, appv, extv, buildid)
        if "detailsUrl" in self:
            details = self["detailsUrl"].replace("%LOCALE%", locale)
            updateLine += ' detailsURL="%s"' % details
        if "licenseUrl" in self:
            license = self["licenseUrl"].replace("%LOCALE%", locale)
            updateLine += ' licenseURL="%s"' % license
        updateLine += ">"

        return updateLine

    def getHeaderXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        """ In order to update some older versions of Firefox without prompting
        them for add-on compatibility, we need to be able to modify the appVersion
        and extVersion attributes. bug 998721 and bug 1174605 have additional
        background on this.
        It would be nicer to do this in _getUpdateLineXML to avoid overriding
        this method, but that doesn't have access to the updateQuery to lookup
        the version making the request.
        """
        xml = super(ReleaseBlobV1, self).getHeaderXML(updateQuery, update_type,
                                                      whitelistedDomains,
                                                      specialForceHosts)

        if self.get("oldVersionSpecialCases"):
            query_ver = MozillaVersion(updateQuery["version"])
            real_appv = self.getAppv(updateQuery["buildTarget"], updateQuery["locale"])
            real_extv = self.getExtv(updateQuery["buildTarget"], updateQuery["locale"])
            if query_ver >= MozillaVersion("2.0") and query_ver < MozillaVersion("3.5"):
                # 2.0 and 3.0 need a fake version, and extVersion omitted
                xml = xml.replace('version="%s"' % real_appv,
                                  'version="%s"' % updateQuery["version"])
                xml = xml.replace('extensionVersion="%s" ' % real_extv, '')
            elif query_ver >= MozillaVersion("3.5") and query_ver < MozillaVersion("3.6"):
                # 3.5 needs extVersion omitted
                xml = xml.replace('extensionVersion="%s" ' % real_extv, '')
            elif query_ver >= MozillaVersion("3.6") and query_ver < MozillaVersion("4.0"):
                # 3.6 needs a fake extensionVersion
                xml = xml.replace('extensionVersion="%s"' % real_extv,
                                  'extensionVersion="%s"' % updateQuery["version"])
            # and we don't use ReleaseBlobV1 to serve anything to 4.0 or later
        return xml


class NewStyleVersionsMixin(object):

    def getAppVersion(self, platform, locale):
        return self.getLocaleOrTopLevelParam(platform, locale, 'appVersion')

    def getDisplayVersion(self, platform, locale):
        return self.getLocaleOrTopLevelParam(platform, locale, 'displayVersion')

    def getPlatformVersion(self, platform, locale):
        return self.getLocaleOrTopLevelParam(platform, locale, 'platformVersion')

    def getApplicationVersion(self, platform, locale):
        """ For v2 schema, appVersion really is the app version """
        return self.getAppVersion(platform, locale)

    def _getUpdateLineXML(self, buildTarget, locale, update_type):
        displayVersion = self.getDisplayVersion(buildTarget, locale)
        appVersion = self.getAppVersion(buildTarget, locale)
        platformVersion = self.getPlatformVersion(buildTarget, locale)
        buildid = self.getBuildID(buildTarget, locale)

        localeData = self.getLocaleData(buildTarget, locale)

        updateLine = '    <update type="%s" displayVersion="%s" appVersion="%s" platformVersion="%s" buildID="%s"' % \
            (update_type, displayVersion, appVersion, platformVersion, buildid)
        if "detailsUrl" in self:
            details = self["detailsUrl"].replace("%LOCALE%", locale)
            updateLine += ' detailsURL="%s"' % details
        if "licenseUrl" in self:
            license = self["licenseUrl"].replace("%LOCALE%", locale)
            updateLine += ' licenseURL="%s"' % license
        if localeData.get("isOSUpdate"):
            updateLine += ' isOSUpdate="true"'
        for attr in self.optional_:
            if attr in self:
                if self.interpolable_ and attr in self.interpolable_:
                    updateLine += ' %s="%s"' % (attr, self[attr].replace("%LOCALE%", locale))
                else:
                    # Responses require lower cased version of True/False for
                    # boolean properties. Strings are sent as stored.
                    value = self[attr]
                    if isinstance(value, bool):
                        value = str(value).lower()
                    updateLine += ' %s="%s"' % (attr, value)
        updateLine += ">"

        return updateLine


class ReleaseBlobV2(ReleaseBlobBase, NewStyleVersionsMixin, SingleUpdateXMLMixin, SeparatedFileUrlsMixin):
    """ Compatible with Gecko 1.9.3a3 and above, ie Firefox/Thunderbird 4.0 and above.

        Client-side changes in
          https://bugzilla.mozilla.org/show_bug.cgi?id=530872
        renamed or introduced several attributes in update.xml

        Changed parameters from ReleaseBlobV1:
         * appv, extv become appVersion, platformVersion, displayVersion
        Added:
         * actions, billboardURL, openURL, notificationURL,
           alertURL, showPrompt, showNeverForVersion, isOSUpdate
        Removed:
         * oldVersionSpecialCases
    """
    jsonschema = "apprelease-v2.yml"

    # for the benefit of get*XML and createSnippets
    optional_ = ('billboardURL', 'showPrompt', 'showNeverForVersion',
                 'actions', 'openURL', 'notificationURL', 'alertURL')
    # params that can have %LOCALE% interpolated
    interpolable_ = ('billboardURL', 'openURL', 'notificationURL', 'alertURL')

    def __init__(self, **kwargs):
        # ensure schema_version is set if we init ReleaseBlobV2 directly
        Blob.__init__(self, **kwargs)
        if 'schema_version' not in self.keys():
            self['schema_version'] = 2

    # TODO: kill me when aus3.m.o is dead, and snippet tests have been
    # converted to unit tests.
    def createSnippets(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        snippets = {}
        buildTarget = updateQuery["buildTarget"]
        locale = updateQuery["locale"]
        localeData = self.getLocaleData(buildTarget, locale)
        for patchKey in ("partial", "complete"):
            patch = localeData.get(patchKey)
            if not patch:
                continue

            fromRelease = self._getFromRelease(patch)
            if fromRelease and not fromRelease.matchesUpdateQuery(updateQuery):
                continue

            url = self._getUrl(updateQuery, patchKey, patch, specialForceHosts)
            if isForbiddenUrl(url, updateQuery['product'], whitelistedDomains):
                break

            snippet = [
                "version=2",
                "type=%s" % patchKey,
                "url=%s" % url,
                "hashFunction=%s" % self["hashFunction"],
                "hashValue=%s" % patch["hashValue"],
                "size=%s" % patch["filesize"],
                "build=%s" % self.getBuildID(buildTarget, locale),
                "displayVersion=%s" % self.getDisplayVersion(buildTarget, locale),
                "appVersion=%s" % self.getAppVersion(buildTarget, locale),
                "platformVersion=%s" % self.getPlatformVersion(buildTarget, locale),
            ]
            if "detailsUrl" in self:
                details = self["detailsUrl"].replace("%LOCALE%", updateQuery["locale"])
                snippet.append("detailsUrl=%s" % details)
            if "licenseUrl" in self:
                license = self["licenseUrl"].replace("%LOCALE%", updateQuery["locale"])
                snippet.append("licenseUrl=%s" % license)
            if update_type == "major":
                snippet.append("updateType=major")
            for attr in self.optional_:
                if attr in self:
                    if attr in self.interpolable_:
                        snippet.append("%s=%s" % (attr, self[attr].replace("%LOCALE%", updateQuery["locale"])))
                    else:
                        snippet.append("%s=%s" % (attr, self[attr]))
            snippets[patchKey] = "\n".join(snippet) + "\n"

        for s in snippets.keys():
            self.log.debug('%s\n%s' % (s, snippets[s].rstrip()))
        return snippets


class MultipleUpdatesXMLMixin(object):

    def _getPatchesXML(self, localeData, updateQuery, whitelistedDomains, specialForceHosts):
        patches = []
        for patchKey, patchType in (("completes", "complete"), ("partials", "partial")):
            for patch in localeData.get(patchKey, {}):
                xml = self._getSpecificPatchXML(patchKey, patchType, patch, updateQuery, whitelistedDomains, specialForceHosts)
                if xml:
                    patches.append(xml)
                    break

        return patches


class ReleaseBlobV3(ReleaseBlobBase, NewStyleVersionsMixin, MultipleUpdatesXMLMixin, SeparatedFileUrlsMixin):
    """ Compatible with Gecko 1.9.3a3 and above, ie Firefox/Thunderbird 4.0 and above.

        This is an internal change to add functionality to Balrog.

        Changes from ReleaseBlobV2:
             * support multiple partials
               * remove "partial" and "complete" from locale level
               * add "partials" and "completes" to locale level, ftpFilenames, and bouncerProducts
    """
    jsonschema = "apprelease-v3.yml"

    # for the benefit of get*XML
    optional_ = ('billboardURL', 'showPrompt', 'showNeverForVersion',
                 'actions', 'openURL', 'notificationURL', 'alertURL')
    # params that can have %LOCALE% interpolated
    interpolable_ = ('billboardURL', 'openURL', 'notificationURL', 'alertURL')

    def __init__(self, **kwargs):
        # ensure schema_version is set if we init ReleaseBlobV3 directly
        Blob.__init__(self, **kwargs)
        if 'schema_version' not in self.keys():
            self['schema_version'] = 3

    def _getFtpFilename(self, patchKey, from_):
        return self.get("ftpFilenames", {}).get(patchKey, {}).get(from_, "")

    def _getBouncerProduct(self, patchKey, from_):
        return self.get("bouncerProducts", {}).get(patchKey, {}).get(from_, "")

    def createSnippets(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        # We have no tests that require this, probably not worthwhile to implement.
        return {}


class UnifiedFileUrlsMixin(object):

    def _getUrl(self, updateQuery, patchKey, patch, specialForceHosts):
        platformData = self.getPlatformData(updateQuery["buildTarget"])
        from_ = patch["from"]
        # A fileUrl in the deep-down patch section takes priority over anything
        # else.
        if 'fileUrl' in patch:
            url = patch['fileUrl']
        else:
            # There's three "channels" that any given request could get
            # a fileUrl from, in order of preference:
            # 1) Its exact specified channel.
            # 2) Its fallback channel.
            # 3) In the catch-all "channel" ("*").
            channels = [
                updateQuery['channel'],
                getFallbackChannel(updateQuery['channel']),
                "*",
            ]
            url = None
            for c in channels:
                url = self.get("fileUrls", {}).get(c, {}).get(patchKey, {}).get(from_)
                if url:
                    break

            # If we still can't find a fileUrl, we cannot fulfill this request.
            if not url:
                self.log.debug("Couldn't find fileUrl")
                raise ValueError("Couldn't find fileUrl")

            url = url.replace('%LOCALE%', updateQuery['locale'])
            url = url.replace('%OS_FTP%', platformData['OS_FTP'])
            url = url.replace('%OS_BOUNCER%', platformData['OS_BOUNCER'])

        # pass on forcing for special hosts (eg download.m.o for mozilla metrics)
        if updateQuery['force']:
            url = self.processSpecialForceHosts(url, specialForceHosts)

        return url


class ReleaseBlobV4(ReleaseBlobBase, NewStyleVersionsMixin, MultipleUpdatesXMLMixin, UnifiedFileUrlsMixin):
    """ Compatible with Gecko 1.9.3a3 and above, ie Firefox/Thunderbird 4.0 and above.

    This is an internal change to add functionality to Balrog.

    Changes from ReleaseBlobV3:
        * Support pushing release builds to the beta channel with bouncer support (bug 1021026)
        ** Combine fileUrls, bouncerProducts, and ftpFilenames into a larger data structure,
           still called "fileUrls". (See below for a more detailed description.)
    """
    jsonschema = "apprelease-v4.yml"

    # for the benefit of get*XML
    optional_ = ('billboardURL', 'showPrompt', 'showNeverForVersion',
                 'actions', 'openURL', 'notificationURL', 'alertURL')
    # params that can have %LOCALE% interpolated
    interpolable_ = ('billboardURL', 'openURL', 'notificationURL', 'alertURL')

    def __init__(self, **kwargs):
        # ensure schema_version is set if we init ReleaseBlobV4 directly
        Blob.__init__(self, **kwargs)
        if 'schema_version' not in self.keys():
            self['schema_version'] = 4

    @classmethod
    def fromV3(cls, v3Blob):
        """Creates a v4 blob based on the v3 blob given."""
        v4Blob = cls()
        v4Blob.update(v3Blob)
        # These 3 sections changed between v3 and v4, we'll fill out the data
        # in the new format, but we need to clear them out first.
        for k in ('fileUrls', 'ftpFilenames', 'bouncerProducts'):
            if k in v4Blob:
                del v4Blob[k]

        v4Blob["schema_version"] = 4
        # If "fileUrls" doesn't exist in the v3 blob, we have nothing else to do.
        # Technically, bouncerProducts and/or ftpFilenames could exist in it,
        # but they have no effect when fileUrls isn't present.
        if "fileUrls" not in v3Blob:
            return v4Blob

        v4Blob["fileUrls"] = {}
        for channel, baseUrl in v3Blob.get('fileUrls').iteritems():
            if channel not in v4Blob["fileUrls"]:
                v4Blob["fileUrls"][channel] = {}

            # Each fileUrl should have one (no more no less) of the matchstrs below.
            # Technically, they could have neither, but if we had blob validation,
            # that probably be considered an invalid state. Probably not worth
            # supporting here.
            for matchstr, lookup in (("%PRODUCT%", "bouncerProducts"), ("%FILENAME%", "ftpFilenames")):
                if matchstr in baseUrl:
                    # If we've found a match, we need to replicate the inner structure
                    # of the lookup dict, substitute the match in the url,
                    # and add it to the new fileUrls.
                    for patchKey, products in v3Blob.get(lookup, {}).iteritems():
                        if patchKey not in v4Blob["fileUrls"][channel]:
                            v4Blob["fileUrls"][channel][patchKey] = {}
                        for from_, product in products.iteritems():
                            url = baseUrl.replace(matchstr, product)
                            v4Blob["fileUrls"][channel][patchKey][from_] = url

        return v4Blob


class ReleaseBlobV5(ReleaseBlobBase, NewStyleVersionsMixin, MultipleUpdatesXMLMixin, UnifiedFileUrlsMixin):
    """ Compatible with Gecko 19.0 and above, ie Firefox/Thunderbird 19.0 and above.

    Driven by a client-side change made in
      https://bugzilla.mozilla.org/show_bug.cgi?id=813322

    Changes from ReleaseBlobV4:
        * Support optional promptWaitTime attribute
    """
    jsonschema = "apprelease-v5.yml"

    # for the benefit of get*XML
    optional_ = ('billboardURL', 'showPrompt', 'showNeverForVersion',
                 'actions', 'openURL', 'notificationURL', 'alertURL',
                 'promptWaitTime')
    # params that can have %LOCALE% interpolated
    interpolable_ = ('billboardURL', 'openURL', 'notificationURL', 'alertURL')

    def __init__(self, **kwargs):
        # ensure schema_version is set if we init ReleaseBlobV5 directly
        Blob.__init__(self, **kwargs)
        if 'schema_version' not in self.keys():
            self['schema_version'] = 5


class DesupportBlob(Blob):
    """ This blob is used to inform users that their OS is no longer supported. This is available
    on the client side since Firefox 24 (bug 843497).

    The XML should look like this (whitespace for clarity & consistency only):
        <?xml version="1.0"?>
        <updates>
            <update type="major" unsupported="true" detailsURL="http://moreinfo">
            </update>
        </updates>
    """
    jsonschema = "desupport.yml"

    def __init__(self, **kwargs):
        # ensure schema_version is set if we init DesupportBlob directly
        Blob.__init__(self, **kwargs)
        if 'schema_version' not in self.keys():
            self['schema_version'] = 50

    def shouldServeUpdate(self, updateQuery):
        # desupport messages should always be returned
        return True

    def getHeaderXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        return ''

    def getInnerXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        tmp_url = self['detailsUrl'].replace("%LOCALE%", updateQuery['locale']).replace("%VERSION%", updateQuery['version'])
        xml = []
        xml.append('    <update type="%s" unsupported="true" detailsURL="%s" displayVersion="%s">' % (update_type, tmp_url, self["displayVersion"]))
        return xml

    def getFooterXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        return '</update>'

    def containsForbiddenDomain(self, product, whitelistedDomains):
        if isForbiddenUrl(self.get('detailsUrl', None), product, whitelistedDomains):
            return True
        return False
