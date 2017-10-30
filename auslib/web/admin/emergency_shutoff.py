import time
from flask import jsonify, Response
from connexion import problem
from jsonschema.compat import str_types
from auslib.global_state import dbo
from auslib.web.admin.views.base import (
    requirelogin, handleGeneralExceptions, transactionHandler)
from scheduled_changes import EnactScheduledChangeView, ScheduledChangesView


def shutoff_already_exists(emergency_shutoff):
    shutoffs = query_shutoffs(product=emergency_shutoff['product'], channel=emergency_shutoff['channel'])
    return bool(shutoffs)


def can_updating_product_or_channel(emergency_shutoff, emergency_shutoff_db):
    if emergency_shutoff['product'] != emergency_shutoff_db['product'] or emergency_shutoff['channel'] != emergency_shutoff_db['channel']:
        return not shutoff_already_exists(emergency_shutoff)
    return True


def get_columns_dict(**columns):
    where = {}
    for column, value in columns.iteritems():
        if isinstance(value, str_types) and not value:
            continue
        where[column] = value
    return where


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
        where=where, what=what, changed_by=changed_by, transaction=transaction)
    return Response(status=200)


@requirelogin
@transactionHandler
@handleGeneralExceptions('DELETE')
def delete(shutoff_id, changed_by, transaction):
    return Response(response='OK {} {}'.format(shutoff_id, changed_by))


def schedule_reenable_updates(shutoff_id, changed_by, transaction):
    asap_schedule = int(time.time() * 1000)
    what = get_columns_dict(updates_disabled=False, when=asap_schedule)
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
    if shutoff.updates_disabled:
        return problem(
            400, 'Bad Request', 'Invalid request for disabling updates',
            ext={'data': 'Updates already disabled'})
    where = get_columns_dict(shutoff_id=shutoff_id)
    what = get_columns_dict(updates_disabled=True)
    dbo.emergencyShutoff.update(
        where=where, what=what, changed_by=changed_by, transaction=transaction)
    schedule_reenable_updates(shutoff_id, changed_by, transaction)
    return Response(status=200)


def scheduled_changes():
    view = ScheduledChangesView('emergency_shutoff', dbo.emergencyShutoff)
    return view.get()


def enact_updates_scheduled_for_reactivation(sc_id, changed_by):
    view = EnactScheduledChangeView('emergency_shutoff', dbo.emergencyShutoff)
    return view.post(sc_id)
