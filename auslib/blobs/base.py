from os import path
import simplejson as json

import jsonschema

import yaml

import logging

from auslib.AUS import isSpecialURL
from auslib.global_state import cache


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
    jsonschema = None

    def __init__(self, *args, **kwargs):
        super(Blob, self).__init__(self, *args, **kwargs)
        # Blobs need to be pickable to go into the cache properly. Pickling
        # extendes to all instance-level attributes, and our Loggers are not
        # pickleable. Moving them to the class level avoids this issue without
        # the need for subclasses to worry about instantiating their own
        # Loggers.
        self.__class__.log = logging.getLogger(self.__class__.__name__)

    def isValid(self):
        """Decides whether or not this blob is valid based."""
        self.log.debug('Validating blob %s' % self)
        schema = self.getSchema()
        # raises exception if broken
        jsonschema.validate(self, schema)
        return True

    def getSchema(self):
        def loadSchema():
            return yaml.load(open(path.join(path.dirname(path.abspath(__file__)), "schemas", self.jsonschema)))

        return cache.get("blob_schema", self.jsonschema, loadSchema)

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
