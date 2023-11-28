import json
import logging
from os import path

import jsonschema
import yaml

# To enable shared jsonschema validators
import auslib.util.jsonschema_validators  # noqa
from auslib.errors import BlobValidationError
from auslib.global_state import cache


def createBlob(data):
    """Takes a string form of a blob (eg from DB or API) and converts into an
    actual blob, taking care to notice the schema"""
    # These imports need to be done here to avoid errors due to circular
    # between this module and specific blob modules like apprelease.
    from auslib.blobs.apprelease import (
        DesupportBlob,
        ReleaseBlobV1,
        ReleaseBlobV2,
        ReleaseBlobV3,
        ReleaseBlobV4,
        ReleaseBlobV5,
        ReleaseBlobV6,
        ReleaseBlobV8,
        ReleaseBlobV9,
    )
    from auslib.blobs.gmp import GMPBlobV1
    from auslib.blobs.guardian import GuardianBlob
    from auslib.blobs.superblob import SuperBlob
    from auslib.blobs.systemaddons import SystemAddonsBlob

    blob_map = {
        1: ReleaseBlobV1,
        2: ReleaseBlobV2,
        3: ReleaseBlobV3,
        4: ReleaseBlobV4,
        5: ReleaseBlobV5,
        6: ReleaseBlobV6,
        8: ReleaseBlobV8,
        9: ReleaseBlobV9,
        50: DesupportBlob,
        1000: GMPBlobV1,
        4000: SuperBlob,
        5000: SystemAddonsBlob,
        10000: GuardianBlob,
    }

    if isinstance(data, str):
        data = json.loads(data)
    schema_version = data.get("schema_version")

    if not schema_version:
        raise BlobValidationError("Invalid Blob", errors=["schema_version is not set"])
    if schema_version not in blob_map:
        raise BlobValidationError("Invalid Blob", errors=["schema_version is unknown"])

    return blob_map[schema_version](**data)


def merge_lists(*lists):
    """Merge an arbitrary number of lists together, keeping only the unique
    items, and not worrying about order. This is essentially a hack to treat
    lists in blobs as sets. In an ideal world, that's what they'd be, but
    because we use jsonschema for validation, we cannot use proper sets."""
    result = []
    for list in lists:
        for i in list:
            if i not in result or not isinstance(i, type(result[result.index(i)])):
                result.append(i)
    return result


def merge_dicts(ancestor, left, right):
    """Perform a 3-way merge on dictonaries. We used to use an external library
    for this, but we replaced it with this because our merge can be a bit more
    liberal than the general case. Specifically:

     - Lists are treated as sets (see above for details)
     - A type mismatch of unicode vs string is OK as long as the text is the same
       (Any other type mismatches result in a failure to merge.)
    """
    # We can't use "logging" directly, because it ignores our custom code in log.py
    log = logging.getLogger(__name__)
    result = {}
    dicts = (ancestor, left, right)
    for key in set(key for d in dicts for key in d.keys()):
        # Extra logging information to help debug https://bugzilla.mozilla.org/show_bug.cgi?id=1501167
        # This is a very large message, so we limit it as much as possible to reduce spam.
        if key == "completes" and ancestor.get("appVersion") and "a1" not in ancestor["appVersion"]:
            log.warning("Ancestor is: %s", ancestor.get(key))
            log.warning("Left is: %s", left.get(key))
            log.warning("Right is: %s", right.get(key))
        key_types = set([type(d.get(key)) for d in dicts])
        key_types.discard(type(None))
        encoded_str_key = str(key.encode("ascii", "replace"), "utf-8")
        if len(key_types) > 1 and key_types != set([str]):
            raise ValueError("Cannot merge blobs: type mismatch for '{}'".format(encoded_str_key))

        if any(isinstance(d.get(key), dict) for d in dicts):
            result[key] = merge_dicts(*[d.get(key, {}) for d in dicts])
        elif any(isinstance(d.get(key), list) for d in dicts):
            result[key] = merge_lists(*[d.get(key, []) for d in dicts])
        else:
            if key in ancestor:
                if key in left and key in right and ancestor[key] != left[key] and ancestor[key] != right[key]:
                    log.warning("Ancestor is: %s", ancestor)
                    log.warning("Left is: %s", left)
                    log.warning("Right is: %s", right)
                    raise ValueError("Cannot merge blobs: left and right are both changing '{}'".format(encoded_str_key))
                if key in left and ancestor[key] != left.get(key):
                    result[key] = left[key]
                elif key in right and ancestor[key] != right.get(key):
                    result[key] = right[key]
                else:
                    result[key] = ancestor[key]
            else:
                if key in left and key in right and left[key] != right[key]:
                    log.warning("Ancestor is: %s", ancestor)
                    log.warning("Left is: %s", left)
                    log.warning("Right is: %s", right)
                    raise ValueError("Cannot merge blobs: left and right are both changing '{}'".format(encoded_str_key))
                if key in left:
                    result[key] = left[key]
                elif key in right:
                    result[key] = right[key]
                else:
                    raise KeyError("Couldn't find value for key '{}'".format(key))

    return result


