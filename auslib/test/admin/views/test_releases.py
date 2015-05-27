import mock
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
        ret = self._post('/releases/d', data=dict(data=data, product='d', version='d', data_version=1))
        self.assertStatusCode(ret, 200)
        ret = select([dbo.releases.data]).where(dbo.releases.name=='d').execute().fetchone()[0]
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
                        "filesize": "1234"
                    }
                }
            }
        }
    }
}
"""))

    def testReleasePostUpdateChangeHashFunction(self):
        data = json.dumps(dict(detailsUrl='blah', hashFunction="sha1024", schema_version=1))
        ret = self._post('/releases/d', data=dict(data=data, product='d', version='d', data_version=1))
        self.assertStatusCode(ret, 400)

    def testReleasePostUpdateChangeProduct(self):
        data = json.dumps(dict(detailsUrl="abc", schema_version=1))
        ret = self._post("/releases/c", data=dict(data=data, product="h", version="c", data_version=1))
        self.assertStatusCode(ret, 400)

    def testReleasePostInvalidBlob(self):
        data = json.dumps(dict(uehont="uhetn", schema_version=1))
        ret = self._post("/releases/c", data=dict(data=data, product="c", version="c", data_version=1))
        self.assertStatusCode(ret, 400)

    def testReleasePostCreatesNewReleasev1(self):
        data = json.dumps(dict(bouncerProducts=dict(linux='foo'), name='e'))
        ret = self._post('/releases/e', data=dict(data=data, product='e', version='e', schema_version=1))
        self.assertStatusCode(ret, 201)
        ret = dbo.releases.t.select().where(dbo.releases.name=='e').execute().fetchone()
        self.assertEqual(ret['product'], 'e')
        self.assertEqual(ret['version'], 'e')
        self.assertEqual(ret['name'], 'e')
        self.assertEqual(json.loads(ret['data']), json.loads("""
{
    "name": "e",
    "schema_version": 1,
    "bouncerProducts": {
        "linux": "foo"
    }
}
"""))

    def testReleasePostCreatesNewReleasev2(self):
        data = json.dumps(dict(bouncerProducts=dict(linux='foo'), name='e'))
        ret = self._post('/releases/e', data=dict(data=data, product='e', version='e', schema_version=2))
        self.assertStatusCode(ret, 201)
        ret = dbo.releases.t.select().where(dbo.releases.name=='e').execute().fetchone()
        self.assertEqual(ret['product'], 'e')
        self.assertEqual(ret['version'], 'e')
        self.assertEqual(ret['name'], 'e')
        self.assertEqual(json.loads(ret['data']), json.loads("""
{
    "name": "e",
    "schema_version": 2,
    "bouncerProducts": {
        "linux": "foo"
    }
}
"""))

    def testReleasePostInvalidKey(self):
        data = json.dumps(dict(foo=1))
        ret = self._post('/releases/a', data=dict(data=data))
        self.assertStatusCode(ret, 400)

    def testReleasePostRejectedURL(self):
        data = json.dumps(dict(platforms=dict(p=dict(locales=dict(f=dict(complete=dict(fileUrl='http://evil.com')))))))
        ret = self._post('/releases/d', data=dict(data=data, product='d', version='d', data_version=1))
        self.assertStatusCode(ret, 400)

    def testDeleteRelease(self):
        ret = self._delete("/releases/d", qs=dict(data_version=1))
        self.assertStatusCode(ret, 200)
        ret = dbo.releases.t.count().where(dbo.releases.name=='d').execute().first()[0]
        self.assertEqual(ret, 0)

    def testDeleteNonExistentRelease(self):
        ret = self._delete("/releases/ueo")
        self.assertStatusCode(ret, 404)

    def testDeleteWithoutPermission(self):
        ret = self._delete("/releases/a", username="bob")
        self.assertStatusCode(ret, 401)

    def testLocalePut(self):
        data = json.dumps(dict(complete=dict(filesize='435')))
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', version='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name=='a').execute().fetchone()[0]
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
                        "filesize": "435"
                    }
                }
            }
        }
    }
}
"""))

    def testLocalePutWithBadHashFunction(self):
        return
        data = json.dumps(dict(complete=dict(filesize='435')))
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', version='a', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 400)

    def testLocalePutWithoutPermissionForProduct(self):
        data = json.dumps(dict(complete=dict(filesize='435')))
        ret = self._put('/releases/a/builds/p/l', username='bob', data=dict(data=data, product='a', version='a', data_version=1))
        self.assertStatusCode(ret, 401)

    def testLocalePutForNewRelease(self):
        data = json.dumps(dict(complete=dict(filesize='678')))
        # setting schema_version in the incoming blob is a hack for testing
        # SingleLocaleView._put() doesn't give us access to the form
        ret = self._put('/releases/e/builds/p/a', data=dict(data=data, product='e', version='e', hashFunction="sha512", schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name=='e').execute().fetchone()[0]
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
                        "filesize": "678"
                    }
                }
            }
        }
    }
}
"""))

    def testLocalePutAppend(self):
        data = json.dumps(dict(partial=dict(fileUrl='http://good.com/blah')))
        ret = self._put('/releases/d/builds/p/g', data=dict(data=data, product='d', version='d', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name=='d').execute().fetchone()[0]
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
                        "filesize": "1234"
                    }
                },
                "g": {
                    "partial": {
                        "fileUrl": "http://good.com/blah"
                    }
                }
            }
        }
    }
}
"""))

    def testLocalePutForNewReleaseWithAlias(self):
        data = json.dumps(dict(complete=dict(filesize='678')))
        # setting schema_version in the incoming blob is a hack for testing
        # SingleLocaleView._put() doesn't give us access to the form
        ret = self._put('/releases/e/builds/p/a', data=dict(data=data, product='e', version='e', alias='["p2"]', schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name=='e').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "e",
    "schema_version": 1,
    "platforms": {
        "p": {
            "locales": {
                "a": {
                    "complete": {
                        "filesize": "678"
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
        data = json.dumps(dict(partial=dict(fileUrl='http://good.com/blah')))
        ret = self._put('/releases/d/builds/q/g', data=dict(data=data, product='d', version='d', data_version=1, alias='["q2"]', schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name=='d').execute().fetchone()[0]
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
                        "filesize": "1234"
                    }
                }
            }
        },
        "q": {
            "locales": {
                "g": {
                    "partial": {
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
        data = json.dumps(dict(partial=dict(filesize='123')))
        data = dict(data=data, product='a', version='a', copyTo=json.dumps(['ab']), data_version=1, schema_version=1)
        ret = self._put('/releases/a/builds/p/l', data=data)
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name=='a').execute().fetchone()[0]
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
                        "filesize": "123"
                    }
                }
            }
        }
    }
}
"""))
        ret = select([dbo.releases.data]).where(dbo.releases.name=='ab').execute().fetchone()[0]
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
                        "filesize": "123"
                    }
                }
            }
        }
    }
}
"""))

    def testLocalePutChangeVersion(self):
        data = json.dumps(dict(extv='b'))
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', version='b', data_version=1, schema_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=3)), "Data: %s" % ret.data)
        ret = select([dbo.releases.data]).where(dbo.releases.name=='a').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "a",
    "schema_version": 1,
    "hashFunction": "sha512",
    "platforms": {
        "p": {
            "locales": {
                "l": {
                    "extv": "b"
                }
            }
        }
    }
}
"""))
        newVersion = select([dbo.releases.version]).where(dbo.releases.name=='a').execute().fetchone()[0]
        self.assertEqual(newVersion, 'b')

    def testLocalePutBadJSON(self):
        ret = self._put('/releases/a/builds/p/l', data=dict(data='a', product='a', version='a'))
        self.assertStatusCode(ret, 400)

    def testLocaleRejectedURL(self):
        data = json.dumps(dict(complete=dict(fileUrl='http://evil.com')))
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', version='a', data_version=1))
        self.assertStatusCode(ret, 400)

    def testLocaleGet(self):
        ret = self._get('/releases/d/builds/p/d')
        self.assertStatusCode(ret, 200)
        self.assertEqual(json.loads(ret.data), dict(complete=dict(filesize='1234')))
        self.assertEqual(ret.headers['X-Data-Version'], '1')

    def testLocalePutNotAllowed(self):
        ret = self.client.put('/releases/d/builds/p/d', data=dict(product='a'))
        self.assertStatusCode(ret, 401)

    def testLocalePutCantChangeProduct(self):
        data = json.dumps(dict(complete=dict(filesize=435)))
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='b', version='a', schema_version=1))
        self.assertStatusCode(ret, 400)

    def testLocaleGet404(self):
        ret = self._get("/releases/c/builds/h/u")
        self.assertStatusCode(ret, 404)

    def testLocaleRevertsPartialUpdate(self):
        data = json.dumps(dict(complete=dict(filesize=1)))
        with mock.patch('auslib.global_state.dbo.releases.addLocaleToRelease') as r:
            r.side_effect = Exception("Fail")
            ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', version='c', data_version=1, schema_version=1))
            self.assertStatusCode(ret, 500)
            ret = dbo.releases.t.select().where(dbo.releases.name=='a').execute().fetchone()
            self.assertEqual(ret['product'], 'a')
            self.assertEqual(ret['version'], 'a')
            self.assertEqual(json.loads(ret['data']), dict(name='a', hashFunction="sha512", schema_version=1))

    def testNewReleasePut(self):
        ret = self._put('/releases/new_release', data=dict(name='new_release', version='11', product='Firefox',
                                                            blob="""
{
    "name": "a",
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
        r = dbo.releases.t.select().where(dbo.releases.name=='new_release').execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['name'], 'new_release')
        self.assertEquals(r[0]['version'], '11')
        self.assertEquals(r[0]['product'], 'Firefox')
        self.assertEquals(json.loads(r[0]['data']), json.loads("""
{
    "name": "a",
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
        ret = self._put("/releases/ueohueo", data=dict(name="ueohueo", version="1", product="aa", blob="""
{
    "name": "ueohueo",
    "schema_version": 3,
    "borken": "yes"
}
"""))
        self.assertStatusCode(ret, 400)

    def testPutExistingRelease(self):
        ret = self._put("/releases/d", data=dict(name="d", version="3", product="Firefox", data_version=1, blob="""
{
    "name": "d",
    "schema_version": 3,
    "hashFunction": "sha512",
    "actions": "doit"
}
"""))
        self.assertEquals(ret.status_code, 200, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = dbo.releases.t.select().where(dbo.releases.name=='d').execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['name'], 'd')
        self.assertEquals(r[0]['version'], '3')
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

        ret = self._put('/releases/gmprel', data=dict(name='gmprel', version='5', product='GMP',
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
        r = dbo.releases.t.select().where(dbo.releases.name=='gmprel').execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['name'], 'gmprel')
        self.assertEquals(r[0]['version'], '5')
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
        {"data_version": 1, "name": "a", "product": "a", "version": "a"},
        {"data_version": 1, "name": "ab", "product": "a", "version": "a"}
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

    def testGetReleasesNamePrefixNamesOnlyVersion(self):
        ret = self._get("/releases", qs=dict(name_prefix='a',
                                                 names_only='1',
                                                 version="b"))
        self.assertStatusCode(ret, 200)
        self.assertEquals(json.loads(ret.data), json.loads("""
{
    "names": []
}
"""))

    def testReleasesPost(self):
        data = json.dumps(dict(bouncerProducts=dict(linux='foo'), name='e', schema_version=1))
        ret = self._post('/releases', data=dict(blob=data, name="e", product='e', version='e'))
        self.assertStatusCode(ret, 201)
        ret = dbo.releases.t.select().where(dbo.releases.name=='e').execute().fetchone()
        self.assertEqual(ret['product'], 'e')
        self.assertEqual(ret['version'], 'e')
        self.assertEqual(ret['name'], 'e')
        self.assertEqual(json.loads(ret['data']), json.loads("""
{
    "name": "e",
    "schema_version": 1,
    "bouncerProducts": {
        "linux": "foo"
    }
}
"""))


class TestReleaseHistoryView(ViewTest, JSONTestMixin):
    def testGetRevisions(self):
        # Make some changes to a release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                version='222.0',
                data_version=1,
            )
        )
        self.assertStatusCode(ret, 200)

        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                version='333.0',
                data_version=3,
            )
        )
        self.assertStatusCode(ret, 200)

        url = '/releases/d/revisions'
        ret = self._get(url)
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        data = json.loads(ret.data)
        self.assertEquals(data["count"], 4)
        self.assertEquals(len(data["revisions"]), 4)

    def testPostRevisionRollback(self):
        # Make some changes to a release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True, schema_version=1))
        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                version='222.0',
                data_version=1,
            )
        )
        self.assertStatusCode(ret, 200)

        # XXX why does the data_version increment twice?
        data = json.dumps(dict(detailsUrl='blah', fakePartials=False, schema_version=1))
        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                version='333.0',
                data_version=3,
            )
        )
        self.assertStatusCode(ret, 200)

        table = dbo.releases
        row, = table.select(where=[table.name == 'd'])
        self.assertEqual(row['version'], '333.0')
        self.assertEqual(row['data_version'], 5)
        data = json.loads(row['data'])
        self.assertEqual(data['fakePartials'], False)

        query = table.history.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 2 * 2)

        # Oh no! We prefer the version 222.0
        row, = table.history.select(
            where=[table.history.version == '222.0'],
            limit=1
        )
        change_id = row['change_id']
        assert row['name'] == 'd'  # one of the fixtures

        url = '/releases/d/revisions'
        ret = self._post(url, {'change_id': change_id})
        self.assertEquals(ret.status_code, 200, ret.data)

        query = table.history.t.count()
        count, = query.execute().first()
        self.assertEqual(count, 2 * 2 + 1)

        row, = table.select(where=[table.name == 'd'])
        self.assertEqual(row['version'], '222.0')
        self.assertEqual(row['data_version'], 6)

    def testPostRevisionRollbackBadRequests(self):
        # when posting you need both the rule_id and the change_id
        ret = self._post('/releases/CRAZYNAME/revisions', {'change_id': 1})
        self.assertEquals(ret.status_code, 404)

        url = '/releases/d/revisions'
        ret = self._post(url, {'change_id': 999})
        self.assertEquals(ret.status_code, 404)

        ret = self._post(url)
        self.assertEquals(ret.status_code, 400)
