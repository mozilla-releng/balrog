import difflib
import json

import connexion
from flask import Response, abort, jsonify

from auslib.blobs.base import createBlob
from auslib.db import OutdatedDataError
from auslib.errors import BlobValidationError, ReadOnlyError
from auslib.global_state import dbo
from auslib.util.signoffs import serialize_signoff_requirements
from auslib.web.admin.views.base import handleGeneralExceptions, log, requirelogin, transactionHandler
from auslib.web.admin.views.problem import problem
from auslib.web.admin.views.scheduled_changes import (
    delete_scheduled_change,
    delete_signoffs_scheduled_change,
    get_by_id_scheduled_change,
    get_scheduled_change_history,
    get_scheduled_changes,
    post_enact_scheduled_change,
    post_scheduled_change,
    post_scheduled_change_history,
    post_scheduled_changes,
    post_signoffs_scheduled_change,
)
from auslib.web.common.releases import serialize_releases

__all__ = ["put_single_release", "post_single_release", "delete_single_release", "put_release_single_locale"]


def createRelease(release, product, changed_by, transaction, releaseData):
    blob = createBlob(releaseData)
    dbo.releases.insert(changed_by=changed_by, transaction=transaction, name=release, product=product, data=blob)
    return dbo.releases.getReleases(name=release, transaction=transaction)[0]


# TODO: certain cases here can return a 400 while still modifying the database
# https://bugzilla.mozilla.org/show_bug.cgi?id=1246993 has more details
def changeRelease(release, changed_by, transaction, existsCallback, commitCallback, log):
    """Generic function to change an aspect of a release. It relies on a
     PartialReleaseForm existing and does some upfront work and checks before
     doing anything. It will, for the named release and any found in the
     'copyTo' field of the PartialReleaseForm:
      - Create the release if it doesn't already exist.
      - return a 400 Response if the release exists and old_data_version doesn't.
      - return a 400 Response if the product name in the form doesn't match the existing one.
      - update the version column of the release table if the one in the form doesn't match it.
      - if the release already exists, 'existsCallback' will be called. If
        that function returns True, a 201 Response will be returned upon
        successful completion. If that function returns False, a 200 Response
        will be returned instead.

    @type  release: string
    @param release: The primary release to update. Additional releases found
                    in the 'copyTo' field of the PartialReleaseForm will also be
                    updated.
    @type  changed_by: string
    @param changed_by: The username making the change.
    @type  transaction: AUSTransaction object
    @param transaction: The transaction object to be used for all database
                        operations.
    @type  existsCallback: callable
    @param existsCallback: The callable to call to determine whether to
                           consider this a "new" change or not. It must
                           receive 3 positional arguments:
                            - the name of the release
                            - the product name from the PartialReleaseForm
                            - the version from the PartialReleaseForm
    @type  commitCallback: callable
    @param commitCallback: The callable to call after all prerequisite checks
                           and updates are done. It must receive 6 positional
                           arguments:
                            - the name of the release
                            - the product name from the PartialReleaseForm
                            - the version from the PartialReleaseForm
                            - the data from the PartialReleaseForm
                            - the most recent version of the data for the
                              release from the database
                            - the old_data_version from the PartialReleaseForm
    """
    new = True
    product = connexion.request.get_json().get("product")
    incomingData = json.loads(connexion.request.get_json().get("data"))

    copyTo = list()
    if connexion.request.get_json().get("copyTo"):
        copyTo = json.loads(connexion.request.get_json().get("copyTo"))

    alias = list()
    if connexion.request.get_json().get("alias"):
        alias = json.loads(connexion.request.get_json().get("alias"))

    old_data_version = connexion.request.get_json().get("data_version")

    # schema_version is an attribute at the root level of a blob.
    # Endpoints that receive an entire blob can find it there.
    # Those that don't have to pass it as a form element instead.

    if connexion.request.get_json().get("schema_version"):
        schema_version = connexion.request.get_json().get("schema_version")
    elif incomingData.get("schema_version"):
        schema_version = incomingData.get("schema_version")
    else:
        return problem(400, "Bad Request", "schema_version is required")

    if connexion.request.get_json().get("hashFunction"):
        hashFunction = connexion.request.get_json().get("hashFunction")
    elif incomingData.get("hashFunction"):
        hashFunction = incomingData.get("hashFunction")
    else:
        hashFunction = None

    allReleases = [release]
    if copyTo:
        allReleases += copyTo
    for rel in allReleases:
        try:
            releaseInfo = dbo.releases.getReleases(name=rel, transaction=transaction)[0]
            if existsCallback(rel, product):
                new = False
            # "release" is the one named in the URL (as opposed to the
            # ones that can be provided in copyTo), and we treat it as
            # the "primary" one
            if rel == release:
                # Make sure that old_data_version is provided, because we need to verify it when updating.
                if not old_data_version:
                    msg = "Release exists, data_version must be provided"
                    log.warning("Bad input: %s", rel)
                    return problem(400, "Bad Request", msg)
                # If the product we're given doesn't match the one in the DB, panic.
                if product != releaseInfo["product"]:
                    msg = "Product name '%s' doesn't match the one on the release object ('%s') for release '%s'" % (product, releaseInfo["product"], rel)
                    log.warning("Bad input: %s", rel)
                    return problem(400, "Bad Request", msg)
                if "hashFunction" in releaseInfo["data"] and hashFunction and hashFunction != releaseInfo["data"]["hashFunction"]:
                    msg = "hashFunction '{0}' doesn't match the one on the release " "object ('{1}') for release '{2}'".format(
                        hashFunction, releaseInfo["data"]["hashFunction"], rel
                    )
                    log.warning("Bad input: %s", rel)
                    return problem(400, "Bad Request", msg)
            # If this isn't the release in the URL...
            else:
                # Use the data_version we just grabbed from the dbo.
                old_data_version = releaseInfo["data_version"]
        except IndexError:
            # If the release doesn't already exist, create it, and set old_data_version appropriately.
            newReleaseData = dict(name=rel, schema_version=schema_version)
            if hashFunction:
                newReleaseData["hashFunction"] = hashFunction
            try:
                releaseInfo = createRelease(rel, product, changed_by, transaction, newReleaseData)
            except BlobValidationError as e:
                msg = "Couldn't create release: %s" % e
                log.warning("Bad input: %s", rel)
                return problem(400, "Bad Request", msg, ext={"exception": e.errors})
            except ValueError as e:
                msg = "Couldn't create release: %s" % e
                log.warning("Bad input: %s", rel)
                return problem(400, "Bad Request", msg, ext={"exception": e.args})
            old_data_version = 1

        extraArgs = {}
        if alias:
            extraArgs["alias"] = alias
        try:
            commitCallback(rel, product, incomingData, releaseInfo["data"], old_data_version, extraArgs)
        except BlobValidationError as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", rel)
            return problem(400, "Bad Request", msg, ext={"exception": e.errors})
        except ReadOnlyError as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", rel)
            return problem(403, "Forbidden", msg, ext={"exception": e.args})
        except (ValueError, OutdatedDataError) as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", rel)
            return problem(400, "Bad Request", msg, ext={"exception": e.args})

    new_data_version = dbo.releases.getReleases(name=release, transaction=transaction)[0]["data_version"]
    if new:
        status = 201
    else:
        status = 200
    return Response(status=status, response=json.dumps(dict(new_data_version=new_data_version)))


