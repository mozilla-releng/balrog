from auslib.web.admin.views.base import (
    requirelogin, handleGeneralExceptions, transactionHandler)
from flask import Response

def get():
    return 'ok'


def get_by_id(shutoff_id):
    return 'ok {}'.format(shutoff_id)


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
