from auslib.global_state import dbo
from auslib.web.admin.views.base import debugPath, handleGeneralExceptions, requirelogin, transactionHandler
from auslib.web.admin.views.scheduled_changes import get_scheduled_changes, post_enact_scheduled_change


def get_pinnable_releases_scheduled_changes():
    """/scheduled_changes/pinnable_releases"""

    return get_scheduled_changes(table=dbo.pinnable_releases)


@requirelogin
@transactionHandler
@handleGeneralExceptions("POST")
@debugPath
def post_pinnable_releases_enact_scheduled_change(sc_id, transaction, changed_by):
    """/scheduled_changes/pinnable_releases/<int:sc_id>/enact"""

    return post_enact_scheduled_change(sc_table=dbo.pinnable_releases.scheduled_changes, sc_id=sc_id, transaction=transaction, changed_by=changed_by)
