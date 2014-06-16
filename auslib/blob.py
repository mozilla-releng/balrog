import simplejson as json

import logging
log = logging.getLogger(__name__)

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

    def isValid(self):
        """Decides whether or not this blob is valid based."""
        log.debug('Validating blob %s' % self)
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


class ReleaseBlobV1(Blob):
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


class ReleaseBlobV2(Blob, NewStyleVersionsMixin):
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


class ReleaseBlobV3(Blob, NewStyleVersionsMixin):
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
