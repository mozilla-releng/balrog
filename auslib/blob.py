import re
import simplejson as json

import logging
log = logging.getLogger(__name__)

from auslib import dbo
from auslib.AUS import isSpecialURL, containsForbiddenDomain, getFallbackChannel
from auslib.util.versions import MozillaVersion


def isValidBlob(format_, blob, topLevel=True):
    """Decides whether or not 'blob' is valid based on the format provided.
       Validation follows these rules:
       1) If there's no format at all, the blob is valid.
       2) If the format contains a '*' key, all key names are accepted.
       3) If the format doesn't contain a '*' key, all keys in the blob must
          also be present in the format.
       3) If the value for the key is None, all values for that key are valid.
       4) If the value for the key is a dictionary, validate it.
    """
    # If there's no format at all, we assume the blob is valid.
    if not format_:
        return True
    # If the blob isn't a dictionary-like or list-like object, it's not valid!
    if not isinstance(blob, (dict,list)):
        return False
    # If the blob format has a schema_version then that's a mandatory int
    if topLevel and 'schema_version' in format_:
        if 'schema_version' not in blob or not isinstance(blob['schema_version'], int):
            log.debug("blob is not valid because schema_version is not defined, or non-integer")
            return False
    # check the blob against the format
    if isinstance(blob, dict):
        for key in blob.keys():
            # A '*' key in the format means that all key names in the blob are accepted.
            if '*' in format_:
                # But we still need to validate the sub-blob, if it exists.
                if format_['*'] and not isValidBlob(format_['*'], blob[key], topLevel=False):
                    log.debug("blob is not valid because of key '%s'" % key)
                    return False
            # If there's no '*' key, we need to make sure the key name is valid
            # and the sub-blob is valid, if it exists.
            elif key not in format_ or not isValidBlob(format_[key], blob[key], topLevel=False):
                log.debug("blob is not valid because of key '%s'" % key)
                return False
    else:
        # Empty lists are not allowed. These can be represented by leaving out the key entirely.
        if len(blob) == 0:
            return False
        for subBlob in blob:
            # Other than the empty list check above, we can hand off the rest
            # of the validation to another isValidBlob call!
            if not isValidBlob(format_[0], subBlob, topLevel=False):
                return False
    return True

def createBlob(data):
    """Takes a string form of a blob (eg from DB or API) and converts into an
    actual blob, taking care to notice the schema"""
    data = json.loads(data)
    try:
        if data['schema_version'] == 1:
            return ReleaseBlobV1(**data)
        elif data['schema_version'] == 2:
            return ReleaseBlobV2(**data)
        elif data['schema_version'] == 3:
            return ReleaseBlobV3(**data)
        else:
            raise ValueError("schema_version is unknown")
    except KeyError:
        raise ValueError("schema_version is not set")

