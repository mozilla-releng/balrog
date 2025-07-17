import json
import logging

from connexion import problem
from flask import Response, jsonify, request

from auslib.global_state import dbo
from auslib.services import releases as releases_service
from auslib.util.data_structures import get_by_path

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
    with dbo.begin() as trans:
        ret = dbo.releases.getReleaseInfo(**kwargs, transaction=trans)
        if kwargs.get("nameOnly"):
            for name in releases_service.get_release_names(trans, product=kwargs.get("product")):
                if kwargs.get("name_prefix") and not name.startswith(kwargs["name_prefix"]):
                    continue

                ret.append({"name": name})
        else:
            for r in releases_service.get_releases(trans)["releases"]:
                if kwargs.get("product") and r["product"] != kwargs["product"]:
                    continue
                if kwargs.get("name_prefix") and not r["name"].startswith(kwargs["name_prefix"]):
                    continue

                ret.append(r)

        return ret


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
    with dbo.begin() as trans:
        release_row = releases_service.get_release(release, trans)
        if release_row:
            return {"data": release_row["blob"], "data_version": release_row["data_versions"]["."]}
        else:
            releases = dbo.releases.getReleases(name=release, limit=1, transaction=trans)
            return releases[0] if releases else None


def get_release(release):
    release_row = _get_release(release)
    if not release_row:
        return problem(404, "Not Found", "Release name: %s not found" % release)
    headers = {"X-Data-Version": release_row["data_version"]}
    if request.args.get("pretty"):
        indent = 4
        separators = (",", ": ")
    else:
        indent = None
        separators = None
    # separators set manually due to https://bugs.python.org/issue16333 affecting Python 2
    return Response(
        response=json.dumps(release_row["data"], indent=indent, separators=separators, sort_keys=True), mimetype="application/json", headers=headers
    )


def get_single_locale(release, platform, locale):
    with dbo.begin() as trans:
        release_row = releases_service.get_release(release, trans)
        if release_row:
            locale_data = get_by_path(release_row["blob"], ("platforms", platform, "locales", locale))
            data_version = get_by_path(release_row["data_versions"], ("platforms", platform, "locales", locale))
        else:
            try:
                locale_data = dbo.releases.getLocale(release, platform, locale, transaction=trans)
            except KeyError as e:
                return problem(404, "Not Found", json.dumps(e.args))
            data_version = dbo.releases.getReleases(name=release, transaction=trans)[0]["data_version"]
        headers = {"X-Data-Version": data_version}
        return Response(response=json.dumps(locale_data), mimetype="application/json", headers=headers)
