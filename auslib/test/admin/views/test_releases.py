import simplejson as json

from sqlalchemy import select

from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest, JSONTestMixin


class TestReleasesAPI_JSON(ViewTest, JSONTestMixin):

    def testGetRelease(self):
        ret = self._get("/releases/b")
        self.assertStatusCode(ret, 200)
        self.assertEqual(json.loads(ret.data), json.loads("""
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
        self.assertEqual(json.loads(ret), json.loads("""
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

    def testReleasePutUpdateOutdatedData(self):
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
        blob = """
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
        # Testing Put request to add new release
        ret = self._put('/releases/dd', data=dict(data=data, name='dd', blob=blob, product='dd', data_version=1))
        self.assertStatusCode(ret, 201)

        ret = select([dbo.releases.data]).where(dbo.releases.name == 'dd').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads(blob))

        # Updating same release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
        ret = self._put('/releases/dd', data=dict(data=data, name='dd', product='dd', blob=blob, data_version=1))
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)

        # Outdated Data Error on same release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
        ret = self._put('/releases/dd', data=dict(data=data, name='dd', product='dd', blob=blob, data_version=1))
        self.assertStatusCode(ret, 400)

    def testReleasePostUpdateOutdatedData(self):
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
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
        # Testing Post request to add new release
        ret = self._post('/releases/ee', data=dict(data=data, hashFunction="sha512", name='ee', blob=blob, product='ee', data_version=1))
        self.assertStatusCode(ret, 201)

        # Updating same release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = self._post('/releases/ee', data=dict(data=data, hashFunction="sha512", name='ee', product='ee', blob=blob, data_version=2))
        self.assertStatusCode(ret, 200)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=3)), "Data: %s" % ret.data)

        # Outdated Data Error on same release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
        ret = self._post('/releases/ee', data=dict(data=data, hashFunction="sha512", name='ee', product='ee', blob=blob, data_version=1))
        self.assertStatusCode(ret, 400)

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

    def testReleasePostCreatesNewReleasev1(self):
        data = json.dumps(dict(bouncerProducts=dict(partial='foo'), name='e', hashFunction="sha512"))
        ret = self._post('/releases/e', data=dict(data=data, product='e', schema_version=1))
        self.assertStatusCode(ret, 201)
        ret = dbo.releases.t.select().where(dbo.releases.name == 'e').execute().fetchone()
        self.assertEqual(ret['product'], 'e')
        self.assertEqual(ret['name'], 'e')
        self.assertEqual(json.loads(ret['data']), json.loads("""
{
    "name": "e",
    "hashFunction": "sha512",
    "schema_version": 1,
    "bouncerProducts": {
        "partial": "foo"
    }
}
"""))

    def testReleasePostCreatesNewReleaseNopermission(self):
        data = json.dumps(dict(bouncerProducts=dict(partial='foo'), name='e', hashFunction="sha512"))
        ret = self._post('/releases/e', data=dict(data=data, product='e', schema_version=1), username="kate")
        self.assertStatusCode(ret, 403)

    def testReleasePostCreatesNewReleasev2(self):
        data = json.dumps(dict(bouncerProducts=dict(complete='foo'), name='e', hashFunction="sha512"))
        ret = self._post('/releases/e', data=dict(data=data, product='e', schema_version=2))
        self.assertStatusCode(ret, 201)
        ret = dbo.releases.t.select().where(dbo.releases.name == 'e').execute().fetchone()
        self.assertEqual(ret['product'], 'e')
        self.assertEqual(ret['name'], 'e')
        self.assertEqual(json.loads(ret['data']), json.loads("""
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
        ret = self._post('/releases/a', data=dict(data=data))
        self.assertStatusCode(ret, 400)

    def testReleasePostRejectedURL(self):
        data = json.dumps(dict(platforms=dict(p=dict(locales=dict(f=dict(complete=dict(fileUrl='http://evil.com')))))))
        ret = self._post('/releases/d', data=dict(data=data, product='d', data_version=1))
        self.assertStatusCode(ret, 400)

    def testDeleteRelease(self):
        ret = self._delete("/releases/d", qs=dict(data_version=1))
        self.assertStatusCode(ret, 200)
        ret = dbo.releases.t.count().where(dbo.releases.name == 'd').execute().first()[0]
        self.assertEqual(ret, 0)

    def testDeleteReleaseOutdatedData(self):
        # Release's data version is outdated
        ret = self._get("/releases/d")
        self.assertStatusCode(ret, 200)
        ret = self._delete("/releases/d", qs=dict(data_version=7))
        self.assertStatusCode(ret, 400)

    def testDeleteNonExistentRelease(self):
        ret = self._delete("/releases/ueo")
        self.assertStatusCode(ret, 404)

    def testDeleteWithoutPermission(self):
        ret = self._delete("/releases/a", username="bob", qs=dict(data_version=1))
        self.assertStatusCode(ret, 403)

    def testDeleteWithoutPermissionForAction(self):
        ret = self._delete("/releases/b", username="bob", qs=dict(data_version=1))
        self.assertStatusCode(ret, 403)

    def testDeleteReadOnlyRelease(self):
        dbo.releases.t.update(values=dict(read_only=True, data_version=2)).where(dbo.releases.name == "a").execute()
        ret = self._delete("/releases/a", username="bill", qs=dict(data_version=2))
        self.assertStatusCode(ret, 403)

    def testLocalePut(self):
        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "abc",
            }
        })
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'a').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "a",
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
"""))

    def testLocalePutSpecificPermission(self):
        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "abc",
            }
        })
        ret = self._put('/releases/a/builds/p/l', username="ashanti", data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'a').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "a",
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
"""))

    def testLocalePutWithBadHashFunction(self):
        data = json.dumps(dict(complete=dict(filesize='435')))
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 400)

    def testLocalePutWithoutPermission(self):
        data = '{"complete": {"filesize": 435, "from": "*", "hashValue": "abc"}}'
        ret = self._put('/releases/a/builds/p/l', username='liu', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 403)

    def testLocalePutWithoutPermissionForProduct(self):
        data = '{"complete": {"filesize": 435, "from": "*", "hashValue": "abc"}}'
        ret = self._put('/releases/a/builds/p/l', username='bob', data=dict(data=data, product='a', data_version=1, schema_version=1))
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
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'e').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
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
"""))

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
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'd').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
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
"""))

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
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'e').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
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
"""))

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
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'd').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
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
"""))

    def testLocalePutWithCopy(self):
        data = json.dumps({
            "partial": {
                "filesize": 123,
                "from": "b",
                "hashValue": "abc",
            }
        })
        data = dict(data=data, product='a', copyTo=json.dumps(['ab']), data_version=1, schema_version=1)
        ret = self._put('/releases/a/builds/p/l', data=data)
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'a').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "a",
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
"""))
        ret = select([dbo.releases.data]).where(dbo.releases.name == 'ab').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
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
"""))

    def testLocalePutBadJSON(self):
        ret = self._put('/releases/a/builds/p/l', data=dict(data='a', product='a'))
        self.assertStatusCode(ret, 400)

    def testLocaleRejectedURL(self):
        data = json.dumps(dict(complete=dict(fileUrl='http://evil.com')))
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', data_version=1))
        self.assertStatusCode(ret, 400)

    def testLocaleGet(self):
        ret = self._get('/releases/d/builds/p/d')
        self.assertStatusCode(ret, 200)
        got = json.loads(ret.data)
        expected = {
            "complete": {
                "filesize": 1234,
                "from": "*",
                "hashValue": "abc",
            }
        }
        self.assertEquals(got, expected)
        self.assertEqual(ret.headers['X-Data-Version'], '1')

    def testLocalePutNotAllowed(self):
        ret = self.client.put('/releases/d/builds/p/d', data=dict(product='a'))
        self.assertStatusCode(ret, 401)

    def testLocalePutReadOnlyRelease(self):
        dbo.releases.t.update(values=dict(read_only=True, data_version=2)).where(dbo.releases.name == "a").execute()
        data = json.dumps({
            "complete": {
                "filesize": 435,
                "from": "*",
                "hashValue": "abc",
            }
        })
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 403)

    def testLocalePutCantChangeProduct(self):
        data = json.dumps(dict(complete=dict(filesize=435)))
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='b', schema_version=1))
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

        self.assertEquals(ret.status_code, 201, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = dbo.releases.t.select().where(dbo.releases.name == 'new_release').execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['name'], 'new_release')
        self.assertEquals(r[0]['product'], 'Firefox')
        self.assertEquals(json.loads(r[0]['data']), json.loads("""
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
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = dbo.releases.t.select().where(dbo.releases.name == 'd').execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['name'], 'd')
        self.assertEquals(r[0]['product'], 'Firefox')
        self.assertEquals(json.loads(r[0]['data']), json.loads("""
{
    "name": "d",
    "schema_version": 3,
    "hashFunction": "sha512",
    "actions": "doit"
}
"""))

    def testGMPReleasePut(self):

        ret = self._put('/releases/gmprel', data=dict(name='gmprel', product='GMP',
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
                    "filesize": "2",
                    "hashValue": "3",
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

        self.assertEquals(ret.status_code, 201, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = dbo.releases.t.select().where(dbo.releases.name == 'gmprel').execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['name'], 'gmprel')
        self.assertEquals(r[0]['product'], 'GMP')
        self.assertEquals(json.loads(r[0]['data']), json.loads("""
{
    "name": "gmprel",
    "schema_version": 1000,
    "hashFunction": "sha512",
    "vendors": {
        "foo": {
            "version": "1",
            "platforms": {
                "a": {
                    "filesize": "2",
                    "hashValue": "3",
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
        data = json.loads(ret.data)
        self.assertEquals(len(data["releases"]), 5)

    def testGetReleasesNamesOnly(self):
        ret = self._get("/releases", qs=dict(names_only=1))
        self.assertStatusCode(ret, 200)
        self.assertEquals(json.loads(ret.data), json.loads("""
{
    "names": [
        "a", "ab", "b", "c", "d"
    ]
}
"""))

    def testGetReleasesNamePrefix(self):
        ret = self._get("/releases", qs=dict(name_prefix='a'))
        self.assertStatusCode(ret, 200)
        self.assertEquals(json.loads(ret.data), json.loads("""
{
    "releases": [
        {"data_version": 1, "name": "a", "product": "a", "read_only": false, "rule_ids": [3, 4]},
        {"data_version": 1, "name": "ab", "product": "a", "read_only": false, "rule_ids": []}
    ]
}
"""))

    def testGetReleasesNamePrefixNamesOnly(self):
        ret = self._get("/releases", qs=dict(name_prefix='a',
                                             names_only='1'))
        self.assertStatusCode(ret, 200)
        self.assertEquals(json.loads(ret.data), json.loads("""
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
        self.assertEqual(json.loads(ret['data']), json.loads("""
{
    "name": "e",
    "hashFunction": "sha512",
    "schema_version": 1,
    "bouncerProducts": {
        "partial": "foo"
    }
}
"""))


def byteify(input):
    if isinstance(input, dict):
        res = {}
        for key, value in input.items():
            res[byteify(key)] = byteify(value)
        return res
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


class TestReleaseHistoryView(ViewTest, JSONTestMixin):

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
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        data = json.loads(ret.data)
        self.assertEquals(data["count"], 2)
        self.assertEquals(len(data["revisions"]), 2)

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

        table = dbo.releases
        row, = table.select(where=[table.name == 'd'])
        self.assertEqual(row['data_version'], 3)
        data = json.loads(row['data'])
        self.assertEqual(data['fakePartials'], False)
        self.assertEqual(data['detailsUrl'], 'boop')

        query = table.history.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 2)

        row, = table.history.select(
            where=[(table.history.product == 'd') & (table.history.data_version == 2)],
            limit=1
        )
        change_id = row['change_id']
        assert row['name'] == 'd'  # one of the fixtures

        url = '/releases/d/revisions'
        ret = self._post(url, json.dumps({'change_id': change_id}), content_type="application/json")
        self.assertEquals(ret.status_code, 200, ret.data)

        query = table.history.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 3)

        row, = table.select(where=[table.name == 'd'])
        self.assertEqual(row['data_version'], 4)
        data = json.loads(row['data'])
        self.assertEqual(data['fakePartials'], True)
        self.assertEqual(data['detailsUrl'], 'beep')

    def testPostRevisionRollbackBadRequests(self):
        # when posting you need both the release name and the change_id
        ret = self._post('/releases/CRAZYNAME/revisions', json.dumps({'change_id': 1}), content_type="application/json")
        self.assertEquals(ret.status_code, 404)

        url = '/releases/d/revisions'
        ret = self._post(url, json.dumps({'change_id': 999}), content_type="application/json")
        self.assertEquals(ret.status_code, 404)

        ret = self._post(url)
        self.assertEquals(ret.status_code, 400)


class TestSingleColumn_JSON(ViewTest, JSONTestMixin):

    def testGetReleasesSingleColumn(self):
        expected_product = ["a", "c", "b", "d"]
        expected = dict(count=4, product=expected_product)
        ret = self._get("/releases/columns/product")
        ret_data = json.loads(ret.data)
        self.assertEquals(ret_data['count'], expected['count'])
        self.assertEquals(ret_data['product'].sort(), expected['product'].sort())

    def testGetReleaseColumn404(self):
        ret = self.client.get("/releases/columns/blah")
        self.assertEquals(ret.status_code, 404)


class TestReadOnlyView(ViewTest, JSONTestMixin):

    def testReadOnlyGet(self):
        ret = self._get('/releases/b/read_only')
        is_read_only = dbo.releases.t.select(dbo.releases.name == 'b').execute().first()['read_only']
        self.assertEqual(json.loads(ret.data)['read_only'], is_read_only)

    def testReadOnlySetTrueAdmin(self):
        data = dict(name='b', read_only=True, product='Firefox', data_version=1)
        self._put('/releases/b/read_only', username='bill', data=data)
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, True)

    def testReadOnlySetTrueNonAdmin(self):
        data = dict(name='b', read_only=True, product='Firefox', data_version=1)
        self._put('/releases/b/read_only', username='bob', data=data)
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, True)
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, True)

    def testReadOnlySetFalseAdmin(self):
        dbo.releases.t.update(values=dict(read_only=True, data_version=2)).where(dbo.releases.name == "a").execute()
        data = dict(name='b', read_only='', product='Firefox', data_version=2)
        self._put('/releases/b/read_only', username='bill', data=data)
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, False)

    def testReadOnlyUnsetWithoutPermissionForProduct(self):
        dbo.releases.t.update(values=dict(read_only=True, data_version=2)).where(dbo.releases.name == "a").execute()
        data = dict(name='b', read_only='', product='Firefox', data_version=2)
        ret = self._put('/releases/b/read_only', username='me', data=data)
        self.assertStatusCode(ret, 403)

    def testReadOnlyAdminSetAndUnsetFlag(self):
        # Setting flag
        data = dict(name='b', read_only=True, product='Firefox', data_version=1)
        ret = self._put('/releases/b/read_only', username='bill', data=data)
        self.assertStatusCode(ret, 201)

        # Resetting flag
        data = dict(name='b', read_only='', product='Firefox', data_version=2)
        ret = self._put('/releases/b/read_only', username='bill', data=data)
        self.assertStatusCode(ret, 201)

        # Verify reset
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, False)

    def testReadOnlyNonAdminCanSetFlagButNotUnset(self):
        # Setting read only flag
        data_set = dict(name='b', read_only=True, product='Firefox', data_version=1)
        ret = self._put('/releases/b/read_only', username='bob', data=data_set)
        self.assertStatusCode(ret, 201)

        # Verifying if flag was set to true
        read_only = dbo.releases.isReadOnly(name='b')
        self.assertEqual(read_only, True)

        # Resetting flag, which should fail with 403
        data_unset = dict(name='b', read_only='', product='Firefox', data_version=2)
        ret = self._put('/releases/b/read_only', username='bob', data=data_unset)
        self.assertStatusCode(ret, 403)


class TestRuleIdsReturned(ViewTest, JSONTestMixin):

    def testPresentRuleIdField(self):
        releases = self._get("/releases")
        releases_data = json.loads(releases.data)
        self.assertTrue('rule_ids' in releases_data['releases'][0])

    def testWhitelistIncluded(self):
        rel_name = 'ab'
        rule_id = 6

        releases = self._get("/releases")
        releases_data = json.loads(releases.data)
        not_whitelisted_rel = next(rel for rel in releases_data['releases'] if rel['name'] == rel_name)
        self.assertEqual(len(not_whitelisted_rel['rule_ids']), 0)
        self.assertFalse(rule_id in not_whitelisted_rel['rule_ids'])

        dbo.rules.t.insert().execute(id=rule_id, priority=100, version='3.5', buildTarget='d',
                                     backgroundRate=100, whitelist=rel_name, update_type='minor', data_version=1)

        releases = self._get("/releases")
        releases_data = json.loads(releases.data)
        whitelisted_rel = next(rel for rel in releases_data['releases'] if rel['name'] == rel_name)
        self.assertEqual(len(whitelisted_rel['rule_ids']), 1)
        self.assertTrue(rule_id in whitelisted_rel['rule_ids'])

    def testMappingIncluded(self):
        rel_name = 'ab'
        rule_id = 6

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