def set_required_signoffs_for_product(sc):
    if sc["change_type"] == "update" and not sc["required_signoffs"] and not sc["read_only"] and dbo.releases.isReadOnly(sc["name"]):
        potential_rs = dbo.releases.getPotentialRequiredSignoffsForProduct(sc["product"])
        sc["required_signoffs"] = serialize_signoff_requirements(potential_rs["rs"])


@requirelogin
@transactionHandler
@handleGeneralExceptions
def put_release_single_locale(release, platform, locale, partial_release_body, changed_by, transaction):
    """Something important to note about this method is that using the
    "copyTo" field of the form, updates can be made to more than just
    the release named in the URL. However, the release in the URL is
    still considered the primary one, and used to make decisions about
    what to set the status code to, and what data_version applies to.
    In an ideal world we would probably require a data_version for the
    releases named in copyTo as well."""

    """/releases/[release]/builds/[platform]/[locale]"""

    def exists(rel, product):
        if rel == release:
            return dbo.releases.localeExists(name=rel, platform=platform, locale=locale, transaction=transaction)
        return False

    def commit(rel, product, localeData, releaseData, old_data_version, extraArgs):
        return dbo.releases.addLocaleToRelease(
            name=rel,
            product=product,
            platform=platform,
            locale=locale,
            data=localeData,
            alias=extraArgs.get("alias"),
            old_data_version=old_data_version,
            changed_by=changed_by,
            transaction=transaction,
        )

    return changeRelease(release, changed_by, transaction, exists, commit, log)


