import mock
import simplejson as json

from sqlalchemy import select

from auslib.web.base import db
from auslib.test.web.views.base import ViewTest, JSONTestMixin, HTMLTestMixin

class TestReleasesAPI_JSON(ViewTest, JSONTestMixin):
    def testLocalePut(self):
        details = json.dumps(dict(complete=dict(filesize=435)))
        ret = self._put('/releases/a/builds/p/l', data=dict(details=details, product='a', version='a'))
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
                        "filesize": 435
                    }
                }
            }
        }
    }
}
"""))

    def testLocalePutForNewRelease(self):
        details = json.dumps(dict(complete=dict(filesize=678)))
        ret = self._put('/releases/e/builds/p/a', data=dict(details=details, product='e', version='e'))
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
                        "filesize": 678
                    }
                }
            }
        }
    }
}
"""))

    def testLocalePutAppend(self):
        details = json.dumps(dict(partial=dict(fileUrl='abc')))
        ret = self._put('/releases/d/builds/p/g', data=dict(details=details, product='d', version='d'))
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
                        "filesize": 1234
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

    def testLocalePutWithCopy(self):
        details = json.dumps(dict(partial=dict(filesize=123)))
        data = dict(details=details, product='a', version='a', copyTo=json.dumps(['ab']))
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
                        "filesize": 123
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
                        "filesize": 123
                    }
                }
            }
        }
    }
}
"""))

    def testLocalePutChangeVersion(self):
        ret = self._put('/releases/a/builds/p/l', data=dict(details="{}", product='a', version='b'))
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
                }
            }
        }
    }
}
"""))
        newVersion = select([db.releases.version]).where(db.releases.name=='a').execute().fetchone()[0]
        self.assertEqual(newVersion, 'b')

    def testLocalePutRetry(self):
        # In order to test the retry logic we need to mock out the method used
        # to grab the current data_version. The first time through, it needs
        # to return the wrong one to trigger the retry logic. The second time
        # through it needs to return the correct one, to make sure retrying
        # results in success still.
        with mock.patch('auslib.web.base.db.releases.getReleases') as r:
            results = [[dict(data_version=2, product='a', version='a')], [dict(data_version=1, product='a', version='a')], [dict(data_version=431, product='a', version='a')]]
            def se(*args, **kwargs):
                print results
                return results.pop()
            r.side_effect = se
            details = json.dumps(dict(complete=dict(filesize=435)))
            ret = self._put('/releases/a/builds/p/l', data=dict(details=details, product='a', version='a'))
            self.assertStatusCode(ret, 201)
            # getReleases gets called once when it returns the wrong data_version, once with the right one
            # and then once again at the end, when the new data version is retrieved
            self.assertEqual(r.call_count, 3)
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
                        "filesize": 435
                    }
                }
            }
        }
    }
}
"""))

    def testLocalePutBadJSON(self):
        ret = self._put('/releases/a/builds/p/l', data=dict(details='a', product='a', version='a'))
        self.assertStatusCode(ret, 400)

    def testLocaleGet(self):
        ret = self._get('/releases/d/builds/p/d')
        self.assertStatusCode(ret, 200)
        self.assertEqual(json.loads(ret.data), dict(complete=dict(filesize=1234)))

    def testLocalePutNotAllowed(self):
        ret = self.client.put('/releases/d/builds/p/d', data=dict(product='a'))
        self.assertStatusCode(ret, 401)

    def testLocalePutCantChangeProduct(self):
        details = json.dumps(dict(complete=dict(filesize=435)))
        ret = self._put('/releases/a/builds/p/l', data=dict(details=details, product='b', version='a'))
        self.assertStatusCode(ret, 400)

    def testLocaleRevertsPartialUpdate(self):
        details = json.dumps(dict(complete=dict(filesize=1)))
        with mock.patch('auslib.web.base.db.releases.addLocaleToRelease') as r:
            r.side_effect = Exception("Fail")
            ret = self._put('/releases/a/builds/p/l', data=dict(details=details, product='a', version='c'))
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
                        "filesize": 1234
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
        self.assertTrue('<table id="Releases_table">' in ret.data, msg=ret.data)

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

