from auslib.web.admin.views.releases import (
    ReleasesAPIView, SingleReleaseView, ReleaseHistoryView)


def get():
    view = ReleasesAPIView()
    return view.get()


def get_release(release):
    view = SingleReleaseView()
    return view.get(release, False)


def get_revisions(release):
    view = ReleaseHistoryView()
    return view.get(release)
