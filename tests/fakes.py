import json

from auslib.db import GCSHistory, GCSHistoryAsync


def FakeBlobFactory(exc=None):
    class fb:
        def __init__(self, data=None):
            self.data = data

        async def upload(self, body, *args, **kwargs):
            if exc:
                raise exc("I failed to upload")
            else:
                self.data = body

    return fb


FakeBlob = FakeBlobFactory()


class FakeBucket:
    def __init__(self):
        self.blobs = {}

    def new_blob(self, blob_name, *args, **kwargs):
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


class FakeGCSHistoryAsync(GCSHistoryAsync):
    def __init__(self, *args, identifier_columns=["name"], **kwargs):
        self.bucket = FakeBucket()
        self.identifier_columns = identifier_columns
        self.data_column = "data"

    def _getBucket(self, identifier):
        return lambda session: self.bucket
