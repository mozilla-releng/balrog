from collections import defaultdict


class FakeGCSHistory:
    def __init__(self, *args, **kwargs):
        self.data = defaultdict(dict)

    def forInsert(self, insertedKeys, columns, changed_by, transaction):
        name = "{}-{}".format(columns.get("name"), columns.get("data_version"))
        self.data[columns.get("name")][name] = columns.get("data")

    def forDelete(self, rowData, changed_by, transaction):
        name = "{}-{}".format(rowData.get("name"), rowData.get("data_version"))
        self.data[rowData.get("name")][name] = ""

    def forUpdate(self, rowData, changed_by, transaction):
        name = "{}-{}".format(rowData.get("name"), rowData.get("data_version"))
        self.data[rowData.get("name")][name] = rowData.get("data")

    def getChange(self, change_id=None, column_values=None, data_version=None, transaction=None):
        name = "{}-{}".format(column_values["name"], data_version)
        return {"name": column_values["name"], "data_version": data_version, "data": self.data[column_values["name"]][name]}
