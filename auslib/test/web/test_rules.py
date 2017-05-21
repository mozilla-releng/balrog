# import json
# import unittest
# from auslib.web.public.base import app
# from auslib.global_state import dbo


# class TestPublicRulesAPI(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Error handlers are removed in order to give us better debug messages
#         cls.error_spec = app.error_handler_spec
#         # Ripped from https://github.com/mitsuhiko/flask/blob/1f5927eee2288b4aaf508af5dc1f148aa2140d91/flask/app.py#L394
#         app.error_handler_spec = {None: {}}

#     @classmethod
#     def tearDownClass(cls):
#         app.error_handler_spec = cls.error_spec

#     def setUp(self):
#         dbo.setDb('sqlite:///:memory:')
#         dbo.create()
#         self.client = app.test_client()

#     def testGetRules(self):
#         ret = self.client.get("/rules")
#         got = json.loads(ret.data)
#         self.assertEquals(got["count"], 6)