@requirelogin
@transactionHandler
@handleGeneralExceptions
def put_single_release(release, release_body, changed_by, transaction):
    if dbo.releases.getReleases(name=release, limit=1):
        if not release_body.get("data_version"):
            return problem(400, "Bad Request", "data_version field is missing")
        try:
            blob = createBlob(release_body.get("blob"))
            dbo.releases.update(
                where={"name": release},
                what={"data": blob, "product": release_body.get("product")},
                changed_by=changed_by,
                old_data_version=release_body.get("data_version"),
                transaction=transaction,
            )
        except BlobValidationError as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", "Couldn't update release", ext={"exception": e.errors})
        except ReadOnlyError as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", msg)
            return problem(403, "Forbidden", "Couldn't update release. Release is marked read only", ext={"exception": e.args})
        except ValueError as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", "Couldn't update release", ext={"exception": e.args})
        # the data_version might jump by more than 1 if outdated blobs are
        # merged
        data_version = dbo.releases.getReleases(name=release, transaction=transaction)[0]["data_version"]
        return jsonify(new_data_version=data_version)
    else:
        try:
            blob = createBlob(release_body.get("blob"))
            dbo.releases.insert(changed_by=changed_by, transaction=transaction, name=release, product=release_body.get("product"), data=blob)
        except BlobValidationError as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", "Couldn't update release", ext={"exception": e.errors})
        except ValueError as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", msg)
            return problem(400, "Bad Request", "Couldn't update release", ext={"exception": e.args})
        return Response(status=201)


@requirelogin
@transactionHandler
@handleGeneralExceptions
def post_single_release(release, partial_release_body, changed_by, transaction):
    def exists(rel, product):
        if rel == release:
            return True
        return False

    def commit(rel, product, newReleaseData, releaseData, old_data_version, extraArgs):
        releaseData.update(newReleaseData)
        blob = createBlob(releaseData)
        return dbo.releases.update(
            where={"name": rel}, what={"data": blob, "product": product}, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction
        )

    return changeRelease(release, changed_by, transaction, exists, commit, log)


@requirelogin
@transactionHandler
@handleGeneralExceptions
def delete_single_release(release, data_version, changed_by, transaction):
    releases = dbo.releases.getReleaseInfo(names=[release], nameOnly=True, limit=1)
    if not releases:
        return problem(404, "Not Found", "Release: %s not found" % release)
    release = releases[0]

    # query argument i.e. data_version  is also required.
    # All input value validations already defined in swagger specification and carried out by connexion.
    try:
        dbo.releases.delete(where={"name": release["name"]}, changed_by=changed_by, old_data_version=data_version, transaction=transaction)
    except ReadOnlyError as e:
        msg = "Couldn't delete release: %s" % e
        log.warning("Bad input: %s", msg)
        return problem(403, "Forbidden", "Couldn't delete %s. Release is marked read only" % release["name"], ext={"exception": e.args})

    return Response(status=200)


def get_release_read_only(release):
    try:
        is_release_read_only = dbo.releases.isReadOnly(name=release, limit=1)
    except KeyError as e:
        return problem(404, "Not Found", json.dumps(e.args))

    return jsonify(read_only=is_release_read_only)


@requirelogin
@transactionHandler
@handleGeneralExceptions
def put_release_read_only(release, release_read_only_body, changed_by, transaction):
    releases = dbo.releases.getReleaseInfo(names=[release], nameOnly=True, limit=1)
    if not releases:
        return problem(404, "Not Found", "Release: %s not found" % release)

    data_version = release_read_only_body.get("data_version")
    is_release_read_only = dbo.releases.isReadOnly(release)
    where = {"name": release}

    if release_read_only_body.get("read_only"):
        if not is_release_read_only:
            dbo.releases.change_readonly(where, True, changed_by, old_data_version=data_version, transaction=transaction)
            data_version += 1
    else:
        dbo.releases.change_readonly(where, False, changed_by, old_data_version=data_version, transaction=transaction)
        data_version += 1
    return Response(status=201, response=json.dumps(dict(new_data_version=data_version)))


def get_release_read_only_product_required_signoffs(release):
    releases = dbo.releases.getReleases(name=release, limit=1)
    if not releases:
        return problem(404, "Not Found", f"Release: {release} not found")
    release = releases[0]
    potential_rs = dbo.releases.getPotentialRequiredSignoffsForProduct(release["product"])
    rs = {"required_signoffs": serialize_signoff_requirements(potential_rs["rs"])}
    return jsonify(rs)


