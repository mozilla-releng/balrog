import time
from flask import jsonify, Response
from connexion import problem
from auslib.global_state import dbo
from auslib.web.admin.views.base import (
    requirelogin, handleGeneralExceptions, transactionHandler)
from auslib.web.admin.views.scheduled_changes import EnactScheduledChangeView, ScheduledChangesView


def shutoff_already_exists(emergency_shutoff):
    shutoffs = query_shutoffs(product=emergency_shutoff['product'], channel=emergency_shutoff['channel'])
    return bool(shutoffs)


def can_updating_product_or_channel(emergency_shutoff, emergency_shutoff_db):
    if emergency_shutoff['product'] != emergency_shutoff_db['product'] or emergency_shutoff['channel'] != emergency_shutoff_db['channel']:
        return not shutoff_already_exists(emergency_shutoff)
    return True


def get_columns_dict(include_nulls=False, **columns):
    cols = {}
    for column, value in columns.iteritems():
        if not value and not include_nulls:
            continue
        cols[column] = value
    return cols


def query_shutoffs(**columns):
    where = get_columns_dict(**columns)
    return dbo.emergencyShutoff.getEmergencyShutoffs(where)


def get(product=None, channel=None):
    shutoffs = query_shutoffs(product=product, channel=channel)
    shutoffs_count = len(shutoffs)
    return jsonify(count=shutoffs_count, shutoffs=shutoffs)


def get_by_id(shutoff_id):
    shutoff = dbo.emergencyShutoff.getEmergencyShutoff(shutoff_id)
    if not shutoff:
        return problem(status=404,
                       title="Not Found",
                       detail="Requested emergency shutoff wasn't found",
                       ext={"exception": "Requested shutoff does not exist"})
    return jsonify(shutoff)


@requirelogin
@transactionHandler
@handleGeneralExceptions('POST')
def post(emergency_shutoff, changed_by, transaction):
    if shutoff_already_exists(emergency_shutoff):
        return problem(
            400, 'Bad Request', 'Invalid Emergency shutoff data',
            ext={'data': 'Emergency shutoff for product/channel already exists.'})
    shutoff = dbo.emergencyShutoff.insert(
        changed_by=changed_by, transaction=transaction, **emergency_shutoff)
    return Response(status=201, response=str(shutoff))


@requirelogin
@transactionHandler
@handleGeneralExceptions('PUT')
def put(shutoff_id, emergency_shutoff, changed_by, transaction):
    shutoff = dbo.emergencyShutoff.getEmergencyShutoff(shutoff_id)
    if not shutoff:
        return problem(status=404,
                       title="Not Found",
                       detail="Shutoff wasn't found",
                       ext={"exception": "Shutoff does not exist"})
    if not can_updating_product_or_channel(emergency_shutoff, shutoff):
        return problem(
            400, 'Bad Request', 'Invalid Emergency shutoff data',
            ext={'data': 'Emergency shutoff for product/channel already exists.'})
    where = get_columns_dict(shutoff_id=shutoff_id)
    what = get_columns_dict(**emergency_shutoff)
    dbo.emergencyShutoff.update(
        where=where, what=what, old_data_version=shutoff['data_version'],
        changed_by=changed_by, transaction=transaction)
    return Response(status=200)


@requirelogin
@transactionHandler
@handleGeneralExceptions('DELETE')
def delete(shutoff_id, changed_by, transaction):
    return Response(response='OK {} {}'.format(shutoff_id, changed_by))


def get_asap_when():
    now = time.time()
    minutes = 5 * 60
    return int((now + minutes) * 1000)


def schedule_reenable_updates(shutoff, changed_by, transaction):
    what = get_columns_dict(when=get_asap_when())
    shutoff['data_version'] += 1
    what.update(shutoff)
    dbo.emergencyShutoff.scheduled_changes.insert(
        changed_by, transaction, change_type='update', **what)


@requirelogin
@transactionHandler
@handleGeneralExceptions('PUT')
def disable_updates(shutoff_id, changed_by, transaction):
    shutoff = dbo.emergencyShutoff.getEmergencyShutoff(shutoff_id)
    if not shutoff:
        return problem(status=404,
                       title="Not Found",
                       detail="Shutoff wasn't found",
                       ext={"exception": "Shutoff does not exist"})
    if shutoff['updates_disabled']:
        return problem(
            400, 'Bad Request', 'Invalid request for disabling updates',
            ext={'data': 'Updates already disabled'})
    where = get_columns_dict(shutoff_id=shutoff_id)
    what = get_columns_dict(updates_disabled=True)
    data_version = shutoff['data_version']
    dbo.emergencyShutoff.update(where=where, what=what,
                                old_data_version=data_version,
                                changed_by=changed_by, transaction=transaction)
    schedule_reenable_updates(shutoff, changed_by, transaction)
    return Response(status=200)


def scheduled_changes():
    view = ScheduledChangesView('emergency_shutoff', dbo.emergencyShutoff)
    return view.get()


@requirelogin
def enact_updates_scheduled_for_reactivation(sc_id, changed_by):
    view = EnactScheduledChangeView('emergency_shutoff', dbo.emergencyShutoff)
    return view.post(sc_id, changed_by=changed_by)
