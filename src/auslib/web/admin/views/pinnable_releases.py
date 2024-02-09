from auslib.global_state import dbo
from auslib.web.admin.views.base import requirelogin
from auslib.web.admin.views.scheduled_changes import EnactScheduledChangeView, get_scheduled_changes


def get_pinnable_releases_scheduled_changes():
    """/scheduled_changes/pinnable_releases"""

    return get_scheduled_changes(table=dbo.pinnable_releases)


class EnactPinnableReleaseScheduledChangeView(EnactScheduledChangeView):
    """/scheduled_changes/pinnable_releases/<int:sc_id>/enact"""

    def __init__(self):
        super(EnactPinnableReleaseScheduledChangeView, self).__init__("pinnable_releases", dbo.pinnable_releases)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(EnactPinnableReleaseScheduledChangeView, self)._post(sc_id, transaction, changed_by)