def get_releases(**kwargs):
    opts = {}
    if connexion.request.args.get("product"):
        opts["product"] = connexion.request.args.get("product")
    if connexion.request.args.get("name_prefix"):
        opts["name_prefix"] = connexion.request.args.get("name_prefix")
    if connexion.request.args.get("names_only"):
        opts["nameOnly"] = True
    releases = dbo.releases.getReleaseInfo(**opts)
    if not opts.get("names_only"):
        requirements = dbo.releases.getPotentialRequiredSignoffs(releases)
        for release in releases:
            release["required_signoffs"] = serialize_signoff_requirements(requirements[release["name"]])
    return serialize_releases(connexion.request, releases)


@requirelogin
@transactionHandler
@handleGeneralExceptions
def post_release(release_body, changed_by, transaction):
    if dbo.releases.getReleaseInfo(names=[release_body.get("name")], transaction=transaction, nameOnly=True, limit=1):
        return problem(
            400,
            "Bad Request",
            "Release: %s already exists" % release_body.get("name"),
            ext={"exception": "Database already contains the release"},
        )
    try:
        blob = createBlob(release_body.get("blob"))
        name = dbo.releases.insert(
            changed_by=changed_by,
            transaction=transaction,
            name=release_body.get("name"),
            product=release_body.get("product"),
            data=blob,
        )
    except BlobValidationError as e:
        msg = "Couldn't create release: %s" % e
        log.warning("Bad input: %s", msg)
        return problem(400, "Bad Request", "Couldn't create release", ext={"exception": e.errors})
    except ValueError as e:
        msg = "Couldn't create release: %s" % e
        log.warning("Bad input: %s", msg)
        return problem(400, "Bad Request", "Couldn't create release", ext={"exception": e.args})

    release = dbo.releases.getReleases(name=name, transaction=transaction, limit=1)[0]
    return Response(status=201, response=json.dumps(dict(new_data_version=release["data_version"])))


def get_release_single_column(column):
    releases = dbo.releases.getReleaseInfo()
    column_values = []
    if column not in releases[0].keys():
        return problem(404, "Not Found", "Requested column does not exist")

    for release in releases:
        for key, value in release.items():
            if key == column and value is not None:
                column_values.append(value)
    column_values = list(set(column_values))
    ret = {"count": len(column_values), column: column_values}
    return jsonify(ret)


def get_releases_scheduled_changes():
    where = {}
    name = connexion.request.args.get("name")
    if name:
        where["base_name"] = name

    ret = get_scheduled_changes(table=dbo.releases, where=where)
    scheduled_changes = []
    for sc in ret.json["scheduled_changes"]:
        set_required_signoffs_for_product(sc)
        scheduled_changes.append(sc)
    return jsonify({"count": len(scheduled_changes), "scheduled_changes": scheduled_changes})


@requirelogin
@transactionHandler
@handleGeneralExceptions
def post_releases_scheduled_changes(sc_release_body, transaction, changed_by):
    what = sc_release_body
    if what.get("when", None) is None:
        return problem(400, "Bad Request", "'when' cannot be set to null when scheduling a new change " "for a Release")
    change_type = what.get("change_type")

    if change_type == "update":
        if not what.get("data_version", None):
            return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})

        data = what.get("data", None)

        if data:
            what["data"] = createBlob(data)

        if "read_only" in what and not data:
            what["data"] = dbo.releases.getReleaseBlob(what["name"])

    elif change_type == "insert":
        if not what.get("product", None):
            return problem(400, "Bad Request", "Missing field", ext={"exception": "product is missing"})

        if what.get("data", None):
            what["data"] = createBlob(what.get("data"))
        else:
            return problem(400, "Bad Request", "Missing field", ext={"exception": "Missing blob 'data' value"})

    elif change_type == "delete":
        if not what.get("data_version", None):
            return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})

    try:
        return post_scheduled_changes(
            sc_table=dbo.releases.scheduled_changes, what=what, transaction=transaction, changed_by=changed_by, change_type=change_type
        )
    except ReadOnlyError as e:
        msg = f"Failed to schedule change - {e}"
        return problem(400, "Bad Request", msg, ext={"data": e.args})


def get_by_id_releases_scheduled_change(sc_id):
    ret = get_by_id_scheduled_change(table=dbo.releases, sc_id=sc_id)
    sc = ret.json["scheduled_change"]
    set_required_signoffs_for_product(sc)
    return jsonify({"scheduled_change": sc})


