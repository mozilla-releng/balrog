import json
import logging

from connexion import problem, request
from flask import Response, jsonify

from auslib.global_state import dbo
from auslib.web.common.csrf import get_csrf_headers

log = logging.getLogger(__name__)


def strip_data(release):
    """Return a release with all the fields except data.

    This is used in multiple APIs to save bandwidth and present a
    simplified view of the release by removing its largest field,
    data, which is of no use except when serving clients.
    """
    return dict((k, v) for (k, v) in release.items() if k != "data")


def release_list(request):
    kwargs = {}
    if request.args.get("product"):
        kwargs["product"] = request.args.get("product")
    if request.args.get("name_prefix"):
        kwargs["name_prefix"] = request.args.get("name_prefix")
    if request.args.get("names_only"):
        kwargs["nameOnly"] = True
    return dbo.releases.getReleaseInfo(**kwargs)


def serialize_releases(request, releases):
    if request.args.get("names_only"):
        names = []
        for release in releases:
            names.append(release["name"])
        data = {"names": names}
    else:
        data = {"releases": [strip_data(release) for release in releases]}
    return jsonify(data)


def get_releases():
    releases = release_list(request)
    return serialize_releases(request, releases)


def _get_release(release):
    releases = dbo.releases.getReleases(name=release, limit=1)
    return releases[0] if releases else None


def get_release(release, with_csrf_header=False):
    release = _get_release(release)
    if not release:
        return problem(404, "Not Found", "Release name: %s not found" % release)
    headers = {"X-Data-Version": release["data_version"]}
    if with_csrf_header:
        headers.update(get_csrf_headers())
    if request.args.get("pretty"):
        indent = 4
        separators = (",", ": ")
    else:
        indent = None
        separators = None
    # separators set manually due to https://bugs.python.org/issue16333 affecting Python 2
    return Response(response=json.dumps(release["data"], indent=indent, separators=separators, sort_keys=True), mimetype="application/json", headers=headers)


def get_release_with_csrf_header(release):
    return get_release(release, with_csrf_header=True)


def get_release_single_locale(release, platform, locale, with_csrf_header=False):
    try:
        locale = dbo.releases.getLocale(release, platform, locale)
    except KeyError as e:
        return problem(404, "Not Found", json.dumps(e.args))
    data_version = dbo.releases.getReleases(name=release)[0]["data_version"]
    headers = {"X-Data-Version": data_version}
    if with_csrf_header:
        headers.update(get_csrf_headers())
    return Response(response=json.dumps(locale), mimetype="application/json", headers=headers)


def get_release_single_locale_with_csrf_header(release, platform, locale):
    return get_release_single_locale(release, platform, locale, with_csrf_header=True)