class Blob(dict):
    jsonschema = None

    def __init__(self, *args, **kwargs):
        super(Blob, self).__init__(self, *args, **kwargs)
        # Blobs need to be pickable to go into the cache properly. Pickling
        # extendes to all instance-level attributes, and our Loggers are not
        # pickleable. Moving them to the class level avoids this issue without
        # the need for subclasses to worry about instantiating their own
        # Loggers.
        logger_name = "{0}.{1}".format(self.__class__.__module__, self.__class__.__name__)
        self.__class__.log = logging.getLogger(logger_name)

    def validate(self, product, allowlistedDomains):
        """Raises a BlobValidationError if the blob is invalid."""
        self.log.debug("Validating blob %s" % self)
        validator = jsonschema.Draft4Validator(self.getSchema(), format_checker=jsonschema.Draft4Validator.FORMAT_CHECKER)
        # Normal usage is to use .validate(), but errors raised by it return
        # a massive error message that includes the entire blob, which is way
        # too big to be useful in the UI. Instead, we iterate over the
        # individual errors (which are all single sentences which contain
        # the name of the failing property and why it failed), and return those.
        errors = [e.message for e in validator.iter_errors(self)]
        if errors:
            raise BlobValidationError("Invalid blob! See 'errors' for details.", errors)

        if self.containsForbiddenDomain(product, allowlistedDomains):
            raise ValueError("Blob contains forbidden domain(s)")

    def getSchema(self):
        def loadSchema():
            return yaml.safe_load(open(path.join(path.dirname(path.abspath(__file__)), "schemas", self.jsonschema)))

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

    def containsForbiddenDomain(self, product, allowlistedDomains):
        raise NotImplementedError()

    def getReferencedReleases(self):
        """
        :return: Returns set of names of partially referenced releases that the current
                 release references
        """
        return set()


# We should be able to kill this Blob and its subclasses at some point by using
# GenericBlob, and fully encapsulating the response in getResponse
# getResponseProducts/getResponseBlobs may have to move elsewhere, though.
class XMLBlob(Blob):
    def getResponseProducts(self):
        """
        :return: Usually returns None. If the Blob is a SuperBlob, it returns the list
                of return products.
        """
        return None

    def getResponseBlobs(self):
        """
        :return: Usually returns None. It the Blob is a systemaddons superblob, it returns the
                 list of return blobs
        """
        return None

    def getInnerHeaderXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        """
        :return: Releases-specific header should be implemented for individual blobs
        """
        raise NotImplementedError()

    def getInnerFooterXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        """
        :return: Releases-specific header should be implemented for individual blobs
        """
        raise NotImplementedError()

    def getInnerXML(self, updateQuery, update_type, allowlistedDomains, specialForceHosts):
        raise NotImplementedError()

    def getHeaderXML(self):
        """
        :return: Returns the outer most header. Returns the outer most header
        """
        header = ['<?xml version="1.0"?>']
        header.append("<updates>")
        return header

    def getFooterXML(self):
        """
        :return: Returns the outer most footer. Returns the outer most header
        """
        footer = "</updates>"
        return footer


class GenericBlob(Blob):
    def getResponse(self):
        raise NotImplementedError
