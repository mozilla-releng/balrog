from auslib.blobs.base import Blob


class SuperBlob(Blob):
    jsonschema = "superblob.yml"

    def __init__(self, **kwargs):
        Blob.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 1000

    def getResponseProducts(self):
        return self["products"]

    def shouldServeUpdate(self, updateQuery):
        # Since a superblob update will always be returned.
        return True
