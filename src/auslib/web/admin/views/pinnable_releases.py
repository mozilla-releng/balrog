from auslib.global_state import dbo
from auslib.web.admin.views.base import handleGeneralExceptions, requirelogin, transactionHandler
from auslib.web.admin.views.scheduled_changes import get_scheduled_changes, post_enact_scheduled_change


def get_pinnable_releases_scheduled_changes():
    return get_scheduled_changes(table=dbo.pinnable_releases)


@requirelogin
@transactionHandler
@handleGeneralExceptions
def post_pinnable_releases_enact_scheduled_change(sc_id, transaction, changed_by):
    return post_enact_scheduled_change(sc_table=dbo.pinnable_releases.scheduled_changes, sc_id=sc_id, transaction=transaction, changed_by=changed_by)