class Blob(dict):
    """See isValidBlob for details on how format is used to validate blobs."""
    format_ = {}

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        dict.__init__(self, *args, **kwargs)

    def matchesUpdateQuery(self, updateQuery):
        self.log.debug("Trying to match update query to %s" % self["name"])
        buildTarget = updateQuery["buildTarget"]
        buildID = updateQuery["buildID"]
        locale = updateQuery["locale"]

        if buildTarget in self["platforms"]:
            try:
                releaseBuildID = self.getBuildID(buildTarget, locale)
            # Platform doesn't exist in release, clearly it's not a match!
            except KeyError:
                return False
            self.log.debug("releasePlat buildID is: %s", releaseBuildID)
            if buildID == releaseBuildID:
                self.log.debug("Query matched!")
                return True

    def isValid(self):
        """Decides whether or not this blob is valid based."""
        self.log.debug('Validating blob %s' % self)
        return isValidBlob(self.format_, self)

    def loadJSON(self, data):
        """Replaces this blob's contents with parsed contents of the json
           string provided."""
        self.clear()
        self.update(json.loads(data))

    def getJSON(self):
        """Returns a JSON formatted version of this blob."""
        return json.dumps(self)

    def getResolvedPlatform(self, platform):
        return self['platforms'][platform].get('alias', platform)

    def getPlatformData(self, platform):
        platform = self.getResolvedPlatform(platform)
        return self['platforms'][platform]

    def getLocaleOrTopLevelParam(self, platform, locale, param):
        try:
            platform = self.getResolvedPlatform(platform)
            return self['platforms'][platform]['locales'][locale][param]
        except KeyError:
            try:
                return self[param]
            except KeyError:
                return None

    def getBuildID(self, platform, locale):
        platform = self.getResolvedPlatform(platform)
        if locale not in self['platforms'][platform]['locales']:
            raise KeyError("No such locale '%s' in platform '%s'" % (locale, platform))
        try:
            return self['platforms'][platform]['locales'][locale]['buildID']
        except KeyError:
            return self['platforms'][platform]['buildID']

    def _getUrl(self, updateQuery, patch, specialForceHosts, ftpFilename, bouncerProduct):
        platformData = self.getPlatformData(updateQuery["buildTarget"])
        if 'fileUrl' in patch:
            url = patch['fileUrl']
        else:
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
        if updateQuery['force'] and isSpecialURL(url, specialForceHosts):
            if '?' in url:
                url += '&force=1'
            else:
                url += '?force=1'

        return url

    def _getSpecificPatchXML(self, patchKey, patchType, patch, updateQuery, whitelistedDomains, specialForceHosts):
        try:
            fromRelease = dbo.releases.getReleaseBlob(name=patch["from"])
        except KeyError:
            fromRelease = None

        ftpFilename = self._getFtpFilename(patchKey, patch["from"])
        bouncerProduct = self._getBouncerProduct(patchKey, patch["from"])

        if patch["from"] != "*" and fromRelease and not fromRelease.matchesUpdateQuery(updateQuery):
            return None

        url = self._getUrl(updateQuery, patch, specialForceHosts, ftpFilename, bouncerProduct)
        # TODO: should be raising a bigger alarm here, or aborting
        # the update entirely? Right now, another patch type could still
        # return an update. Eg, the partial could contain a forbidden domain
        # but the complete could still return an update from an accepted one.
        if containsForbiddenDomain(url, whitelistedDomains):
            return None

        return '        <patch type="%s" URL="%s" hashFunction="%s" hashValue="%s" size="%s"/>' % \
            (patchType, url, self["hashFunction"], patch["hashValue"], patch["filesize"])

    def createXML(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        """This method is the entry point for update XML creation for all Gecko
           app blobs. However, the XML and underlying data has changed over
           time, so there is a lot of indirection and calls factored out to
           subclasses. Below is a brief description of the flow of control that
           should help in understanding this code. Inner methods that are
           shared between blob versions live in Mixin classes so that they can
           be easily shared. Inner methods that only apply to a single blob
           version live on concrete blob classes (but should be moved if they
           need to be shared in the future).
           * createXML() called by web layer, lives on this base class.
           ** _getUpdateLineXML() called to get information that is independent
              of specific MARs. Most notably, version information changed
              starting with V2 blobs.
           ** _getPatchesXML() called to get the information that describes
              specific MARs. Where in the blob this information comes from
              changed significantly starting with V3 blobs.
           *** _getPatchSpecificXML() called to translate MAR information into
               XML. This transformation in blob version independent, so it
               lives on the base class to avoid duplication.
           **** _getFtpFilename/_getBouncerProduct called to substitute some
                paths with real information. This is another part of the blob
                format that changed starting with V3 blobs.
        """

        buildTarget = updateQuery["buildTarget"]
        locale = updateQuery["locale"]
        localeData = self.getPlatformData(buildTarget)["locales"][locale]

        updateLine = self._getUpdateLineXML(buildTarget, locale, update_type)
        patches = self._getPatchesXML(localeData, updateQuery, whitelistedDomains, specialForceHosts)

        xml = ['<?xml version="1.0"?>']
        xml.append('<updates>')
        if patches:
            xml.append(updateLine)
            xml.extend(patches)
            xml.append('    </update>')
        xml.append('</updates>')
        # ensure valid xml by using the right entity for ampersand
        return re.sub('&(?!amp;)','&amp;', '\n'.join(xml))

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

        return True


class SingleUpdateXMLMixin(object):
    def _getFtpFilename(self, patchKey, from_):
        return self.get("ftpFilenames", {}).get(patchKey, "")

    def _getBouncerProduct(self, patchKey, from_):
        return self.get("bouncerProducts", {}).get(patchKey, "")

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


class ReleaseBlobV1(Blob, SingleUpdateXMLMixin):
    format_ = {
        'name': None,
        'schema_version': None,
        'extv': None,
        'appv': None,
        'fileUrls': {
            '*': None
        },
        'ftpFilenames': {
            '*': None
        },
        'bouncerProducts': {
            '*': None
        },
        'hashFunction': None,
        'detailsUrl': None,
        'licenseUrl': None,
        'fakePartials': None,
        'platforms': {
            '*': {
                'alias': None,
                'buildID': None,
                'OS_BOUNCER': None,
                'OS_FTP': None,
                'locales': {
                    '*': {
                        'buildID': None,
                        'extv': None,
                        'appv': None,
                        'partial': {
                            'filesize': None,
                            'from': None,
                            'hashValue': None,
                            'fileUrl': None
                        },
                        'complete': {
                            'filesize': None,
                            'from': None,
                            'hashValue': None,
                            'fileUrl': None
                        }
                    }
                }
            }
        }
    }

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
        platformData = self.getPlatformData(buildTarget)
        localeData = platformData["locales"][locale]
        for patchKey in ("partial", "complete"):
            patch = localeData.get(patchKey)
            if not patch:
                continue

            try:
                fromRelease = dbo.releases.getReleaseBlob(name=patch["from"])
            except KeyError:
                fromRelease = None
            ftpFilename = self.get("ftpFilenames", {}).get(patchKey)
            bouncerProduct = self.get("bouncerProducts", {}).get(patchKey)

            if patch["from"] != "*" and fromRelease and not fromRelease.matchesUpdateQuery(updateQuery):
                continue

            url = self._getUrl(updateQuery, patch, specialForceHosts, ftpFilename, bouncerProduct)
            if containsForbiddenDomain(url, whitelistedDomains):
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
        localeData = self.getPlatformData(buildTarget)["locales"][locale]

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
                updateLine += ' %s="%s"' % (attr, self[attr])
        updateLine += ">"

        return updateLine


class ReleaseBlobV2(Blob, NewStyleVersionsMixin, SingleUpdateXMLMixin):
    """ Changes from ReleaseBlobV1:
         * appv, extv become appVersion, platformVersion, displayVersion
        Added:
         * actions, billboardURL, openURL, notificationURL,
           alertURL, showPrompt, showSurvey, showNeverForVersion, isOSUpdate
    """
    format_ = {
        'name': None,
        'schema_version': None,
        'appVersion': None,
        'displayVersion': None,
        'platformVersion': None,
        'fileUrls': {
            '*': None
        },
        'ftpFilenames': {
            '*': None
        },
        'bouncerProducts': {
            '*': None
        },
        'hashFunction': None,
        'detailsUrl': None,
        'licenseUrl': None,
        'actions': None,
        'billboardURL': None,
        'openURL': None,
        'notificationURL': None,
        'alertURL': None,
        'showPrompt': None,
        'showNeverForVersion': None,
        'showSurvey': None,
        'platforms': {
            '*': {
                'alias': None,
                'buildID': None,
                'OS_BOUNCER': None,
                'OS_FTP': None,
                'locales': {
                    '*': {
                        'isOSUpdate': None,
                        'buildID': None,
                        'appVersion': None,
                        'displayVersion': None,
                        'platformVersion': None,
                        'partial': {
                            'filesize': None,
                            'from': None,
                            'hashValue': None,
                            'fileUrl': None
                        },
                        'complete': {
                            'filesize': None,
                            'from': None,
                            'hashValue': None,
                            'fileUrl': None
                        }
                    }
                }
            }
        }
    }
    # for the benefit of createXML and createSnippetv2
    optional_ = ('billboardURL', 'showPrompt', 'showNeverForVersion',
                 'showSurvey', 'actions', 'openURL', 'notificationURL',
                 'alertURL')

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
        platformData = self.getPlatformData(buildTarget)
        localeData = platformData["locales"][locale]
        for patchKey in ("partial", "complete"):
            patch = localeData.get(patchKey)
            if not patch:
                continue

            try:
                fromRelease = dbo.releases.getReleaseBlob(name=patch["from"])
            except KeyError:
                fromRelease = None
            ftpFilename = self.get("ftpFilenames", {}).get(patchKey)
            bouncerProduct = self.get("bouncerProducts", {}).get(patchKey)

            if patch["from"] != "*" and fromRelease and not fromRelease.matchesUpdateQuery(updateQuery):
                continue

            url = self._getUrl(updateQuery, patch, specialForceHosts, ftpFilename, bouncerProduct)
            if containsForbiddenDomain(url, whitelistedDomains):
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
                    snippet.append("%s=%s" % (attr, self[attr]))
            snippets[patchKey] = "\n".join(snippet) + "\n"

        for s in snippets.keys():
            self.log.debug('%s\n%s' % (s, snippets[s].rstrip()))
        return snippets


class MultipleUpdatesXMLMixin(object):
    def _getFtpFilename(self, patchKey, from_):
        return self.get("ftpFilenames", {}).get(patchKey, {}).get(from_, "")

    def _getBouncerProduct(self, patchKey, from_):
        return self.get("bouncerProducts", {}).get(patchKey, {}).get(from_, "")

    def _getPatchesXML(self, localeData, updateQuery, whitelistedDomains, specialForceHosts):
        patches = []
        for patchKey, patchType in (("completes", "complete"), ("partials", "partial")):
            for patch in localeData.get(patchKey, {}):
                xml = self._getSpecificPatchXML(patchKey, patchType, patch, updateQuery, whitelistedDomains, specialForceHosts)
                if xml:
                    patches.append(xml)
                    break

        return patches


class ReleaseBlobV3(Blob, NewStyleVersionsMixin, MultipleUpdatesXMLMixin):
    """ Changes from ReleaseBlobV2:
         * support multiple partials
           * remove "partial" and "complete" from locale level
           * add "partials" and "completes" to locale level, ftpFilenames, and bouncerProducts
    """
    format_ = {
        'name': None,
        'schema_version': None,
        'appVersion': None,
        'displayVersion': None,
        'platformVersion': None,
        'fileUrls': {
            '*': None
        },
        'ftpFilenames': {
            'partials': {
                '*': None
            },
            'completes': {
                '*': None
            }
        },
        'bouncerProducts': {
            'partials': {
                '*': None
            },
            'completes': {
                '*': None
            }
        },
        'hashFunction': None,
        'detailsUrl': None,
        'licenseUrl': None,
        'actions': None,
        'billboardURL': None,
        'openURL': None,
        'notificationURL': None,
        'alertURL': None,
        'showPrompt': None,
        'showNeverForVersion': None,
        'showSurvey': None,
        'platforms': {
            '*': {
                'alias': None,
                'buildID': None,
                'OS_BOUNCER': None,
                'OS_FTP': None,
                'locales': {
                    '*': {
                        'isOSUpdate': None,
                        'buildID': None,
                        'appVersion': None,
                        'displayVersion': None,
                        'platformVersion': None,
                        # Using lists instead of dicts for multiple updates
                        # gives us a way to reduce load a bit. As this is
                        # iterated over, each "from" release is looked up
                        # in the database. If the "from" releases that we
                        # we expect to be the most common are earlier in the
                        # list, we can avoid looking up every single entry.
                        # The server doesn't know anything about which order is
                        # best, so we assume the client will make the right
                        # decision about this.
                        'partials': [
                            {
                                'filesize': None,
                                'from': None,
                                'hashValue': None,
                                'fileUrl': None
                            }
                        ],
                        'completes': [
                            {
                                'filesize': None,
                                'from': None,
                                'hashValue': None,
                                'fileUrl': None
                            }
                        ]
                    }
                }
            }
        }
    }
    # for the benefit of createXML and createSnippetv2
    optional_ = ('billboardURL', 'showPrompt', 'showNeverForVersion',
                 'showSurvey', 'actions', 'openURL', 'notificationURL',
                 'alertURL')

    def __init__(self, **kwargs):
        # ensure schema_version is set if we init ReleaseBlobV3 directly
        Blob.__init__(self, **kwargs)
        if 'schema_version' not in self.keys():
            self['schema_version'] = 3

    def createSnippets(self, updateQuery, update_type, whitelistedDomains, specialForceHosts):
        # We have no tests that require this, probably not worthwhile to implement.
        return {}
