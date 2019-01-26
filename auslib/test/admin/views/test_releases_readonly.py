from auslib.global_state import dbo
from auslib.test.admin.views.base import ViewTest
from auslib.blobs.base import createBlob


class TestReleasesReadOnly(ViewTest):
    def setUp(self):
        super(TestReleasesReadOnly, self).setUp()
        dbo.productRequiredSignoffs.t.insert().execute(
            product="K", channel="Z", role="releng", signoffs_required=1, data_version=1)
        dbo.productRequiredSignoffs.t.insert().execute(
            product="K", channel="Z", role="relman", signoffs_required=1, data_version=1)
        dbo.releases.t.insert().execute(
            name='K', product='K', data_version=1,
            data=createBlob(dict(name='a', hashFunction="sha512", schema_version=1)))
        dbo.rules.t.insert().execute(
            rule_id=42000042, product='K', priority=25, backgroundRate=100,
            mapping='K', update_type='minor', channel="Z", data_version=1)
        dbo.releasesReadonly.t.insert().execute(
            {'release_name': 'K', 'data_version': 1})
        dbo.releasesReadonly.scheduled_changes.t.insert().execute(
            sc_id=1, scheduled_by='bill', change_type='delete',
            data_version=1, base_release_name='K', base_data_version=1)
        dbo.releasesReadonly.scheduled_changes.conditions.t.insert().execute(
            sc_id=1, data_version=1, when=1000000)

    def test_set_readonly(self):
        release_name = 'a'
        resp = self._post('/releases_readonly/{}'.format(release_name))
        self.assertStatusCode(resp, 201)
        release_readonly = dbo.releasesReadonly.select(where={'release_name': release_name})
        self.assertTrue(release_readonly)
        self.assertEqual(release_readonly[0]['release_name'], release_name)

    def test_already_readonly(self):
        release_name = 'a'
        dbo.releasesReadonly.t.insert().execute(
            {'release_name': release_name, 'data_version': 1})
        resp = self._post('/releases_readonly/{}'.format(release_name))
        self.assertStatusCode(resp, 400)

    def test_set_readonly_release_does_not_exists(self):
        release_name = 'a42'
        resp = self._post('/releases_readonly/{}'.format(release_name))
        self.assertStatusCode(resp, 400)

    def test_set_readonly_no_permission(self):
        release_name = 'a'
        resp = self._post('/releases_readonly/{}'.format(release_name), username='julie')
        self.assertStatusCode(resp, 403)

    def test_set_read_write(self):
        release_name = 'c'
        dbo.releasesReadonly.t.insert().execute({'release_name': release_name, 'data_version': 1})
        resp = self._delete(
            '/releases_readonly/{}'.format(release_name),
            qs={'data_version': 1})
        self.assertStatusCode(resp, 200)
        release_readonly = dbo.releasesReadonly.select(where={'release_name': release_name})
        self.assertFalse(release_readonly)

    def test_set_read_write_when_not_readonly(self):
        release_name = 'a'
        resp = self._delete('/releases_readonly/{}'.format(release_name), qs={'data_version': 1})
        self.assertStatusCode(resp, 400)

    def test_set_read_write_no_permission(self):
        release_name = 'c'
        dbo.releasesReadonly.t.insert().execute({'release_name': release_name, 'data_version': 1})
        resp = self._delete(
            '/releases_readonly/{}'.format(release_name),
            qs={'data_version': 1},
            username='julie')
        self.assertStatusCode(resp, 403)
        release_readonly = dbo.releasesReadonly.select(where={'release_name': release_name})
        self.assertTrue(release_readonly)

    def test_get_scheduled_changes_read_write(self):
        resp = self._get('/scheduled_changes/releases_readonly')
        self.assertStatusCode(resp, 200)
        data = resp.get_json()
        self.assertEqual(data['count'], 1)
        scheduled_change = data['scheduled_changes'][0]
        self.assertIn('relman', scheduled_change['required_signoffs'])
        self.assertIn('releng', scheduled_change['required_signoffs'])

    def test_schedule_read_write(self):
        release_name = 'a'
        dbo.releasesReadonly.t.insert().execute(
            {'release_name': release_name, 'data_version': 1})
        data = {
            'release_name': release_name,
            'data_version': 1,
            'change_type': 'delete'
        }
        resp = self._post('/scheduled_changes/releases_readonly', data=data)
        self.assertStatusCode(resp, 200)

        sc = dbo.releasesReadonly.scheduled_changes.select(where={'base_release_name': release_name})
        self.assertTrue(sc)

    def test_delete_scheduled_read_write(self):
        resp = self._delete(
            '/scheduled_changes/releases_readonly/1', qs={'data_version': 1})
        self.assertStatusCode(resp, 200)
        sc_table = dbo.releasesReadonly.scheduled_changes
        sc = sc_table.t.select().where(sc_table.sc_id == 1).execute().fetchall()
        self.assertFalse(sc)

    def test_enact_change_read_write(self):
        signoffs_table = dbo.releasesReadonly.scheduled_changes.signoffs
        signoffs_table.t.insert().execute(sc_id=1, username="julie", role="releng")
        signoffs_table.t.insert().execute(sc_id=1, username="mary", role="relman")

        resp = self._post('/scheduled_changes/releases_readonly/1/enact')
        self.assertStatusCode(resp, 200)
        releases_readonly = dbo.releasesReadonly.select(where={'release_name': 'K'})
        self.assertFalse(releases_readonly)

    def test_enact_change_insufficient_signoffs(self):
        resp = self._post('/scheduled_changes/releases_readonly/1/enact')
        self.assertStatusCode(resp, 400)
        releases_readonly = dbo.releasesReadonly.select(where={'release_name': 'K'})
        self.assertTrue(releases_readonly)

    def test_signoff(self):
        sc_id = 1
        data = {
            'username': 'julie',
            'role': 'releng'
        }
        resp = self._post(
            '/scheduled_changes/releases_readonly/{}/signoffs'.format(sc_id),
            data=data, username='julie')
        self.assertStatusCode(resp, 200)
        signoffs = dbo.releasesReadonly.scheduled_changes.signoffs.select(
            where={'sc_id': sc_id, 'username': 'julie', 'role': 'releng'})
        self.assertTrue(signoffs)

    def test_remove_signoff(self):
        sc_id = 1
        qs = {'username': 'julie'}
        dbo.releasesReadonly.scheduled_changes.signoffs.t.insert().execute(
            sc_id=sc_id, username='julie', role='releng')
        resp = self._delete(
            '/scheduled_changes/releases_readonly/{}/signoffs'.format(sc_id),
            qs=qs, username='julie')
        self.assertStatusCode(resp, 200)
        sc = dbo.releasesReadonly.scheduled_changes.signoffs.select(
            where={'sc_id': sc_id})
        self.assertFalse(sc)
