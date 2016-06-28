from auslib.blobs.gmp import GMPBlobV1


class SystemAddonsBlob(GMPBlobV1):
    jsonschema = "systemaddons.yml"

    def __init__(self, **kwargs):
        GMPBlobV1.__init__(self, **kwargs)
        if "schema_version" not in self:
            self["schema_version"] = 5000

    def hasHeaderIfInnerXMLIsEmpty(self):
        return self["uninstall"]
