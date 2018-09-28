import mock
import simplejson as json

from sqlalchemy import select

from auslib.blobs.base import createBlob
from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest


class TestReleasesAPI_JSON(ViewTest):

    def testGetRelease(self):
        ret = self._get("/releases/b")
        self.assertStatusCode(ret, 200)
        self.assertIn('X-CSRF-Token', ret.headers)
        self.assertEqual(ret.get_json(), json.loads("""
{
    "name": "b",
    "hashFunction": "sha512",
    "schema_version": 1
}
"""))

    def testGetRelease404(self):
        ret = self._get("/releases/g")
        self.assertStatusCode(ret, 404)

    def testReleasePostUpdateExisting(self):
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
        ret = self._post('/releases/d', data=dict(data=data, product='d', data_version=1))
        self.assertStatusCode(ret, 200)
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'd').execute().fetchone()[0]
        self.assertEqual(ret, createBlob("""
{
    "name": "d",
    "schema_version": 1,
    "detailsUrl": "blah",
    "fakePartials": true,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "d": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
"""))

    def testReleasePostUpdateExistingWithoutPermission(self):
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
        ret = self._post('/releases/d', data=dict(data=data, product='d', data_version=1), username="hannah")
        self.assertStatusCode(ret, 403)

    def testReleasePutUpdateMergeableOutdatedData(self):
        ancestor_blob = """
        {
            "name": "dd",
            "schema_version": 1,
            "detailsUrl": "blah",
            "fakePartials": true,
            "hashFunction": "sha512",
            "platforms": {
                "p": {
                    "locales": {
                        "dd": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        }
                    }
                }
            }
        }"""
        blob1 = """
        {
            "name": "dd",
            "schema_version": 1,
            "detailsUrl": "blah",
            "fakePartials": true,
            "hashFunction": "sha512",
            "platforms": {
                "p": {
                    "locales": {
                        "dd": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        },
                        "dd2": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        }
                     }
                }
            }
        }"""
        blob2 = """
        {
            "name": "dd",
            "schema_version": 1,
            "detailsUrl": "blah",
            "fakePartials": true,
            "hashFunction": "sha512",
            "platforms": {
                "p": {
                    "locales": {
                        "dd": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        },
                        "dd1": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        }
                    }
                }
            }
        }"""
        result_blob = createBlob("""
        {
            "name": "dd",
            "schema_version": 1,
            "detailsUrl": "blah",
            "fakePartials": true,
            "hashFunction": "sha512",
            "platforms": {
                "p": {
                    "locales": {
                        "dd2": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        },
                        "dd": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        },
                        "dd1": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        }
                    }
                }
            }
        }""")

        # Testing Put request to add new release
        ret = self._put('/releases/dd', data=dict(blob=ancestor_blob, name='dd',
                                                  product='dd', data_version=1))
        self.assertStatusCode(ret, 201)
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'dd').execute().fetchone()[0]
        self.assertEqual(ret, createBlob(ancestor_blob))

        # Updating same release
        ret = self._put('/releases/dd', data=dict(blob=blob1, name='dd',
                                                  product='dd', data_version=1))
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.get_json(), dict(new_data_version=2))

        # Updating release with outdated data, testing if merged correctly
        ret = self._put('/releases/dd', data=dict(blob=blob2, name='dd',
                                                  product='dd', data_version=1))
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.get_json(), dict(new_data_version=3))

        ret = select([dbo.releases.data]).where(dbo.releases.name == 'dd').execute().fetchone()[0]
        self.assertEqual(ret, result_blob)

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "dd").execute().fetchall()
        self.assertEqual(len(history_rows), 4)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], json.loads(ancestor_blob))
        self.assertEqual(history_rows[2]["data"], json.loads(blob1))
        self.assertEqual(history_rows[3]["data"], result_blob)

    def testReleasePutUpdateConflictingOutdatedData(self):
        ancestor_blob = """
        {
            "name": "dd",
            "schema_version": 1,
            "detailsUrl": "blah",
            "fakePartials": true,
            "hashFunction": "sha512",
            "platforms": {
                "p": {
                    "locales": {
                        "dd": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        }
                    }
                }
            }
        }"""
        blob1 = """
        {
            "name": "dd",
            "schema_version": 1,
            "detailsUrl": "blah",
            "fakePartials": true,
            "hashFunction": "sha512",
            "platforms": {
                "p": {
                    "locales": {
                        "dd1": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        }
                    }
                }
            }
        }"""
        blob2 = """
        {
            "name": "dd",
            "schema_version": 1,
            "detailsUrl": "blah",
            "fakePartials": true,
            "hashFunction": "sha512",
            "platforms": {
                "p": {
                    "locales": {
                        "dd": {
                            "complete": {
                                "filesize": 12345,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        },
                        "dd1": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc1"
                            }
                        }
                    }
                }
            }
        }"""
        # Testing Put request to add new release
        ret = self._put('/releases/dd', data=dict(blob=ancestor_blob, name='dd', product='dd', data_version=1))
        self.assertStatusCode(ret, 201)

        ret = select([dbo.releases.data]).where(dbo.releases.name == 'dd').execute().fetchone()[0]
        self.assertEqual(ret, createBlob(ancestor_blob))

        # Updating same release
        ret = self._put('/releases/dd', data=dict(blob=blob1, name='dd',
                                                  product='dd', data_version=1))
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.get_json(), dict(new_data_version=2))

        # Updating same release with conflicting data
        ret = self._put('/releases/dd', data=dict(blob=blob2, name='dd',
                                                  product='dd', data_version=1))
        self.assertStatusCode(ret, 400)

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "dd").execute().fetchall()
        self.assertEqual(len(history_rows), 3)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], json.loads(ancestor_blob))
        self.assertEqual(history_rows[2]["data"], json.loads(blob1))

    def testReleasePostUpdateOutdatedDataNotBlob(self):
        blob = """
        {
            "name": "ee",
            "schema_version": 1,
            "detailsUrl": "blah",
            "fakePartials": true,
            "hashFunction": "sha512",
            "platforms": {
                "p": {
                    "locales": {
                        "ee": {
                            "complete": {
                                "filesize": 1234,
                                "from": "*",
                                "hashValue": "abc"
                            }
                        }
                    }
                }
            }
        }"""
        ret = self._post('/releases/ee', data=dict(data=blob, hashFunction="sha512", name='ee', product='ee'))
        self.assertStatusCode(ret, 201)

        # Updating same release
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=2)), "Data: %s" % ret.get_data())
        ret = self._post('/releases/ee', data=dict(data=blob,
                                                   hashFunction="sha512",
                                                   name='ee', product='ee', data_version=2))
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=3)), "Data: %s" % ret.get_data())

        # Outdated Data Error on same release
        ret = self._post('/releases/ee', data=dict(hashFunction="sha512",
                                                   read_only=True,
                                                   name='ee', product='ee', data_version=1))
        self.assertStatusCode(ret, 400)

        blob = json.loads(blob)
        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "ee").execute().fetchall()
        self.assertEqual(len(history_rows), 4)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[0]["data_version"], None)
        self.assertEqual(history_rows[0]["read_only"], False)
        self.assertEqual(history_rows[1]["data"], {"name": "ee", "schema_version": 1, "hashFunction": "sha512"})
        self.assertEqual(history_rows[1]["data_version"], 1)
        self.assertEqual(history_rows[1]["read_only"], False)
        self.assertEqual(history_rows[2]["data"], blob)
        self.assertEqual(history_rows[2]["data_version"], 2)
        self.assertEqual(history_rows[2]["read_only"], False)
        self.assertEqual(history_rows[3]["data"], blob)
        self.assertEqual(history_rows[3]["data_version"], 3)
        self.assertEqual(history_rows[3]["read_only"], False)

    def testReleasePostMismatchedName(self):
        data = json.dumps(dict(name="eee", schema_version=1))
        ret = self._post('/releases/d', data=dict(data=data, product='d', data_version=1))
        self.assertStatusCode(ret, 400)

    def testReleasePostUpdateChangeHashFunction(self):
        data = json.dumps(dict(detailsUrl='blah', hashFunction="sha1024", schema_version=1))
        ret = self._post('/releases/d', data=dict(data=data, product='d', data_version=1))
        self.assertStatusCode(ret, 400)

    def testReleasePostUpdateChangeProduct(self):
        data = json.dumps(dict(detailsUrl="abc", schema_version=1))
        ret = self._post("/releases/c", data=dict(data=data, product="h", data_version=1))
        self.assertStatusCode(ret, 400)

    def testReleasePostInvalidBlob(self):
        data = json.dumps(dict(uehont="uhetn", schema_version=1))
        ret = self._post("/releases/c", data=dict(data=data, product="c", data_version=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("Additional properties are not allowed", ret.get_data(as_text=True))

    def testReleasePostWithSignoffRequired(self):
        data = json.dumps(dict(bouncerProducts=dict(partial='foo'), name='a', hashFunction="sha512"))
        ret = self._post("/releases/a", data=dict(data=data, product="a", data_version=1, schema_version=1))
        self.assertStatusCode(ret, 400)
        self.assertIn("This change requires signoff", ret.get_data(as_text=True))

    def testReleasePostCreatesNewReleasev1(self):
        data = json.dumps(dict(bouncerProducts=dict(partial='foo'), name='e', hashFunction="sha512"))
        ret = self._post('/releases/e', data=dict(data=data, product='e', schema_version=1))
        self.assertStatusCode(ret, 201)
        ret = dbo.releases.t.select().where(dbo.releases.name == 'e').execute().fetchone()
        self.assertEqual(ret['product'], 'e')
        self.assertEqual(ret['name'], 'e')
        self.assertEqual(ret['data'], createBlob("""
{
    "name": "e",
    "hashFunction": "sha512",
    "schema_version": 1,
    "bouncerProducts": {
        "partial": "foo"
    }
}
"""))

    def testReleasePostCreatesNewReleaseNoAuthentication(self):
        data = json.dumps(dict(bouncerProducts=dict(partial='foo'), name='e', hashFunction="sha512"))
        ret = self._post('/releases/e', data=dict(data=data, product='e', schema_version=1), username=None)
        self.assertStatusCode(ret, 401)

    def testReleasePostCreatesNewReleaseNoPermission(self):
        data = json.dumps(dict(bouncerProducts=dict(partial='foo'), name='e', hashFunction="sha512"))
        ret = self._post('/releases/e', data=dict(data=data, product='e', schema_version=1), username="mary")
        self.assertStatusCode(ret, 403)

    def testReleasePostCreatesNewReleasev2(self):
        data = json.dumps(dict(bouncerProducts=dict(complete='foo'), name='e', hashFunction="sha512"))
        ret = self._post('/releases/e', data=dict(data=data, product='e', schema_version=2))
        self.assertStatusCode(ret, 201)
        ret = dbo.releases.t.select().where(dbo.releases.name == 'e').execute().fetchone()
        self.assertEqual(ret['product'], 'e')
        self.assertEqual(ret['name'], 'e')
        self.assertEqual(ret['data'], createBlob("""
{
    "name": "e",
    "hashFunction": "sha512",
    "schema_version": 2,
    "bouncerProducts": {
        "complete": "foo"
    }
}
"""))

    def testReleasePostInvalidKey(self):
        data = json.dumps(dict(foo=1))
        ret = self._post('/releases/ab', data=dict(data=data))
        self.assertStatusCode(ret, 400)

    def testReleasePostRejectedURL(self):
        data = json.dumps(dict(platforms=dict(p=dict(locales=dict(f=dict(complete=dict(fileUrl='http://evil.com')))))))
        ret = self._post('/releases/d', data=dict(data=data, product='d', data_version=1))
        self.assertStatusCode(ret, 400)

    def testDeleteRelease(self):
        ret = self._delete("/releases/d", qs=dict(data_version=1))
        self.assertStatusCode(ret, 200)
        ret = dbo.releases.count(where=[dbo.releases.name == 'd'])
        self.assertEqual(ret, 0)

    def testDeleteReleaseOutdatedData(self):
        # Release's data version is outdated
        ret = self._get("/releases/d")
        self.assertStatusCode(ret, 200)
        ret = self._delete("/releases/d", qs=dict(data_version=7))
        self.assertStatusCode(ret, 400)

    def testDeleteNonExistentRelease(self):
        ret = self._delete("/releases/ueo", qs=dict(data_version=1))
        self.assertStatusCode(ret, 404)

    def testDeleteWithoutPermission(self):
        ret = self._delete("/releases/d", username="bob", qs=dict(data_version=1))
        self.assertStatusCode(ret, 403)

    def testDeleteWithoutPermissionForAction(self):
        ret = self._delete("/releases/d", username="bob", qs=dict(data_version=1))
        self.assertStatusCode(ret, 403)

    def testDeleteWithProductAdminPermission(self):
        ret = self._delete("/releases/d", username="bill", qs=dict(data_version=1))
        self.assertStatusCode(ret, 200)

    def testDeleteWithoutProductAdminPermission(self):
        ret = self._delete("/releases/d", username="billy", qs=dict(data_version=1))
        self.assertStatusCode(ret, 403)

    def testDeleteReadOnlyRelease(self):
        dbo.releases.t.update(values=dict(read_only=True, data_version=2)).where(dbo.releases.name == "d").execute()
        ret = self._delete("/releases/d", username="bill", qs=dict(data_version=2))
        self.assertStatusCode(ret, 403)

    def testDeleteWithRules(self):
        ret = self._delete("/releases/a", qs=dict(data_version=1))
        self.assertStatusCode(ret, 400)

    def testLocalePut(self):
        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "abc",
            }
        })
        ret = self._put('/releases/ab/builds/p/l', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=2)), "Data: %s" % ret.get_data())
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'ab').execute().fetchone()[0]
        expected = createBlob("""
{
    "name": "ab",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 435,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(ret, expected)

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "ab").execute().fetchall()
        self.assertEqual(len(history_rows), 3)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], {"name": "ab", "schema_version": 1, "hashFunction": "sha512"})
        self.assertEqual(history_rows[2]["data"], expected)

    def testLocalePutOutdatedDataError(self):
        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "abc",
            }
        })
        ret = self._put('/releases/ab/builds/p/l', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 201)

        expected = {
            "name": "ab", "schema_version": 1, "hashFunction": "sha512",
            "platforms": {
                "p": {
                    "locales": {
                        "l": {
                            "complete": {
                                "filesize": 435, "from": "*", "hashValue": "abc"
                            }
                        }
                    }
                }
            }
        }

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "ab").execute().fetchall()
        self.assertEqual(len(history_rows), 3)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], {"name": "ab", "schema_version": 1, "hashFunction": "sha512"})
        self.assertEqual(history_rows[2]["data"], expected)

        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "def",
            }
        })
        ret = self._put('/releases/ab/builds/p/l', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 400)

        # Ensure that history wasn't created for second request.
        # See https://bugzilla.mozilla.org/show_bug.cgi?id=1246993 for background.
        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "ab").execute().fetchall()
        self.assertEqual(len(history_rows), 3)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], {"name": "ab", "schema_version": 1, "hashFunction": "sha512"})
        self.assertEqual(history_rows[2]["data"], expected)

    def testLocalePutSpecificPermission(self):
        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "abc",
            }
        })
        ret = self._put('/releases/ab/builds/p/l', username="ashanti", data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=2)), "Data: %s" % ret.get_data())
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'ab').execute().fetchone()[0]
        expected = createBlob("""
{
    "name": "ab",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "complete": {
                        "filesize": 435,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(ret, expected)

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "ab").execute().fetchall()
        self.assertEqual(len(history_rows), 3)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], {"name": "ab", "schema_version": 1, "hashFunction": "sha512"})
        self.assertEqual(history_rows[2]["data"], expected)

    def testLocalePutWithBadHashFunction(self):
        data = json.dumps(dict(complete=dict(filesize='435')))
        ret = self._put('/releases/ab/builds/p/l', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 400)

    def testLocalePutWithoutAuthentication(self):
        data = '{"complete": {"filesize": 435, "from": "*", "hashValue": "abc"}}'
        ret = self._put('/releases/ab/builds/p/l', username=None, data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 401)

    def testLocalePutWithoutPermission(self):
        data = '{"complete": {"filesize": 435, "from": "*", "hashValue": "abc"}}'
        ret = self._put('/releases/ab/builds/p/l', username='liu', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 403)

    def testLocalePutWithoutPermissionForProduct(self):
        data = '{"complete": {"filesize": 435, "from": "*", "hashValue": "abc"}}'
        ret = self._put('/releases/ab/builds/p/l', username='bob', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 403)

    def testLocalePutForNewRelease(self):
        data = json.dumps({
            "complete": {
                "filesize": 678,
                "from": "*",
                "hashValue": "abc",
            }
        })
        # setting schema_version in the incoming blob is a hack for testing
        # SingleLocaleView._put() doesn't give us access to the form
        ret = self._put('/releases/e/builds/p/a', data=dict(data=data, product='e', hashFunction="sha512", schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=2)), "Data: %s" % ret.get_data())
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'e').execute().fetchone()[0]
        expected = createBlob("""
{
    "name": "e",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "a": {
                    "complete": {
                        "filesize": 678,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(ret, expected)

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "e").execute().fetchall()
        self.assertEqual(len(history_rows), 3)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], {"name": "e", "schema_version": 1, "hashFunction": "sha512"})
        self.assertEqual(history_rows[2]["data"], expected)

    def testLocalePutAppend(self):
        data = json.dumps({
            "partial": {
                "filesize": 234,
                "from": "c",
                "hashValue": "abc",
                "fileUrl": "http://good.com/blah",
            }
        })
        ret = self._put('/releases/d/builds/p/g', data=dict(data=data, product='d', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=2)), "Data: %s" % ret.get_data())
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'd').execute().fetchone()[0]
        expected = createBlob("""
{
    "name": "d",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "d": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "abc"
                    }
                },
                "g": {
                    "partial": {
                        "filesize": 234,
                        "from": "c",
                        "hashValue": "abc",
                        "fileUrl": "http://good.com/blah"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(ret, expected)

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "d").execute().fetchall()
        interim_blob = createBlob("""
{
    "name": "d",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "d": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(len(history_rows), 3)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], interim_blob)
        self.assertEqual(history_rows[2]["data"], expected)

    def testLocalePutForNewReleaseWithAlias(self):
        data = json.dumps({
            "complete": {
                "filesize": 678,
                "from": "*",
                "hashValue": "abc",
            }
        })
        # setting schema_version in the incoming blob is a hack for testing
        # SingleLocaleView._put() doesn't give us access to the form
        ret = self._put('/releases/e/builds/p/a', data=dict(data=data, product='e', alias='["p2"]', schema_version=1, hashFunction="sha512"))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=2)), "Data: %s" % ret.get_data())
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'e').execute().fetchone()[0]
        expected = createBlob("""
{
    "name": "e",
    "hashFunction": "sha512",
    "schema_version": 1,
    "platforms": {
        "p": {
            "locales": {
                "a": {
                    "complete": {
                        "filesize": 678,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        },
        "p2": {
            "alias": "p"
        }
    }
}
""")
        self.assertEqual(ret, expected)

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "e").execute().fetchall()
        self.assertEqual(len(history_rows), 3)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], {"name": "e", "schema_version": 1, "hashFunction": "sha512"})
        self.assertEqual(history_rows[2]["data"], expected)

    def testLocalePutAppendWithAlias(self):
        data = json.dumps({
            "partial": {
                "filesize": 123,
                "from": "c",
                "hashValue": "abc",
                "fileUrl": "http://good.com/blah",
            }
        })
        ret = self._put('/releases/d/builds/q/g', data=dict(data=data, product='d', data_version=1, alias='["q2"]', schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=2)), "Data: %s" % ret.get_data())
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'd').execute().fetchone()[0]
        expected = createBlob("""
{
    "name": "d",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "d": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        },
        "q": {
            "locales": {
                "g": {
                    "partial": {
                        "filesize": 123,
                        "from": "c",
                        "hashValue": "abc",
                        "fileUrl": "http://good.com/blah"
                    }
                }
            }
        },
        "q2": {
            "alias": "q"
        }
    }
}
""")
        self.assertEqual(ret, expected)

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "d").execute().fetchall()
        interim_blob = createBlob("""
{
    "name": "d",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "d": {
                    "complete": {
                        "filesize": 1234,
                        "from": "*",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(len(history_rows), 3)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], interim_blob)
        self.assertEqual(history_rows[2]["data"], expected)

    def testLocalePutWithCopy(self):
        data = json.dumps({
            "partial": {
                "filesize": 123,
                "from": "b",
                "hashValue": "abc",
            }
        })
        data = dict(data=data, product='a', copyTo=json.dumps(['b']), data_version=1, schema_version=1)
        ret = self._put('/releases/ab/builds/p/l', data=data)
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.get_data(as_text=True), json.dumps(dict(new_data_version=2)), "Data: %s" % ret.get_data())
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'ab').execute().fetchone()[0]
        expected = createBlob("""
{
    "name": "ab",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "partial": {
                        "filesize": 123,
                        "from": "b",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(ret, expected)

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "ab").execute().fetchall()
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], {"name": "ab", "schema_version": 1, "hashFunction": "sha512"})
        self.assertEqual(history_rows[2]["data"], expected)

        ret = select([dbo.releases.data]).where(dbo.releases.name == 'b').execute().fetchone()[0]
        expected = createBlob("""
{
    "name": "b",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "partial": {
                        "filesize": 123,
                        "from": "b",
                        "hashValue": "abc"
                    }
                }
            }
        }
    }
}
""")
        self.assertEqual(ret, expected)

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "b").execute().fetchall()
        self.assertEqual(len(history_rows), 3)
        self.assertEqual(history_rows[0]["data"], None)
        self.assertEqual(history_rows[1]["data"], {"name": "b", "schema_version": 1, "hashFunction": "sha512"})
        self.assertEqual(history_rows[2]["data"], expected)

    def testLocalePutBadJSON(self):
        ret = self._put('/releases/ab/builds/p/l', data=dict(data='a', product='a'))
        self.assertStatusCode(ret, 400)

    def testLocaleRejectedURL(self):
        data = json.dumps(dict(complete=dict(fileUrl='http://evil.com')))
        ret = self._put('/releases/ab/builds/p/l', data=dict(data=data, product='a', data_version=1))
        self.assertStatusCode(ret, 400)

    def testLocaleGet(self):
        ret = self._get('/releases/d/builds/p/d')
        self.assertStatusCode(ret, 200)
        got = ret.get_json()
        expected = {
            "complete": {
                "filesize": 1234,
                "from": "*",
                "hashValue": "abc",
            }
        }
        self.assertEqual(got, expected)
        self.assertEqual(ret.headers['X-Data-Version'], '1')

    def testLocalePutNotAllowed(self):
        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "abc",
            }
        })
        inp_data = dict(csrf_token="lorem", data=data, product='d', data_version=1, schema_version=1)
        ret = self.client.put('/releases/d/builds/p/d', data=json.dumps(inp_data), content_type="application/json")
        self.assertStatusCode(ret, 401)

    def testLocalePutReadOnlyRelease(self):
        dbo.releases.t.update(values=dict(read_only=True, data_version=2)).where(dbo.releases.name == "ab").execute()
        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "abc",
            }
        })
        ret = self._put('/releases/ab/builds/p/l', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 403)

    def testLocalePutWithProductAdmin(self):
        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "abc",
            }
        })
        ret = self._put('/releases/ab/builds/p/l', username='billy',
                        data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 201)

    def testLocalePutWithoutProductAdmin(self):
        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "abc",
            }
        })
        ret = self._put('/releases/d/builds/p/d', username='billy',
                        data=dict(data=data, product='d', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 403)

    def testLocalePutCantChangeProduct(self):
        data = json.dumps(dict(complete=dict(filesize=435)))
        ret = self._put('/releases/ab/builds/p/l', data=dict(data=data, product='b', schema_version=1))
        self.assertStatusCode(ret, 400)

    def testLocaleGet404(self):
        ret = self._get("/releases/c/builds/h/u")
        self.assertStatusCode(ret, 404)

    # FIXME: We shouldn't rely on 500 to validate behaviour. This test should fake a 400 instead.
    # Currently, causing a 400 in this will NOT make version revert to the original value. Need to
    # fix the bug at the same time as changing the test.
#    def testLocaleRevertsPartialUpdate(self):
#        data = json.dumps(dict(complete=dict(filesize=1)))
#        with mock.patch('auslib.global_state.dbo.releases.addLocaleToRelease') as r:
#            r.side_effect = Exception("Fail")
#            ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', version='c', data_version=1, schema_version=1))
#            self.assertStatusCode(ret, 500)
#            ret = dbo.releases.t.select().where(dbo.releases.name == 'a').execute().fetchone()
#            self.assertEqual(ret['product'], 'a')
#            self.assertEqual(ret['version'], 'a')
#            self.assertEqual(json.loads(ret['data']), dict(name='a', hashFunction="sha512", schema_version=1))

    def testNewReleasePut(self):
        ret = self._put('/releases/new_release', data=dict(name='new_release', product='Firefox',
                                                           blob="""
{
    "name": "new_release",
    "hashFunction": "sha512",
    "schema_version": 1,
    "platforms": {
        "p": {
            "locales": {
                "l": {
                }
            }
        }
    }
}
"""))

        self.assertEqual(ret.status_code, 201, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        r = dbo.releases.t.select().where(dbo.releases.name == 'new_release').execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]['name'], 'new_release')
        self.assertEqual(r[0]['product'], 'Firefox')
        self.assertEqual(r[0]['data'], createBlob("""
{
    "name": "new_release",
    "hashFunction": "sha512",
    "schema_version": 1,
    "platforms": {
        "p": {
            "locales": {
                "l": {
                }
            }
        }
    }
}
"""))

    def testNewReleasePutBadInput(self):
        ret = self._put("/releases/ueohueo", data=dict(name="ueohueo", product="aa", blob="""
{
    "name": "ueohueo",
    "schema_version": 3,
    "hashFunction": "sha512",
    "borken": "yes"
}
"""))
        self.assertStatusCode(ret, 400)

    def testNewAppReleaseV9BadVersion(self):
        ret = self._put("/releases/bad", data=dict(name="ueohueo", product="aa", blob="""
{
    "name": "bad",
    "schema_version": 9,
    "hashFunction": "sha512",
    "appVersion": "31.0.2",
    "displayVersion": "31.0.2",
    "updateLine": [
        {
            "for": {
                "versions": ["<49"]
            },
            "fields": {
                "detailsURL": "http://example.org/details/%LOCALE%",
                "type": "minor"
            }
        }
    ]
}
"""))
        self.assertStatusCode(ret, 400)

    def testNewReleasePutMismatchedName(self):
        ret = self._put("/releases/aaaa", data=dict(name="ueohueo", product="aa", blob="""
{
    "name": "bbbb",
    "schema_version": 3
}
"""))
        self.assertStatusCode(ret, 400)

    def testPutExistingRelease(self):
        ret = self._put("/releases/d", data=dict(name="d", product="Firefox", data_version=1, blob="""
{
    "name": "d",
    "schema_version": 3,
    "hashFunction": "sha512",
    "actions": "doit"
}
"""))
        self.assertEqual(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        r = dbo.releases.t.select().where(dbo.releases.name == 'd').execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]['name'], 'd')
        self.assertEqual(r[0]['product'], 'Firefox')
        self.assertEqual(r[0]['data'], createBlob("""
{
    "name": "d",
    "schema_version": 3,
    "hashFunction": "sha512",
    "actions": "doit"
}
"""))

    def testGMPReleasePut(self):

        ret = self._put('/releases/gmprel', data=dict(name='gmprel', product='a',
                                                      blob="""
{
    "name": "gmprel",
    "schema_version": 1000,
    "hashFunction": "sha512",
    "vendors": {
        "foo": {
            "version": "1",
            "platforms": {
                "a": {
                    "filesize": 2,
                    "hashValue": "acbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbda\
cbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbd",
                    "fileUrl": "http://good.com/4"
                },
                "a2": {
                    "alias": "a"
                }
            }
        }
    }
}
"""))

        self.assertEqual(ret.status_code, 201, "Status Code: %d, Data: %s" % (ret.status_code, ret.get_data()))
        r = dbo.releases.t.select().where(dbo.releases.name == 'gmprel').execute().fetchall()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]['name'], 'gmprel')
        self.assertEqual(r[0]['product'], 'a')
        self.assertEqual(r[0]['data'], createBlob("""
{
    "name": "gmprel",
    "schema_version": 1000,
    "hashFunction": "sha512",
    "vendors": {
        "foo": {
            "version": "1",
            "platforms": {
                "a": {
                    "filesize": 2,
                    "hashValue": "acbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbda\
cbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbdacbd",
                    "fileUrl": "http://good.com/4"
                },
                "a2": {
                    "alias": "a"
                }
            }
        }
    }
}
"""))

    def testGetReleases(self):
        ret = self._get("/releases")
        self.assertStatusCode(ret, 200)
        data = ret.get_json()
        self.assertEqual(len(data["releases"]), 5)

    def testGetReleasesNamesOnly(self):
        ret = self._get("/releases", qs=dict(names_only=1))
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.get_json(), json.loads("""
{
    "names": [
        "a", "ab", "b", "c", "d"
    ]
}
"""))

    def testGetReleasesNamePrefix(self):
        ret = self._get("/releases", qs=dict(name_prefix='a'))
        self.assertStatusCode(ret, 200)

        ret_data = ret.get_json()

        with self.assertRaises(KeyError):
            ret_data['data']

        self.assertEqual(ret_data, json.loads("""
{
    "releases": [
        {"data_version": 1, "name": "a", "product": "a", "read_only": false, "rule_ids": [3, 4, 6, 7, 8, 9], "required_signoffs": {"releng": 1}},
        {"data_version": 1, "name": "ab", "product": "a", "read_only": false, "rule_ids": [], "required_signoffs": {}}
    ]
}
"""))

    def testGetReleasesNamePrefixNamesOnly(self):
        ret = self._get("/releases", qs=dict(name_prefix='a',
                                             names_only='1'))
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.get_json(), json.loads("""
{
    "names": ["a", "ab"]
}
"""))

    def testReleasesPost(self):
        data = json.dumps(dict(bouncerProducts=dict(partial='foo'), name='e', schema_version=1, hashFunction="sha512"))
        ret = self._post('/releases', data=dict(blob=data, name="e", product='e'))
        self.assertStatusCode(ret, 201)
        ret = dbo.releases.t.select().where(dbo.releases.name == 'e').execute().fetchone()
        self.assertEqual(ret['product'], 'e')
        self.assertEqual(ret['name'], 'e')
        self.assertEqual(ret['data'], createBlob("""
{
    "name": "e",
    "hashFunction": "sha512",
    "schema_version": 1,
    "bouncerProducts": {
        "partial": "foo"
    }
}
"""))


class TestReleasesScheduledChanges(ViewTest):
    maxDiff = 10000

    def setUp(self):
        super(TestReleasesScheduledChanges, self).setUp()
        dbo.releases.scheduled_changes.t.insert().execute(
            sc_id=1, scheduled_by="bill", change_type="insert", data_version=1, base_name="m", base_product="m",
            base_data=createBlob(dict(name="m", hashFunction="sha512", schema_version=1))
        )
        dbo.releases.scheduled_changes.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=50, sc_id=1)
        dbo.releases.scheduled_changes.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=51, sc_id=1, scheduled_by="bill", change_type="insert", data_version=1, base_name="m",
            base_product="m", base_data=createBlob(dict(name="m", hashFunction="sha512", schema_version=1))
        )
        dbo.releases.scheduled_changes.conditions.t.insert().execute(sc_id=1, when=4000000000, data_version=1)
        dbo.releases.scheduled_changes.conditions.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=50, sc_id=1)
        dbo.releases.scheduled_changes.conditions.history.t.insert().execute(
            change_id=2, changed_by="bill", timestamp=51, sc_id=1, when=4000000000, data_version=1
        )

        dbo.releases.scheduled_changes.t.insert().execute(
            sc_id=2, scheduled_by="bill", change_type="update", data_version=1, base_name="a", base_product="a",
            base_data=createBlob(dict(name="a", hashFunction="sha512", schema_version=1, extv="2.0")), base_data_version=1
        )
        dbo.releases.scheduled_changes.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=70, sc_id=2)
        dbo.releases.scheduled_changes.history.t.insert().execute(
            change_id=4, changed_by="bill", timestamp=71, sc_id=2, scheduled_by="bill", change_type="update", data_version=1, base_name="a",
            base_product="a", base_data=createBlob(dict(name="a", hashFunction="sha512", schema_version=1, extv="2.0")), base_data_version=1
        )
        dbo.releases.scheduled_changes.signoffs.t.insert().execute(sc_id=2, username="bill", role="releng")
        dbo.releases.scheduled_changes.signoffs.history.t.insert().execute(change_id=1, changed_by="bill", timestamp=100, sc_id=2, username="bill")
        dbo.releases.scheduled_changes.signoffs.history.t.insert().execute(change_id=2, changed_by="bill", timestamp=101, sc_id=2,
                                                                           username="bill", role="releng")
        dbo.releases.scheduled_changes.conditions.t.insert().execute(sc_id=2, when=6000000000, data_version=1)
        dbo.releases.scheduled_changes.conditions.history.t.insert().execute(change_id=3, changed_by="bill", timestamp=70, sc_id=2)
        dbo.releases.scheduled_changes.conditions.history.t.insert().execute(
            change_id=4, changed_by="bill", timestamp=71, sc_id=2, when=6000000000, data_version=1
        )

        dbo.releases.scheduled_changes.t.insert().execute(
            sc_id=3, complete=True, scheduled_by="bill", change_type="update", data_version=2, base_name="b", base_product="b",
            base_data=createBlob(dict(name="b", hashFunction="sha512", schema_version=1)), base_data_version=1
        )
        dbo.releases.scheduled_changes.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=6, sc_id=3)
        dbo.releases.scheduled_changes.history.t.insert().execute(
            change_id=6, changed_by="bill", timestamp=7, sc_id=3, complete=False, scheduled_by="bill", change_type="update", data_version=1, base_name="b",
            base_product="b", base_data=createBlob(dict(name="b", hashFunction="sha512", schema_version=1)), base_data_version=1
        )
        dbo.releases.scheduled_changes.history.t.insert().execute(
            change_id=7, changed_by="bill", timestamp=25, sc_id=3, complete=True, change_type="update", scheduled_by="bill", data_version=2, base_name="b",
            base_product="b", base_data=createBlob(dict(name="b", hashFunction="sha512", schema_version=1)), base_data_version=1
        )
        dbo.releases.scheduled_changes.conditions.t.insert().execute(sc_id=3, when=10000000, data_version=2)
        dbo.releases.scheduled_changes.conditions.history.t.insert().execute(change_id=5, changed_by="bill", timestamp=6, sc_id=3)
        dbo.releases.scheduled_changes.conditions.history.t.insert().execute(
            change_id=6, changed_by="bill", timestamp=7, sc_id=3, when=10000000, data_version=1
        )
        dbo.releases.scheduled_changes.conditions.history.t.insert().execute(
            change_id=7, changed_by="bill", timestamp=25, sc_id=3, when=10000000, data_version=2
        )
        dbo.releases.scheduled_changes.t.insert().execute(
            sc_id=4, complete=False, scheduled_by="bill", change_type="delete", data_version=1, base_name="ab", base_data_version=1,
        )
        dbo.releases.scheduled_changes.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=25, sc_id=4)
        dbo.releases.scheduled_changes.history.t.insert().execute(
            change_id=9, changed_by="bill", timestamp=26, sc_id=4, complete=False, scheduled_by="bill", change_type="delete", data_version=1,
            base_name="ab", base_data_version=1
        )
        dbo.releases.scheduled_changes.conditions.t.insert().execute(sc_id=4, when=230000000, data_version=1)
        dbo.releases.scheduled_changes.conditions.history.t.insert().execute(change_id=8, changed_by="bill", timestamp=25, sc_id=4)
        dbo.releases.scheduled_changes.conditions.history.t.insert().execute(
            change_id=9, changed_by="bill", timestamp=26, sc_id=4, when=230000000, data_version=1
        )
        dbo.releases.scheduled_changes.signoffs.t.insert().execute(sc_id=4, username="bill", role="releng")
        dbo.releases.scheduled_changes.signoffs.t.insert().execute(sc_id=4, username="ben", role="releng")

    def testGetScheduledChanges(self):
        ret = self._get("/scheduled_changes/releases")
        expected = {
            "count": 3,
            "scheduled_changes": [
                {
                    "sc_id": 1, "when": 4000000000, "scheduled_by": "bill", "change_type": "insert", "complete": False, "sc_data_version": 1,
                    "name": "m", "product": "m", "data": {"name": "m", "hashFunction": "sha512", "schema_version": 1}, "read_only": False,
                    "data_version": None, "signoffs": {}, "required_signoffs": {},
                },
                {
                    "sc_id": 2, "when": 6000000000, "scheduled_by": "bill", "change_type": "update", "complete": False, "sc_data_version": 1,
                    "name": "a", "product": "a", "data": {"name": "a", "hashFunction": "sha512", "schema_version": 1, "extv": "2.0"},
                    "read_only": False, "data_version": 1, "signoffs": {"bill": "releng"}, "required_signoffs": {"releng": 1},
                    "original_row": dbo.releases.select({'name': 'a'})[0],
                },
                {
                    "sc_id": 4, "when": 230000000, "scheduled_by": "bill", "change_type": "delete", "complete": False, "sc_data_version": 1,
                    "name": "ab", "product": None, "data": None, "read_only": False, "data_version": 1, "signoffs": {"ben": "releng", "bill": "releng"},
                    "required_signoffs": {},
                    "original_row": dbo.releases.select({'name': 'ab'})[0],
                },
            ]
        }
        self.assertEqual(ret.get_json(), expected)

    def testGetScheduledChangesWithCompleted(self):
        ret = self._get("/scheduled_changes/releases", qs={"all": 1})
        expected = {
            "count": 4,
            "scheduled_changes": [
                {
                    "sc_id": 1, "when": 4000000000, "scheduled_by": "bill", "change_type": "insert", "complete": False, "sc_data_version": 1,
                    "name": "m", "product": "m", "data": {"name": "m", "hashFunction": "sha512", "schema_version": 1}, "read_only": False,
                    "data_version": None, "signoffs": {}, "required_signoffs": {},
                },
                {
                    "sc_id": 2, "when": 6000000000, "scheduled_by": "bill", "change_type": "update", "complete": False, "sc_data_version": 1,
                    "name": "a", "product": "a", "data": {"name": "a", "hashFunction": "sha512", "schema_version": 1, "extv": "2.0"},
                    "read_only": False, "data_version": 1, "signoffs": {"bill": "releng"}, "required_signoffs": {"releng": 1},
                    "original_row": dbo.releases.select({'name': 'a'})[0],
                },
                {
                    "sc_id": 3, "when": 10000000, "scheduled_by": "bill", "change_type": "update", "complete": True, "sc_data_version": 2,
                    "name": "b", "product": "b", "data": {"name": "b", "hashFunction": "sha512", "schema_version": 1}, "read_only": False,
                    "data_version": 1, "signoffs": {}, "required_signoffs": {},
                    # No original_row for complete changes.
                },
                {
                    "sc_id": 4, "when": 230000000, "scheduled_by": "bill", "change_type": "delete", "complete": False, "sc_data_version": 1,
                    "name": "ab", "product": None, "data": None, "read_only": False, "data_version": 1, "signoffs": {"ben": "releng", "bill": "releng"},
                    "required_signoffs": {},
                    "original_row": dbo.releases.select({'name': 'ab'})[0],
                },
            ]
        }
        self.assertEqual(ret.get_json(), expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeExistingRelease(self):
        data = {
            "when": 2300000000, "name": "d", "data": '{"name": "d", "hashFunction": "sha256", "schema_version": 1}',
            "product": "d", "data_version": 1, "change_type": "update"
        }
        ret = self._post("/scheduled_changes/releases", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 5, "signoffs": {}})
        r = dbo.releases.scheduled_changes.t.select().where(dbo.releases.scheduled_changes.sc_id == 5).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 5, "scheduled_by": "bill", "change_type": "update", "complete": False, "data_version": 1, "base_product": "d", "base_read_only": False,
            "base_name": "d", "base_data": {"name": "d", "hashFunction": "sha256", "schema_version": 1}, "base_data_version": 1
        }
        self.assertEqual(db_data, expected)
        cond = dbo.releases.scheduled_changes.conditions.t.select().where(dbo.releases.scheduled_changes.conditions.sc_id == 5).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "when": 2300000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeDeleteRelease(self):
        data = {
            "when": 4200000000, "name": "d", "data_version": 1, "change_type": "delete",
        }
        ret = self._post("/scheduled_changes/releases", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 5, "signoffs": {}})
        r = dbo.releases.scheduled_changes.t.select().where(dbo.releases.scheduled_changes.sc_id == 5).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 5, "scheduled_by": "bill", "change_type": "delete", "complete": False, "data_version": 1, "base_product": None, "base_read_only": False,
            "base_name": "d", "base_data": None, "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.releases.scheduled_changes.conditions.t.select().where(dbo.releases.scheduled_changes.conditions.sc_id == 5).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "when": 4200000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testAddScheduledChangeNewRelease(self):
        data = {
            "when": 5200000000, "name": "q", "data": '{"name": "q", "hashFunction": "sha512", "schema_version": 1}',
            "product": "q", "change_type": "insert",
        }
        ret = self._post("/scheduled_changes/releases", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"sc_id": 5, "signoffs": {}})
        r = dbo.releases.scheduled_changes.t.select().where(dbo.releases.scheduled_changes.sc_id == 5).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 5, "scheduled_by": "bill", "change_type": "insert", "complete": False, "data_version": 1, "base_product": "q", "base_read_only": False,
            "base_name": "q", "base_data": {"name": "q", "hashFunction": "sha512", "schema_version": 1}, "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.releases.scheduled_changes.conditions.t.select().where(dbo.releases.scheduled_changes.conditions.sc_id == 5).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 5, "data_version": 1, "when": 5200000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledUnknownScheduledChangeID(self):
        data = {
            "data": '{"name": "a", "hashFunction": "sha512", "extv": "3.0", "schema_version": 1}', "name": "a",
            "data_version": 1, "sc_data_version": 1, "when": 78900000000, "change_type": "update",
        }
        ret = self._post("/scheduled_changes/releases/98765432", data=data)
        self.assertEqual(ret.status_code, 404, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeExistingRelease(self):
        data = {
            "data": '{"name": "a", "hashFunction": "sha512", "extv": "3.0", "schema_version": 1}', "name": "a",
            "data_version": 1, "sc_data_version": 1, "when": 78900000000, "change_type": "update",
        }
        ret = self._post("/scheduled_changes/releases/2", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {'bill': 'releng'}})

        r = dbo.releases.scheduled_changes.t.select().where(dbo.releases.scheduled_changes.sc_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2, "complete": False, "change_type": "update", "data_version": 2, "scheduled_by": "bill", "base_name": "a", "base_product": "a",
            "base_read_only": False, "base_data": {"name": "a", "hashFunction": "sha512", "extv": "3.0", "schema_version": 1},
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.releases.scheduled_changes.conditions.t.select().where(dbo.releases.scheduled_changes.conditions.sc_id == 2).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 2, "data_version": 2, "when": 78900000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeExistingReleaseResetSignOffs(self):
        data = {
            "name": "ab", "data_version": 1, "sc_data_version": 1, "when": 88900000000, "change_type": "delete"
        }
        rows = dbo.releases.scheduled_changes.signoffs.t.select().\
            where(dbo.releases.scheduled_changes.signoffs.sc_id == 4).execute().fetchall()
        self.assertEqual(len(rows), 2)
        ret = self._post("/scheduled_changes/releases/4", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {'bill': 'releng'}})

        r = dbo.releases.scheduled_changes.t.select().where(
            dbo.releases.scheduled_changes.sc_id == 4).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 4, "complete": False, "change_type": "delete", "data_version": 2, "scheduled_by": "bill",
            "base_name": "ab", "base_product": None,
            "base_read_only": False,
            "base_data": None,
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        rows = dbo.releases.scheduled_changes.signoffs.t.select(). \
            where(dbo.releases.scheduled_changes.signoffs.sc_id == 4).execute().fetchall()
        self.assertEqual(len(rows), 1)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduleChangeExistingReleaseDiffUserResetSignOffs(self):
        data = {
            "data": '{"name": "a", "hashFunction": "sha512", "extv": "3.0", "schema_version": 1}', "name": "a",
            "data_version": 1, "sc_data_version": 1, "when": 78900000000, "change_type": "update"
        }
        rows = dbo.releases.scheduled_changes.signoffs.t.select(). \
            where(dbo.releases.scheduled_changes.signoffs.sc_id == 2).execute().fetchall()
        self.assertEqual(len(rows), 1)
        ret = self._post("/scheduled_changes/releases/2", data=data, username="julie")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {'julie': 'releng'}})

        r = dbo.releases.scheduled_changes.t.select().where(
            dbo.releases.scheduled_changes.sc_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2, "complete": False, "change_type": "update", "data_version": 2, "scheduled_by": "julie",
            "base_name": "a", "base_product": "a",
            "base_read_only": False,
            "base_data": {"name": "a", "hashFunction": "sha512", "extv": "3.0", "schema_version": 1},
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)
        rows = dbo.releases.scheduled_changes.signoffs.t.select(). \
            where(dbo.releases.scheduled_changes.signoffs.sc_id == 2).execute().fetchall()
        self.assertEqual(len(rows), 1)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeExistingDeleteRelease(self):
        data = {
            "name": "c",
            "data_version": 1, "sc_data_version": 1, "when": 78900000000, "change_type": "delete"
        }
        ret = self._post("/scheduled_changes/releases/4", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateCompletedScheduledChangeDeleteRelease(self):
        data = {
            "name": "c",
            "data_version": 1, "sc_data_version": 1, "when": 78900000000, "change_type": "delete"
        }
        ret = self._post("/scheduled_changes/releases/3", data=data)
        self.assertEqual(ret.status_code, 400, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateCompletedScheduledChangeUpdatingTheRelease(self):
        data = {
            "data": '{"name": "c", "hashFunction": "sha512", "extv": "3.0", "schema_version": 1}', "name": "c",
            "data_version": 1, "sc_data_version": 1, "when": 78900000000, "change_type": "update",
        }
        ret = self._post("/scheduled_changes/releases/3", data=data)
        self.assertEqual(ret.status_code, 400, ret.get_data())

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeNewRelease(self):
        data = {
            "data": '{"name": "m", "hashFunction": "sha512", "appv": "4.0", "schema_version": 1}', "name": "m", "product": "m",
            "sc_data_version": 1, "change_type": "insert",
        }
        ret = self._post("/scheduled_changes/releases/1", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {}})

        r = dbo.releases.scheduled_changes.t.select().where(dbo.releases.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1, "complete": False, "change_type": "insert", "data_version": 2, "scheduled_by": "bill", "base_name": "m", "base_product": "m",
            "base_read_only": False, "base_data": {"name": "m", "hashFunction": "sha512", "appv": "4.0", "schema_version": 1},
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.releases.scheduled_changes.conditions.t.select().where(dbo.releases.scheduled_changes.conditions.sc_id == 1).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 1, "data_version": 2, "when": 4000000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300))
    def testUpdateScheduledChangeNewReleaseChangeName(self):
        data = {
            "data": '{"name": "mm", "hashFunction": "sha512", "appv": "4.0", "schema_version": 1}', "name": "mm", "product": "mm",
            "sc_data_version": 1, "change_type": "insert",

        }
        ret = self._post("/scheduled_changes/releases/1", data=data)
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.get_json(), {"new_data_version": 2, "signoffs": {}})

        r = dbo.releases.scheduled_changes.t.select().where(dbo.releases.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1, "complete": False, "change_type": "insert", "data_version": 2, "scheduled_by": "bill", "base_name": "mm", "base_product": "mm",
            "base_read_only": False, "base_data": {"name": "mm", "hashFunction": "sha512", "appv": "4.0", "schema_version": 1},
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)
        cond = dbo.releases.scheduled_changes.conditions.t.select().where(dbo.releases.scheduled_changes.conditions.sc_id == 1).execute().fetchall()
        self.assertEqual(len(cond), 1)
        cond_expected = {"sc_id": 1, "data_version": 2, "when": 4000000000}
        self.assertEqual(dict(cond[0]), cond_expected)

    def testDeleteScheduledChange(self):
        ret = self._delete("/scheduled_changes/releases/2", qs={"data_version": 1})
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
        got = dbo.releases.scheduled_changes.t.select().where(dbo.releases.scheduled_changes.sc_id == 2).execute().fetchall()
        self.assertEqual(got, [])
        cond_got = dbo.releases.scheduled_changes.conditions.t.select().where(dbo.releases.scheduled_changes.conditions.sc_id == 2).execute().fetchall()
        self.assertEqual(cond_got, [])

    def testEnactScheduledChangeExistingRelease(self):
        ret = self._post("/scheduled_changes/releases/2/enact")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")

        r = dbo.releases.scheduled_changes.t.select().where(dbo.releases.scheduled_changes.sc_id == 2).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 2, "complete": True, "data_version": 2, "scheduled_by": "bill", "change_type": "update", "base_name": "a", "base_product": "a",
            "base_read_only": False, "base_data": {"name": "a", "hashFunction": "sha512", "schema_version": 1, "extv": "2.0"},
            "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)

        base_row = dict(dbo.releases.t.select().where(dbo.releases.name == "a").execute().fetchall()[0])
        base_expected = {
            "name": "a", "product": "a", "read_only": False,
            "data": {"name": "a", "hashFunction": "sha512", "schema_version": 1, "extv": "2.0"}, "data_version": 2,
        }
        self.assertEqual(base_row, base_expected)

    def testEnactScheduledChangeNewRelease(self):
        ret = self._post("/scheduled_changes/releases/1/enact")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")

        r = dbo.releases.scheduled_changes.t.select().where(dbo.releases.scheduled_changes.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 1, "complete": True, "data_version": 2, "scheduled_by": "bill", "change_type": "insert", "base_name": "m", "base_product": "m",
            "base_read_only": False, "base_data": {"name": "m", "hashFunction": "sha512", "schema_version": 1},
            "base_data_version": None,
        }
        self.assertEqual(db_data, expected)

        base_row = dict(dbo.releases.t.select().where(dbo.releases.name == "m").execute().fetchall()[0])
        base_expected = {
            "name": "m", "product": "m", "read_only": False,
            "data": {"name": "m", "hashFunction": "sha512", "schema_version": 1}, "data_version": 1,
        }
        self.assertEqual(base_row, base_expected)

    def testEnactScheduledChangeDeleteRelease(self):
        ret = self._post("/scheduled_changes/releases/4/enact")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")

        r = dbo.releases.scheduled_changes.t.select().where(dbo.releases.scheduled_changes.sc_id == 4).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        expected = {
            "sc_id": 4, "complete": True, "data_version": 2, "scheduled_by": "bill", "change_type": "delete", "base_name": "ab", "base_product": None,
            "base_read_only": False, "base_data": None, "base_data_version": 1,
        }
        self.assertEqual(db_data, expected)

        base_row = dbo.releases.t.select().where(dbo.releases.name == "ab").execute().fetchall()
        self.assertEqual(len(base_row), 0)

    def testGetScheduledChangeHistoryRevisions(self):
        ret = self._get("/scheduled_changes/releases/3/revisions")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        ret = ret.get_json()
        expected = {
            "count": 2,
            "revisions": [
                {
                    "change_id": 7, "changed_by": "bill", "timestamp": 25, "sc_id": 3, "scheduled_by": "bill", "change_type": "update", "data_version": 1,
                    "name": "b", "product": "b", "data": {"name": "b", "hashFunction": "sha512", "schema_version": 1}, "read_only": False,
                    "complete": True, "when": 10000000, "sc_data_version": 2,
                },
                {
                    "change_id": 6, "changed_by": "bill", "timestamp": 7, "sc_id": 3, "scheduled_by": "bill", "change_type": "update", "data_version": 1,
                    "name": "b", "product": "b", "data": {"name": "b", "hashFunction": "sha512", "schema_version": 1}, "read_only": False,
                    "complete": False, "when": 10000000, "sc_data_version": 1,
                },
            ],
        }
        self.assertEqual(ret, expected)

    @mock.patch("time.time", mock.MagicMock(return_value=300000))
    def testGetReleaseHistoryWithinTimeRange(self):
        ret = self._get("/releases/history", qs={"timestamp_from": 15, "timestamp_to": 33})
        self.assertEqual(ret.status_code, 200, ret.get_data())
        data = ret.get_json()
        expected = {
            'Releases scheduled change': {
                'revisions': [
                    {
                        'change_id': 9,
                        'read_only': False,
                        'name': 'ab',
                        'scheduled_by': 'bill',
                        'when': 230000000,
                        'changed_by': 'bill',
                        'data_version': 1,
                        'sc_id': 4,
                        'product': None,
                        'complete': False,
                        'data': None,
                        'timestamp': 26,
                        'change_type': 'delete',
                        'sc_data_version': 1
                    },
                    {
                        'change_id': 7,
                        'read_only': False,
                        'name': 'b',
                        'scheduled_by': 'bill',
                        'when': 10000000,
                        'changed_by': 'bill',
                        'data_version': 1,
                        'sc_id': 3,
                        'product': 'b',
                        'complete': True,
                        'data': {'hashFunction': 'sha512', 'schema_version': 1, 'name': 'b'},
                        'timestamp': 25,
                        'change_type': 'update',
                        'sc_data_version': 2
                    }
                ],
                'count': 2
            },
            'Releases': {
                'revisions': [
                    {
                        'change_id': 6,
                        'read_only': 'False',
                        'name': 'b',
                        '_different': [],
                        'changed_by': 'bill',
                        'data_version': 1,
                        'product': 'b',
                        'timestamp': 16,
                        '_time_ago': '48 years ago'
                    }
                ],
                'count': 1
            }
        }
        history_data = data["Releases"]
        revisions = history_data["revisions"]
        expected_data = expected["Releases"]
        expected_revisions = expected_data["revisions"]
        for index in range(len(revisions)):
            self.assertEqual(revisions[index]['product'], expected_revisions[index]['product'])
            self.assertEqual(revisions[index]['timestamp'], expected_revisions[index]['timestamp'])
            self.assertEqual(revisions[index]['read_only'], expected_revisions[index]['read_only'])
            self.assertEqual(revisions[index]['data_version'], expected_revisions[index]['data_version'])
            self.assertEqual(revisions[index]['changed_by'], expected_revisions[index]['changed_by'])
        self.assertEqual(len(history_data["revisions"]), 1)

    @mock.patch("time.time", mock.MagicMock(return_value=100))
    def testSignoffWithPermission(self):
        ret = self._post("/scheduled_changes/releases/1/signoffs", data=dict(role="qa"), username="bill")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
        r = dbo.releases.scheduled_changes.signoffs.t.select().where(dbo.releases.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 1)
        db_data = dict(r[0])
        self.assertEqual(db_data, {"sc_id": 1, "username": "bill", "role": "qa"})
        r = dbo.releases.scheduled_changes.signoffs.history.t.select().where(dbo.releases.scheduled_changes.signoffs.history.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 2)
        self.assertEqual(dict(r[0]), {"change_id": 3, "changed_by": "bill", "timestamp": 99999, "sc_id": 1, "username": "bill", "role": None})
        self.assertEqual(dict(r[1]), {"change_id": 4, "changed_by": "bill", "timestamp": 100000, "sc_id": 1, "username": "bill", "role": "qa"})

    def testSignoffWithoutPermission(self):
        ret = self._post("/scheduled_changes/releases/1/signoffs", data=dict(role="relman"), username="bill")
        self.assertEqual(ret.mimetype, "application/json")
        self.assertEqual(ret.status_code, 403, ret.get_data())

    def testSignoffWithoutRole(self):
        ret = self._post("/scheduled_changes/releases/1/signoffs", data=dict(lorem="random"), username="bill")
        self.assertEqual(ret.mimetype, "application/problem+json")
        self.assertEqual(ret.status_code, 400, ret.get_data())

    def testRevokeSignoff(self):
        ret = self._delete("/scheduled_changes/releases/2/signoffs", username="bill")
        self.assertEqual(ret.status_code, 200, ret.get_data())
        self.assertEqual(ret.mimetype, "application/json")
        r = dbo.releases.scheduled_changes.signoffs.t.select().where(dbo.releases.scheduled_changes.signoffs.sc_id == 1).execute().fetchall()
        self.assertEqual(len(r), 0)

    def testReleasesScheduledChangeViewDiff(self):
        table = dbo.releases.scheduled_changes
        sc = table.select(where=[table.change_type == 'update'], limit=1)[0]
        ret = self._get("/scheduled_change/diff/release/{}".format(sc['sc_id']))
        self.assertEqual(ret.status_code, 200, ret.get_data())


class TestReleaseHistoryView(ViewTest):

    @mock.patch("time.time", mock.MagicMock(return_value=300000))
    def testGetRevisions(self):
        # Make some changes to a release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                data_version=1,
            )
        )
        self.assertStatusCode(ret, 200)

        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                data_version=2,
            )
        )
        self.assertStatusCode(ret, 200)

        url = '/releases/d/revisions'
        ret = self._get(url)
        self.assertEqual(ret.status_code, 200, msg=ret.get_data())
        data = ret.get_json()
        self.assertEqual(data["count"], 3)
        self.assertEqual(len(data["revisions"]), 3)

        with self.assertRaises(KeyError):
            data['data']

    @mock.patch("time.time", mock.MagicMock(return_value=300000))
    def testGetHistory(self):
        url = '/releases/history'
        ret = self._get(url)
        self.assertEqual(ret.status_code, 200, msg=ret.get_data())
        data = ret.get_json()
        expected = {
            'Releases': {
                'count': 2,
                'revisions': [
                    {
                        'name': 'b',
                        'change_id': 6,
                        'read_only': 'False',
                        '_time_ago': '48 years ago',
                        'data_version': 1,
                        '_different': [],
                        'timestamp': 16,
                        'product': 'b',
                        'changed_by': 'bill'
                    },
                    {
                        'name': 'd',
                        'change_id': 4,
                        'read_only': 'False',
                        '_time_ago': '48 years ago',
                        'data_version': 1,
                        '_different': ['name', 'data', 'product'],
                        'timestamp': 10, 'product': 'd', 'changed_by': 'bill'
                    },
                    {
                        'name': 'ab',
                        'change_id': 2,
                        'read_only': 'False',
                        '_time_ago': '48 years ago',
                        'data_version': 1,
                        '_different': ['name', 'data', 'product'],
                        'timestamp': 6,
                        'product': 'a',
                        'changed_by': 'bill'
                    }
                ]
            },
            "Releases Scheduled Change": {
                'count': 2,
                'revisions': [
                    {
                        'product': 'a', 'changed_by': 'bill', 'data': {'name': 'a', 'extv': '2.0', 'hashFunction': 'sha512', 'schema_version': 1},
                        'sc_id': 2, 'sc_data_version': 1, 'scheduled_by': 'bill', 'data_version': 1, 'complete': False, 'when': 6000000000,
                        'change_type': 'update', 'name': 'a', 'timestamp': 71, 'change_id': 4, 'read_only': False
                    },
                    {
                        'product': 'm', 'changed_by': 'bill', 'data': {'name': 'm', 'hashFunction': 'sha512', 'schema_version': 1},
                        'sc_id': 1, 'sc_data_version': 1, 'scheduled_by': 'bill', 'data_version': None, 'complete': False,
                        'when': 4000000000, 'change_type': 'insert', 'name': 'm', 'timestamp': 51, 'change_id': 2, 'read_only': False
                    },
                ],
            }
        }
        history_data = data["Releases"]
        revisions = history_data["revisions"]
        expected_data = expected["Releases"]
        expected_revisions = expected_data["revisions"]
        for index in range(len(revisions)):
            self.assertEqual(revisions[index]['product'], expected_revisions[index]['product'])
            self.assertEqual(revisions[index]['timestamp'], expected_revisions[index]['timestamp'])
            self.assertEqual(revisions[index]['read_only'], expected_revisions[index]['read_only'])
            self.assertEqual(revisions[index]['data_version'], expected_revisions[index]['data_version'])
            self.assertEqual(revisions[index]['changed_by'], expected_revisions[index]['changed_by'])
        self.assertEqual(len(history_data["revisions"]), 3)

    @mock.patch("time.time", mock.MagicMock(return_value=300000))
    def testPostRevisionRollback(self):
        # Make some changes to a release
        data = json.dumps(dict(detailsUrl='beep', fakePartials=True, schema_version=1))
        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                data_version=1,
            )
        )
        self.assertStatusCode(ret, 200)

        data = json.dumps(dict(detailsUrl='boop', fakePartials=False, schema_version=1))
        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                data_version=2,
            )
        )
        self.assertStatusCode(ret, 200)

        rows = dbo.releases.t.select().where(dbo.releases.name == "d").execute().fetchall()
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row['data_version'], 3)
        data = row['data']
        self.assertEqual(data['fakePartials'], False)
        self.assertEqual(data['detailsUrl'], 'boop')

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "d")\
                                                      .where(dbo.releases.history.data_version == 2).execute().fetchall()
        self.assertEqual(len(history_rows), 1)
        history_row = history_rows[0]

        url = '/releases/d/revisions'
        ret = self._post(url, {'change_id': history_row["change_id"]})
        self.assertEqual(ret.status_code, 200, ret.get_data())

        history_rows = dbo.releases.history.t.select().where(dbo.releases.history.name == "d").execute().fetchall()
        self.assertEqual(len(history_rows), 5)
        history_row = history_rows[-1]

        self.assertEqual(history_row['data_version'], 4)
        data = history_row['data']
        self.assertEqual(data['fakePartials'], True)
        self.assertEqual(data['detailsUrl'], 'beep')

    @mock.patch("time.time", mock.MagicMock(return_value=300000))
    def testPostRevisionRollbackBadRequests(self):
        data = json.dumps(dict(detailsUrl='beep', fakePartials=True, schema_version=1))
        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                data_version=1,
            )
        )
        self.assertStatusCode(ret, 200)
        # when posting you need both the release name and the change_id
        ret = self._post('/releases/CRAZYNAME/revisions', data={'change_id': 1})
        self.assertEqual(ret.status_code, 404, ret.get_data())

        url = '/releases/d/revisions'
        ret = self._post(url, {'change_id': 999})
        self.assertEqual(ret.status_code, 400)

        ret = self._post(url)
        self.assertEqual(ret.status_code, 400)


class TestSingleColumn_JSON(ViewTest):

    def testGetReleasesSingleColumn(self):
        expected_product = ["a", "c", "b", "d"]
        expected = dict(count=4, product=expected_product)
        ret = self._get("/releases/columns/product")
        ret_data = ret.get_json()
        self.assertEqual(ret_data['count'], expected['count'])
        self.assertEqual(ret_data['product'].sort(), expected['product'].sort())

    def testGetReleaseColumn404(self):
        ret = self.client.get("/releases/columns/blah")
        self.assertEqual(ret.status_code, 404)


class TestReadOnlyView(ViewTest):

    def testReadOnlyGet(self):
        ret = self._get('/releases/b/read_only')
        is_read_only = dbo.releases.t.select(dbo.releases.name == 'b').execute().first()['read_only']
        self.assertEqual(ret.get_json()['read_only'], is_read_only)

    def testReadOnlySetTrueAdmin(self):
        data = dict(name='b', read_only=True, product='b', data_version=1)
        ret = self._put('/releases/b/read_only', username='bill', data=data)
        self.assertStatusCode(ret, 201)
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, True)

    def testReadOnlySetTrueNonAdmin(self):
        data = dict(name='b', read_only=True, product='b', data_version=1)
        ret = self._put('/releases/b/read_only', username='bob', data=data)
        self.assertStatusCode(ret, 201)
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, True)

    def testReadOnlySetFalseAdmin(self):
        dbo.releases.t.update(values=dict(read_only=True, data_version=2)).where(dbo.releases.name == "a").execute()
        data = dict(name='b', read_only='', product='b', data_version=2)
        ret = self._put('/releases/b/read_only', username='bill', data=data)
        self.assertStatusCode(ret, 201)
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, False)

    def testReadOnlyUnsetWithoutPermissionForProduct(self):
        dbo.releases.t.update(values=dict(read_only=True, data_version=2)).where(dbo.releases.name == "a").execute()
        data = dict(name='b', read_only='', product='b', data_version=2)
        ret = self._put('/releases/b/read_only', username='me', data=data)
        self.assertStatusCode(ret, 403)

    def testReadOnlyAdminSetAndUnsetFlag(self):
        # Setting flag
        data = dict(name='b', read_only=True, product='b', data_version=1)
        ret = self._put('/releases/b/read_only', username='bill', data=data)
        self.assertStatusCode(ret, 201)

        # Resetting flag
        data = dict(name='b', read_only='', product='b', data_version=2)
        ret = self._put('/releases/b/read_only', username='bill', data=data)
        self.assertStatusCode(ret, 201)

        # Verify reset
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, False)

    def testReadOnlyNonAdminCanSetFlagButNotUnset(self):
        # Setting read only flag
        data_set = dict(name='b', read_only=True, product='b', data_version=1)
        ret = self._put('/releases/b/read_only', username='bob', data=data_set)
        self.assertStatusCode(ret, 201)

        # Verifying if flag was set to true
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, True)

        # Resetting flag, which should fail with 403
        data_unset = dict(name='b', read_only='', product='b', data_version=2)
        ret = self._put('/releases/b/read_only', username='bob', data=data_unset)
        self.assertStatusCode(ret, 403)


class TestRuleIdsReturned(ViewTest):

    def testPresentRuleIdField(self):
        releases = self._get("/releases")
        releases_data = json.loads(releases.data)
        self.assertTrue('rule_ids' in releases_data['releases'][0])

    def testMappingIncluded(self):
        rel_name = 'ab'
        rule_id = 10

        releases = self._get("/releases")
        releases_data = json.loads(releases.data)
        not_mapped_rel = next(rel for rel in releases_data['releases'] if rel['name'] == rel_name)
        self.assertEqual(len(not_mapped_rel['rule_ids']), 0)
        self.assertFalse(rule_id in not_mapped_rel['rule_ids'])

        dbo.rules.t.insert().execute(id=rule_id, priority=100, version='3.5', buildTarget='d',
                                     backgroundRate=100, mapping=rel_name, update_type='minor', data_version=1)

        releases = self._get("/releases")
        releases_data = json.loads(releases.data)
        mapped_rel = next(rel for rel in releases_data['releases'] if rel['name'] == rel_name)
        self.assertEqual(len(mapped_rel['rule_ids']), 1)
        self.assertTrue(rule_id in mapped_rel['rule_ids'])
