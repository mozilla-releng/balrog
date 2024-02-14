import json

from connexion import problem
from flask import Response

from auslib.global_state import dbo
from auslib.web.admin.views.base import handleGeneralExceptions, requirelogin, transactionHandler
from auslib.web.admin.views.scheduled_changes import (
    delete_scheduled_change,
    delete_signoffs_scheduled_change,
    get_scheduled_changes,
    post_enact_scheduled_change,
    post_scheduled_change,
    post_scheduled_changes,
    post_signoffs_scheduled_change,
)


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
    return get_scheduled_changes(table=dbo.emergencyShutoffs)


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
def schedule_deletion(sc_emergency_shutoff, changed_by, transaction):
    change_type = sc_emergency_shutoff.get("change_type")
    if change_type != "delete":
        return problem(400, "Bad Request", "Invalid or missing change_type")

    return post_scheduled_changes(
        sc_table=dbo.emergencyShutoffs.scheduled_changes, what=sc_emergency_shutoff, transaction=transaction, changed_by=changed_by, change_type=change_type
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
def update_scheduled_deletion(sc_id, sc_emergency_shutoff, changed_by, transaction):
    return post_scheduled_change(
        sc_table=dbo.emergencyShutoffs.scheduled_changes,
        sc_id=sc_id,
        what=sc_emergency_shutoff,
        transaction=transaction,
        changed_by=changed_by,
        old_sc_data_version=sc_emergency_shutoff["sc_data_version"],
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("DELETE")
def delete_scheduled_deletion(sc_id, data_version, changed_by, transaction):
    return delete_scheduled_change(
        sc_table=dbo.emergencyShutoffs.scheduled_changes, sc_id=sc_id, data_version=data_version, transaction=transaction, changed_by=changed_by
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
def scheduled_changes_signoffs(sc_id, transaction, changed_by):
    return post_signoffs_scheduled_change(
        signoffs_table=dbo.emergencyShutoffs.scheduled_changes.signoffs, sc_id=sc_id, transaction=transaction, changed_by=changed_by
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("DELETE")
def scheduled_changes_signoffs_delete(sc_id, transaction, changed_by):
    return delete_signoffs_scheduled_change(
        signoffs_table=dbo.emergencyShutoffs.scheduled_changes.signoffs, sc_id=sc_id, transaction=transaction, changed_by=changed_by
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
def enact_updates_scheduled_for_reactivation(sc_id, transaction, changed_by):
    return post_enact_scheduled_change(sc_table=dbo.emergencyShutoffs.scheduled_changes, sc_id=sc_id, transaction=transaction, changed_by=changed_by)
