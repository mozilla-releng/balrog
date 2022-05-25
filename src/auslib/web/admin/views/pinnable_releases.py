from auslib.global_state import dbo
from auslib.web.admin.views.base import requirelogin
from auslib.web.admin.views.scheduled_changes import EnactScheduledChangeView, ScheduledChangesView


class PinnableReleaseScheduledChangesView(ScheduledChangesView):
    """/scheduled_changes/pinnable_releases"""

    def __init__(self):
        super(PinnableReleaseScheduledChangesView, self).__init__("pinnable_releases", dbo.pinnable_releases)

    def get(self):
        return super(PinnableReleaseScheduledChangesView, self).get()


class EnactPinnableReleaseScheduledChangeView(EnactScheduledChangeView):
    """/scheduled_changes/pinnable_releases/<int:sc_id>/enact"""

    def __init__(self):
        super(EnactPinnableReleaseScheduledChangeView, self).__init__("pinnable_releases", dbo.pinnable_releases)

    @requirelogin
    def _post(self, sc_id, transaction, changed_by):
        return super(EnactPinnableReleaseScheduledChangeView, self)._post(sc_id, transaction, changed_by)
