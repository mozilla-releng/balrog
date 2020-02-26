import json

from auslib.db import GCSHistory


class FakeBlob:
    def __init__(self, data=None):
        self.data = data

    def upload_from_string(self, body, *args, **kwargs):
        self.data = body


class FakeBucket:
    def __init__(self):
        self.blobs = {}

    def blob(self, blob_name, *args, **kwargs):
        self.blobs[blob_name] = FakeBlob()
        return self.blobs[blob_name]


class FakeGCSHistory(GCSHistory):
    def __init__(self, *args, identifier_columns=["name"], **kwargs):
        self.bucket = FakeBucket()
        self.identifier_columns = identifier_columns
        self.data_column = "data"

    def _getBucket(self, identifier):
        return self.bucket

    def getChange(self, change_id=None, column_values=None, data_version=None, transaction=None):
        name = column_values["name"]
        prefix = f"{name}/{data_version}-"
        data = None
        for bname, blob in self.bucket.blobs.items():
            if bname.startswith(prefix):
                data = blob.data
                break
        return {"name": column_values["name"], "data_version": data_version, "data": json.loads(data)}
