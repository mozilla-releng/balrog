from os import path
import simplejson as json

import jsonschema

import yaml

import logging
log = logging.getLogger(__name__)

from auslib.AUS import isSpecialURL


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
    if not isinstance(blob, (dict, list)):
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
    # These imports need to be done here to avoid errors due to circular
    # between this module and specific blob modules like apprelease.
    from auslib.blobs.apprelease import ReleaseBlobV1, ReleaseBlobV2, ReleaseBlobV3, \
        ReleaseBlobV4, DesupportBlob
    from auslib.blobs.gmp import GMPBlobV1
    from auslib.blobs.settings import SettingsBlob
    from auslib.blobs.whitelist import WhitelistBlobV1

    blob_map = {
        1: ReleaseBlobV1,
        2: ReleaseBlobV2,
        3: ReleaseBlobV3,
        4: ReleaseBlobV4,
        50: DesupportBlob,
        1000: GMPBlobV1,
        2000: SettingsBlob,
        3000: WhitelistBlobV1
    }

    if isinstance(data, basestring):
        data = json.loads(data)
    schema_version = data.get("schema_version")

    if not schema_version:
        raise ValueError("schema_version is not set")
    if schema_version not in blob_map:
        raise ValueError("schema_version is unknown")

    return blob_map[schema_version](**data)


class Blob(dict):
    """See isValidBlob for details on how format is used to validate blobs."""
    format_ = {}

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.__class__.__name__)
        self.cached_schemas = {}
        dict.__init__(self, *args, **kwargs)

    def isValid(self):
        """Decides whether or not this blob is valid based."""
        self.log.debug('Validating blob %s' % self)
        if hasattr(self, "jsonschema"):
            schema = self.getSchema()
            # raises exception if broken
            jsonschema.validate(self, schema)
            return True
        return isValidBlob(self.format_, self)

    def getSchema(self):
        if self.jsonschema in self.cached_schemas:
            return self.cached_schemas[self.jsonschema]

        schema = yaml.load(open(path.join(path.dirname(path.abspath(__file__)), "schemas", self.jsonschema)))
        self.cached_schemas[self.jsonschema] = self.cached_schemas
        return schema

    def loadJSON(self, data):
        """Replaces this blob's contents with parsed contents of the json
           string provided."""
        self.clear()
        self.update(json.loads(data))

    def getJSON(self):
        """Returns a JSON formatted version of this blob."""
        return json.dumps(self)

    def shouldServeUpdate(self, updateQuery):
        """Should be implemented by subclasses. In the event that it's not,
        False is the safest thing to return (it will fail closed instead of
        failing open)."""
        return False

    def processSpecialForceHosts(self, url, specialForceHosts):
        if isSpecialURL(url, specialForceHosts):
            if '?' in url:
                url += '&force=1'
            else:
                url += '?force=1'
        return url
