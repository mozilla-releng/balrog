import json

from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest


# TODO: needs scheduled changes tests too
class TestProductRequiredSignoffs(ViewTest):

    def testGetRequiredSignoffs(self):
        ret = self._get("/required_signoffs/product")
        got = json.loads(ret.data)
        self.assertEquals(got["count"], 1)
        self.assertEquals(got["required_signoffs"], [{"product": "fake", "channel": "a", "role": "releng", "signoffs_required": 1, "data_version": 1}])

    def testAddRequiredSignoff(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="b", role="releng", signoffs_required=1))
        self.assertStatusCode(ret, 201)
        rs = dbo.productRequiredSignoffs.t.select().where(dbo.productRequiredSignoffs.product == "fake")\
                                                   .where(dbo.productRequiredSignoffs.channel == "b")\
                                                   .where(dbo.productRequiredSignoffs.role == "releng")\
                                                   .execute().fetchall()
        self.assertEquals(len(rs), 1)
        self.assertEquals(rs[0]["signoffs_required"], 1)
        self.assertEquals(rs[0]["data_version"], 1)

    def testAddRequiredSignoffWithoutEnoughUsersInRole(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="b", role="releng", signoffs_required=3))
        self.assertStatusCode(ret, 400)
        self.assertIn("Cannot require 3 signoffs", ret.data)

    def testAddRequiredSignoffThatRequiresSignoff(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="a", role="relman", signoffs_required=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("This change requires signoff", ret.data)

    def testAddRequiredSignoffWithoutPermission(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="b", role="releng", signoffs_required=1), username="janet")
        self.assertStatusCode(ret, 403)

    def testModifyRequiredSignoff(self):
        ret = self._post("/required_signoffs/product", data=dict(product="fake", channel="a", role="relman", signoffs_required=1, data_version=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("This change requires signoff", ret.data)

    def testDeleteRequiredSignoff(self):
        ret = self._delete("/required_signoffs/product", qs=dict(product="fake", channel="a", role="relman", data_version=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("This change requires signoff", ret.data)


class TestPermissionsRequiredSignoffs(ViewTest):
    pass
