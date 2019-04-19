import json
import time

from connexion import problem
from flask import Response

from auslib.global_state import dbo
from auslib.web.admin.views.base import (
    requirelogin, handleGeneralExceptions, transactionHandler)

from auslib.web.admin.views.scheduled_changes import (
    EnactScheduledChangeView, ScheduledChangeView, ScheduledChangesView, SignoffsView)


@handleGeneralExceptions('GET')
def get(release):
    where = dict(release_name=release)
    releases_read_only = dbo.releasesReadonly.select(where=where)

    if not releases_read_only:
        return problem(
            status=404, title="Not Found",
            detail="Release readonly not found.",
            ext={"exception": "Release readonly not found."})

    release_read_only = releases_read_only[0]
    headers = {'X-Data-Version': release_read_only['data_version']}

    return Response(
        response=json.dumps(release_read_only),
        headers=headers,
        mimetype='application/json')


@requirelogin
@transactionHandler
@handleGeneralExceptions('POST')
def post(release, changed_by, transaction):
    if dbo.releasesReadonly.is_readonly(release):
        return problem(
            400, 'Bad Request', 'Releases Readonly',
            ext={'data': 'Release is already in readonly state.'})

    if not dbo.releasesReadonly.get_release_info(release, transaction=transaction):
        return problem(
            400, 'Bad Request', 'Releases Readonly',
            ext={'data': 'Release {} does not exists.'.format(release)})

    dbo.releasesReadonly.insert(
        changed_by, transaction=transaction, release_name=release)

    return Response(status=201)


@requirelogin
@transactionHandler
@handleGeneralExceptions('DELETE')
def delete(release, data_version, changed_by, transaction, **kwargs):
    if not dbo.releasesReadonly.is_readonly(release):
        return problem(
            400, 'Bad Request', 'Releases Readonly',
            ext={'data': 'Release is not in readonly state.'})
    where = {'release_name': release}
    dbo.releasesReadonly.delete(where, changed_by, data_version)
    return Response(status=200)


def scheduled_changes():
    view = ScheduledChangesView('releases_readonly', dbo.releasesReadonly)
    return view.get()


@requirelogin
@transactionHandler
def schedule_release_read_write(sc_release_readonly, changed_by, transaction):
    if 'csrf_token' in sc_release_readonly:
        del sc_release_readonly['csrf_token']

    change_type = sc_release_readonly.get('change_type')
    if change_type != 'delete':
        return problem(400, "Bad Request", "Invalid or missing change_type")

    sc_release_readonly['when'] = (time.time() + 360) * 1000
    view = ScheduledChangesView('releases_readonly', dbo.releasesReadonly)
    return view._post(sc_release_readonly, transaction, changed_by, change_type)


@requirelogin
@transactionHandler
def delete_scheduled_release_read_write(sc_id, changed_by, transaction, **kwargs):
    view = ScheduledChangeView('releases_readonly', dbo.releasesReadonly)
    return view._delete(sc_id, transaction, changed_by)


def scheduled_changes_signoffs(sc_id):
    view = SignoffsView('releases_readonly', dbo.releasesReadonly)
    return view.post(sc_id)


def scheduled_changes_signoffs_delete(sc_id):
    view = SignoffsView('releases_readonly', dbo.releasesReadonly)
    return view.delete(sc_id)


@requirelogin
def enact_release_read_write(sc_id, changed_by):
    view = EnactScheduledChangeView('releases_readonly', dbo.releasesReadonly)
    return view.post(sc_id, changed_by=changed_by)