@requirelogin
@transactionHandler
@handleGeneralExceptions
def post_releases_scheduled_change(sc_id, sc_release_body, transaction, changed_by):
    # TODO: modify UI and clients to stop sending 'change_type' in request body
    sc_table = dbo.releases.scheduled_changes
    sc_release = sc_table.select(where={"sc_id": sc_id}, transaction=transaction, columns=["change_type"])
    if sc_release:
        change_type = sc_release[0]["change_type"]
    else:
        return problem(404, "Not Found", "Unknown sc_id", ext={"exception": "No scheduled change for release found for given sc_id"})

    what = {}
    for field in sc_release_body:
        # Only data may be changed when editing an existing Scheduled Change for
        # an existing Release. Name cannot be changed because it is a PK field, and product
        # cannot be changed because it almost never makes sense to (and can be done
        # by deleting/recreating instead).
        # Any Release field may be changed when editing an Scheduled Change for a new Release
        if (
            (change_type == "delete" and field not in ["when", "data_version"])
            or (change_type == "update" and field not in ["when", "data", "data_version"])
            or (change_type == "insert" and field not in ["when", "name", "product", "data"])
        ):
            continue

        what[field] = sc_release_body[field]

    if change_type in ["update", "delete"] and not what.get("data_version", None):
        return problem(400, "Bad Request", "Missing field", ext={"exception": "data_version is missing"})

    elif change_type == "insert" and "data" in what and not what.get("data", None):
        # edit scheduled change for new release
        return problem(400, "Bad Request", "Null/Empty Value", ext={"exception": "data cannot be set to null when scheduling insertion of a new release"})
    if what.get("data", None):
        what["data"] = createBlob(what.get("data"))

    return post_scheduled_change(
        sc_table=sc_table,
        sc_id=sc_id,
        what=what,
        transaction=transaction,
        changed_by=changed_by,
        old_sc_data_version=sc_release_body.get("sc_data_version", None),
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions
def delete_releases_scheduled_change(sc_id, data_version, transaction, changed_by):
    return delete_scheduled_change(
        sc_table=dbo.releases.scheduled_changes, sc_id=sc_id, data_version=data_version, transaction=transaction, changed_by=changed_by
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions
def post_releases_enact_scheduled_change(sc_id, transaction, changed_by):
    return post_enact_scheduled_change(sc_table=dbo.releases.scheduled_changes, sc_id=sc_id, transaction=transaction, changed_by=changed_by)


@requirelogin
@transactionHandler
@handleGeneralExceptions
def post_release_signoffs_scheduled_change(sc_id, sc_post_signoffs_body, transaction, changed_by):
    return post_signoffs_scheduled_change(
        signoffs_table=dbo.releases.scheduled_changes.signoffs, sc_id=sc_id, what=sc_post_signoffs_body, transaction=transaction, changed_by=changed_by
    )


@requirelogin
@transactionHandler
@handleGeneralExceptions
def delete_release_signoffs_scheduled_change(sc_id, transaction, changed_by):
    return delete_signoffs_scheduled_change(signoffs_table=dbo.releases.scheduled_changes.signoffs, sc_id=sc_id, transaction=transaction, changed_by=changed_by)


def get_releases_scheduled_change_history(sc_id):
    return get_scheduled_change_history(sc_table=dbo.releases.scheduled_changes, sc_id=sc_id)


@requirelogin
@transactionHandler
@handleGeneralExceptions
def post_releases_scheduled_change_history(sc_id, transaction, changed_by):
    return post_scheduled_change_history(sc_table=dbo.releases.scheduled_changes, sc_id=sc_id, transaction=transaction, changed_by=changed_by)


def get_scheduled_release_field_value(sc_id, field=None):
    data = dbo.releases.scheduled_changes.select(where={"sc_id": sc_id}, transaction=None)[0]
    if not data:
        abort(400, "Bad sc_id")
    if not field:
        return data
    if field not in data:
        raise KeyError("Bad field")
    return data[field]


def get_release(sc):
    data = dbo.releases.select(where={"name": sc["base_name"], "product": sc["base_product"]}, limit=1)[0]
    if not data:
        abort(400, "Bad sc_id")
    return data


def get_scheduled_release_diff(sc_id):
    sc = get_scheduled_release_field_value(sc_id)
    release = get_release(sc)

    if "data" not in release:
        return problem(400, "Bad Request", "Bad field")

    previous = json.dumps(release["data"], indent=2, sort_keys=True)
    value = json.dumps(sc["base_{}".format("data")], indent=2, sort_keys=True)
    result = difflib.unified_diff(
        previous.splitlines(),
        value.splitlines(),
        fromfile="Current Version (Data Version {})".format(release["data_version"]),
        tofile="Scheduled Update (sc_id {})".format(sc["sc_id"]),
        lineterm="",
    )

    return Response("\n".join(result), content_type="text/plain")
