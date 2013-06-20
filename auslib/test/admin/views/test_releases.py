import mock
import simplejson as json

from sqlalchemy import select

from auslib.admin.base import db
from auslib.test.admin.views.base import ViewTest, JSONTestMixin, HTMLTestMixin

class TestReleasesAPI_JSON(ViewTest, JSONTestMixin):
    def testReleasePost(self):
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True))
        ret = self._post('/releases/d', data=dict(data=data, product='d', version='d', data_version=1))
        self.assertStatusCode(ret, 200)
        ret = select([db.releases.data]).where(db.releases.name=='d').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "d",
    "detailsUrl": "blah",
    "fakePartials": true,
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

    def testReleasePostCreatesNewRelease(self):
        data = json.dumps(dict(bouncerProducts=dict(linux='foo'), name='e'))
        ret = self._post('/releases/e', data=dict(data=data, product='e', version='e'))
        self.assertStatusCode(ret, 201)
        ret = db.releases.t.select().where(db.releases.name=='e').execute().fetchone()
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

    def testReleasePostInvalidKey(self):
        data = json.dumps(dict(foo=1))
        ret = self._post('/releases/a', data=dict(data=data))
        self.assertStatusCode(ret, 400)

    def testLocalePut(self):
        data = json.dumps(dict(complete=dict(filesize='435')))
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', version='a', data_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([db.releases.data]).where(db.releases.name=='a').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "a",
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

    def testLocalePutForNewRelease(self):
        data = json.dumps(dict(complete=dict(filesize='678')))
        ret = self._put('/releases/e/builds/p/a', data=dict(data=data, product='e', version='e'))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([db.releases.data]).where(db.releases.name=='e').execute().fetchone()[0]
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
        }
    }
}
"""))

    def testLocalePutAppend(self):
        data = json.dumps(dict(partial=dict(fileUrl='abc')))
        ret = self._put('/releases/d/builds/p/g', data=dict(data=data, product='d', version='d', data_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([db.releases.data]).where(db.releases.name=='d').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "d",
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
                        "fileUrl": "abc"
                    }
                }
            }
        }
    }
}
"""))

    def testLocalePutForNewReleaseWithAlias(self):
        data = json.dumps(dict(complete=dict(filesize='678')))
        ret = self._put('/releases/e/builds/p/a', data=dict(data=data, product='e', version='e', alias='["p2"]'))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([db.releases.data]).where(db.releases.name=='e').execute().fetchone()[0]
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
        data = json.dumps(dict(partial=dict(fileUrl='abc')))
        ret = self._put('/releases/d/builds/q/g', data=dict(data=data, product='d', version='d', data_version=1, alias='["q2"]'))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([db.releases.data]).where(db.releases.name=='d').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "d",
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
                        "fileUrl": "abc"
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
        data = dict(data=data, product='a', version='a', copyTo=json.dumps(['ab']), data_version=1)
        ret = self._put('/releases/a/builds/p/l', data=data)
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=2)), "Data: %s" % ret.data)
        ret = select([db.releases.data]).where(db.releases.name=='a').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "a",
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
        ret = select([db.releases.data]).where(db.releases.name=='ab').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "ab",
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
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', version='b', data_version=1))
        self.assertStatusCode(ret, 201)
        self.assertEqual(ret.data, json.dumps(dict(new_data_version=3)), "Data: %s" % ret.data)
        ret = select([db.releases.data]).where(db.releases.name=='a').execute().fetchone()[0]
        self.assertEqual(json.loads(ret), json.loads("""
{
    "name": "a",
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
        newVersion = select([db.releases.version]).where(db.releases.name=='a').execute().fetchone()[0]
        self.assertEqual(newVersion, 'b')

    def testLocalePutBadJSON(self):
        ret = self._put('/releases/a/builds/p/l', data=dict(data='a', product='a', version='a'))
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
        ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='b', version='a'))
        self.assertStatusCode(ret, 400)

    def testLocaleRevertsPartialUpdate(self):
        data = json.dumps(dict(complete=dict(filesize=1)))
        with mock.patch('auslib.admin.base.db.releases.addLocaleToRelease') as r:
            r.side_effect = Exception("Fail")
            ret = self._put('/releases/a/builds/p/l', data=dict(data=data, product='a', version='c', data_version=1))
            self.assertStatusCode(ret, 500)
            ret = db.releases.t.select().where(db.releases.name=='a').execute().fetchone()
            self.assertEqual(ret['product'], 'a')
            self.assertEqual(ret['version'], 'a')
            self.assertEqual(json.loads(ret['data']), dict(name='a'))

    # Test get of a release's full data column, queried by name
    def testGetSingleReleaseBlob(self):
        ret = self._get("/releases/d/data")
        self.assertStatusCode(ret, 200)
        self.assertEqual(json.loads(ret.data), json.loads("""
{
    "name": "d",
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
"""), msg=ret.data)


class TestReleasesAPI_HTML(ViewTest, HTMLTestMixin):

    def testGetReleases(self):
        ret = self._get("/releases.html")
        self.assertStatusCode(ret, 200)
        self.assertTrue('<table id="Releases_table"' in ret.data, msg=ret.data)

    # Test get of a release's full data column, queried by name
    def testGetSingleRelease(self):
        ret = self._get("/releases/d")
        self.assertStatusCode(ret, 200)
        self.assertTrue("<td> <a href='releases/d/data'>link</a></td>" in ret.data, msg=ret.data)

    def testNewReleasePut(self):

        ret = self._put('/releases/new_release', data=dict(name='new_release', version='11', product='Firefox',
                                                            blob="""
{
    "name": "a",
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

                                                        #json.dumps(newReleaseFile.getvalue())))
        self.assertEquals(ret.status_code, 201, "Status Code: %d, Data: %s" % (ret.status_code, ret.data))
        r = db.releases.t.select().where(db.releases.name=='new_release').execute().fetchall()
        self.assertEquals(len(r), 1)
        self.assertEquals(r[0]['name'], 'new_release')
        self.assertEquals(r[0]['version'], '11')
        self.assertEquals(r[0]['product'], 'Firefox')
        self.assertEquals(json.loads(r[0]['data']), json.loads("""
{
    "name": "a",
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


class TestReleaseHistoryView(ViewTest, HTMLTestMixin):
    def testGetNoRevisions(self):
        url = '/releases/a/revisions/'
        ret = self._get(url)
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        self.assertTrue('There were no previous revisions' in ret.data)

    def testGetRevisions(self):
        # Make some changes to a release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True))
        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                version='222.0',
                data_version=1
            )
        )
        self.assertStatusCode(ret, 200)

        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                version='333.0',
                data_version=3
            )
        )
        self.assertStatusCode(ret, 200)

        url = '/releases/d/revisions/'
        ret = self._get(url)
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        self.assertTrue('There were no previous revisions' not in ret.data)
        self.assertTrue('222.0' in ret.data)
        self.assertTrue('333.0' in ret.data)

    def testPostRevisionRollback(self):
        # Make some changes to a release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True))
        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                version='222.0',
                data_version=1
            )
        )
        self.assertStatusCode(ret, 200)

        # XXX why does the data_version increment twice?
        data = json.dumps(dict(detailsUrl='blah', fakePartials=False))
        ret = self._post(
            '/releases/d',
            data=dict(
                data=data,
                product='d',
                version='333.0',
                data_version=3
            )
        )
        self.assertStatusCode(ret, 200)

        table = db.releases
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

        url = '/releases/d/revisions/'
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
        ret = self._post('/releases/CRAZYNAME/revisions/', {'change_id': 1})
        self.assertEquals(ret.status_code, 404)

        url = '/releases/d/revisions/'
        ret = self._post(url, {'change_id': 999})
        self.assertEquals(ret.status_code, 404)

        ret = self._post(url)
        self.assertEquals(ret.status_code, 400)

    def testGetRevisionsWithPagination(self):
        # Make some changes to a release
        data = json.dumps(dict(detailsUrl='blah', fakePartials=True))
        for i in range(0, 33, 2):  # any largish number
            ret = self._post(
                '/releases/d',
                data=dict(
                    data=data,
                    product='d',
                    version='%d.0' % i,
                    data_version=1 + i
                )
            )
            self.assertStatusCode(ret, 200)

        url = '/releases/d/revisions/'
        ret = self._get(url)
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        self.assertTrue('There were no previous revisions' not in ret.data)
        self.assertTrue('?page=2' in ret.data)

        ret2 = self._get(url + '?page=2')
        self.assertEquals(ret.status_code, 200, msg=ret.data)
        self.assertTrue(ret.data != ret2.data)
