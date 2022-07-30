import json

from connexion import problem
from flask import Response

from auslib.global_state import dbo
from auslib.web.admin.views.base import handleGeneralExceptions, requirelogin, transactionHandler
from auslib.web.admin.views.scheduled_changes import EnactScheduledChangeView, ScheduledChangesView, ScheduledChangeView, SignoffsView


def get_emergency_shutoff(product, channel):
    where = dict(product=product, channel=channel)
    shutoffs = dbo.emergencyShutoffs.select(where=where)
    return shutoffs[0] if shutoffs else None


def shutoff_exists(product, channel):
    return bool(get_emergency_shutoff(product, channel))


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
def post(emergency_shutoff, changed_by, transaction):
    if shutoff_exists(emergency_shutoff["product"], emergency_shutoff["channel"]):
        return problem(400, "Bad Request", "Invalid Emergency shutoff data", ext={"exception": "Emergency shutoff for product/channel already exists."})
    inserted_shutoff = dbo.emergencyShutoffs.insert(
        changed_by=changed_by,
        transaction=transaction,
        product=emergency_shutoff["product"],
        channel=emergency_shutoff["channel"],
        comment=emergency_shutoff.get("comment"),
    )
    return Response(status=201, content_type="application/json", response=json.dumps(inserted_shutoff))


@requirelogin
@transactionHandler
@handleGeneralExceptions("DELETE")
def delete(product, channel, data_version, changed_by, transaction, **kwargs):
    if not shutoff_exists(product, channel):
        return problem(status=404, title="Not Found", detail="Shutoff wasn't found", ext={"exception": "Shutoff does not exist"})
    where = dict(product=product, channel=channel)
    dbo.emergencyShutoffs.delete(where=where, changed_by=changed_by, old_data_version=data_version, transaction=transaction)
    return Response(status=200)


def scheduled_changes():
    view = ScheduledChangesView("emergency_shutoff", dbo.emergencyShutoffs)
    return view.get()


@requirelogin
@transactionHandler
def schedule_deletion(sc_emergency_shutoff, changed_by, transaction):
    change_type = sc_emergency_shutoff.get("change_type")
    if change_type != "delete":
        return problem(400, "Bad Request", "Invalid or missing change_type")

    view = ScheduledChangesView("emergency_shutoff", dbo.emergencyShutoffs)
    return view._post(sc_emergency_shutoff, transaction, changed_by, change_type)


@requirelogin
@transactionHandler
def update_scheduled_deletion(sc_id, sc_emergency_shutoff, changed_by, transaction):
    view = ScheduledChangeView("emergency_shutoff", dbo.emergencyShutoffs)
    return view._post(sc_id, sc_emergency_shutoff, transaction, changed_by, sc_emergency_shutoff["sc_data_version"])


@requirelogin
@transactionHandler
def delete_scheduled_deletion(sc_id, changed_by, transaction, **kwargs):
    view = ScheduledChangeView("emergency_shutoff", dbo.emergencyShutoffs)
    return view._delete(sc_id, transaction, changed_by)


def scheduled_changes_signoffs(sc_id):
    view = SignoffsView("emergency_shutoff", dbo.emergencyShutoffs)
    return view.post(sc_id)


def scheduled_changes_signoffs_delete(sc_id):
    view = SignoffsView("emergency_shutoff", dbo.emergencyShutoffs)
    return view.delete(sc_id)


@requirelogin
def enact_updates_scheduled_for_reactivation(sc_id, changed_by):
    view = EnactScheduledChangeView("emergency_shutoff", dbo.emergencyShutoffs)
    return view.post(sc_id, changed_by=changed_by)
