from auslib.global_state import dbo
from auslib.web.admin.views import scheduled_changes as sc
from auslib.web.admin.views.base import requirelogin, transactionHandler


def get_scheduled_changes():
    return sc.get_scheduled_changes(table=dbo.pinnable_releases)


@requirelogin
@transactionHandler
def enact_scheduled_change(sc_id, transaction, changed_by):
    return sc.post_enact_scheduled_change(sc_table=dbo.pinnable_releases.scheduled_changes, sc_id=sc_id, transaction=transaction, changed_by=changed_by)
