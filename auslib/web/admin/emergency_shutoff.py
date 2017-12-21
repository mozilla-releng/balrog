import json
import time
from flask import Response
from connexion import problem
from auslib.global_state import dbo
from auslib.web.admin.views.base import (
    requirelogin, handleGeneralExceptions, transactionHandler)
from auslib.web.admin.views.scheduled_changes import (
    EnactScheduledChangeView, ScheduledChangesView, SignoffsView)


def get_emergency_shutoff(product, channel):
    where = dict(product=product, channel=channel)
    shutoffs = dbo.emergencyShutoffs.select(where=where)
    return shutoffs[0] if shutoffs else None


def shutoff_already_exists(product, channel):
    return bool(get_emergency_shutoff(product, channel))


def product_requires_signoffs(product):
    rs = dbo.productRequiredSignoffs.select(where=dict(product=product))
    return bool(rs)


def process_shutoff_post(emergency_shutoff):
    if 'csrf_token' in emergency_shutoff:
        del emergency_shutoff['csrf_token']
    if 'data_version' not in emergency_shutoff:
        emergency_shutoff['data_version'] = 1
    return emergency_shutoff


@requirelogin
@transactionHandler
@handleGeneralExceptions('POST')
def post(emergency_shutoff, changed_by, transaction):
    if shutoff_already_exists(emergency_shutoff['product'], emergency_shutoff['channel']):
        return problem(
            400, 'Bad Request', 'Invalid Emergency shutoff data',
            ext={'data': 'Emergency shutoff for product/channel already exists.'})
    if not product_requires_signoffs(emergency_shutoff['product']):
        return problem(
            400, 'Bad Request', 'Invalid Emergency shutoff data',
            ext={'data': 'The given product should requires signoffs.'})
    emergency_shutoff = process_shutoff_post(emergency_shutoff)
    dbo.emergencyShutoffs.insert(
        changed_by=changed_by, transaction=transaction, **emergency_shutoff)
    schedule_reenable_updates(emergency_shutoff, changed_by, transaction)
    return Response(status=201,
                    content_type="application/json",
                    response=json.dumps(emergency_shutoff))


@requirelogin
@transactionHandler
@handleGeneralExceptions('DELETE')
def delete(product, channel, data_version, changed_by, transaction, **kwargs):
    shutoff = get_emergency_shutoff(product, channel)
    if not shutoff:
        return problem(status=404,
                       title="Not Found",
                       detail="Shutoff wasn't found",
                       ext={"exception": "Shutoff does not exist"})
    where = dict(product=product, channel=channel)
    dbo.emergencyShutoffs.delete(where=where, changed_by=changed_by,
                                 old_data_version=data_version,
                                 transaction=transaction)
    return Response(status=200)


def get_asap_when():
    now = time.time()
    minutes = 5 * 60
    return int((now + minutes) * 1000)


def schedule_reenable_updates(shutoff, changed_by, transaction):
    what = dict(when=get_asap_when())
    what.update(shutoff)
    dbo.emergencyShutoffs.scheduled_changes.insert(
        changed_by, transaction, change_type='delete', **what)


def scheduled_changes():
    view = ScheduledChangesView('emergency_shutoff', dbo.emergencyShutoffs)
    return view.get()


def scheduled_changes_signoffs(sc_id):
    view = SignoffsView('emergency_shutoff', dbo.emergencyShutoffs)
    return view.post(sc_id)


def scheduled_changes_signoffs_delete(sc_id):
    view = SignoffsView('emergency_shutoff', dbo.emergencyShutoffs)
    return view.delete(sc_id)


@requirelogin
def enact_updates_scheduled_for_reactivation(sc_id, changed_by):
    view = EnactScheduledChangeView('emergency_shutoff', dbo.emergencyShutoffs)
    return view.post(sc_id, changed_by=changed_by)
