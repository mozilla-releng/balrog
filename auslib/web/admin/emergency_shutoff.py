from flask import jsonify, Response
from connexion import problem
from auslib.global_state import dbo
from auslib.web.admin.views.base import (
    requirelogin, handleGeneralExceptions, transactionHandler)


json_mimetype = 'application/json'


def get(product=None, channel=None):
    where = {}
    if product:
        where['product'] = product
    if channel:
        where['channel'] = channel
    shutoffs = dbo.emergencyShutoff.getEmergencyShutoffs(where)
    shutoffs_count = len(shutoffs)
    return jsonify(count=shutoffs_count, shutoffs=shutoffs)


def get_by_id(shutoff_id):
    shutoff = dbo.emergencyShutoff.getEmergencyShutoff(shutoff_id)
    if not shutoff:
        return problem(status=404,
                       title="Not Found",
                       detail="Requested emergency shutoff wasn't found",
                       ext={"exception": "Requested rule does not exist"})
    return jsonify(shutoff)


@requirelogin
@transactionHandler
@handleGeneralExceptions('POST')
def post(emergency_shutoff, changed_by, transaction):
    return Response(response='OK {} {} {}'.format(changed_by, emergency_shutoff['product'], emergency_shutoff['channel']))


@requirelogin
@transactionHandler
@handleGeneralExceptions('PUT')
def put(shutoff_id, emergency_shutoff, changed_by, transaction):
    return Response(response='OK {} {} {} {}'.format(shutoff_id, changed_by, emergency_shutoff['product'], emergency_shutoff['channel']))


@requirelogin
@transactionHandler
@handleGeneralExceptions('DELETE')
def delete(shutoff_id, changed_by, transaction):
    return Response(response='OK {} {}'.format(shutoff_id, changed_by))


@requirelogin
@transactionHandler
@handleGeneralExceptions('PUT')
def disable_updates(shutoff_id, changed_by, transaction):
    return Response(response='OK {} {}'.format(shutoff_id, changed_by))


def scheduled_changes():
    return 'OK'


@requirelogin
@transactionHandler
@handleGeneralExceptions('POST')
def enact_updates_scheduled_for_reactivation(sc_id, changed_by, transaction):
    return Response(response='OK {} {}'.format(sc_id, changed_by))
