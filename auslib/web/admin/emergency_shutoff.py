from flask import jsonify, Response
from connexion import problem
from auslib.global_state import dbo
from auslib.web.admin.views.base import (
    requirelogin, handleGeneralExceptions, transactionHandler)


json_mimetype = 'application/json'


def get_filter(**columns):
    where = {column: value for column, value in columns.iteritems() if value}
    return where


def get(product=None, channel=None):
    where = get_filter(product=product, channel=channel)
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


def validate_shutoff(emergency_shutoff):
    validation_messages = []
    required_fields = ['product', 'channel']
    for required_field in required_fields:
        if required_field not in emergency_shutoff or not emergency_shutoff[required_field]:
            validation_messages.append('{} is required.'.format(required_field.capitalize()))
    return len(validation_messages) == 0, validation_messages


@requirelogin
@transactionHandler
@handleGeneralExceptions('POST')
def post(emergency_shutoff, changed_by, transaction):
    is_valid, validation_messages = validate_shutoff(emergency_shutoff)
    if not is_valid:
        return problem(
            400, 'Bad Request', 'Invalid Emergency shutoff data', ext={'data': validation_messages})

    where = get_filter(product=emergency_shutoff['product'], channel=emergency_shutoff['channel'])
    shutoffs = dbo.emergencyShutoff.getEmergencyShutoffs(where)
    if shutoffs:
        return problem(400, 'Bad Request',
                       'Emergency shutoff for product/channel already exists.',
                       ext={'data': validation_messages})
    shutoff = dbo.emergencyShutoff.insert(
        changed_by=changed_by, transaction=transaction, **emergency_shutoff)
    return Response(status=200, response=str(shutoff))


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
