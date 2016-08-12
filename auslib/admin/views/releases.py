import simplejson as json

from sqlalchemy.sql.expression import null

from flask import Response, jsonify, request

from auslib.global_state import dbo
from auslib.blobs.base import createBlob, BlobValidationError
from auslib.db import OutdatedDataError, ReadOnlyError
from auslib.admin.views.base import (
    requirelogin, AdminView, HistoryAdminView
)
from auslib.admin.views.csrf import get_csrf_headers
from auslib.admin.views.forms import PartialReleaseForm, CompleteReleaseForm, DbEditableForm, ReadOnlyForm

__all__ = ["SingleReleaseView", "SingleLocaleView"]


def createRelease(release, product, changed_by, transaction, releaseData):
    blob = createBlob(json.dumps(releaseData))
    dbo.releases.insert(changed_by=changed_by, transaction=transaction, name=release,
                        product=product, data=blob)
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
    form = PartialReleaseForm()
    if not form.validate():
        log.warning("Bad input: %s", form.errors)
        return Response(status=400, response=json.dumps(form.errors))
    product = form.product.data
    incomingData = form.data.data
    copyTo = form.copyTo.data
    alias = form.alias.data
    old_data_version = form.data_version.data

    # schema_version is an attribute at the root level of a blob.
    # Endpoints that receive an entire blob can find it there.
    # Those that don't have to pass it as a form element instead.
    if getattr(form.schema_version, "data", None):
        schema_version = form.schema_version.data
    elif incomingData.get("schema_version"):
        schema_version = incomingData.get("schema_version")
    else:
        return Response(status=400, response="schema_version is required")

    if getattr(form.hashFunction, "data", None):
        hashFunction = form.hashFunction.data
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
                    return Response(status=400, response=msg)
                # If the product we're given doesn't match the one in the DB, panic.
                if product != releaseInfo['product']:
                    msg = "Product name '%s' doesn't match the one on the release object ('%s') for release '%s'" % (product, releaseInfo['product'], rel)
                    log.warning("Bad input: %s", rel)
                    return Response(status=400, response=msg)
                if 'hashFunction' in releaseInfo['data'] and hashFunction and hashFunction != releaseInfo['data']['hashFunction']:
                    msg = "hashFunction '{0}' doesn't match the one on the release object ('{1}') for release '{2}'".format(
                        hashFunction, releaseInfo["data"]["hashFunction"], rel
                    )
                    log.warning("Bad input: %s", rel)
                    return Response(status=400, response=msg)
            # If this isn't the release in the URL...
            else:
                # Use the data_version we just grabbed from the dbo.
                old_data_version = releaseInfo['data_version']
        except IndexError:
            # If the release doesn't already exist, create it, and set old_data_version appropriately.
            newReleaseData = dict(name=rel, schema_version=schema_version)
            if hashFunction:
                newReleaseData['hashFunction'] = hashFunction
            try:
                releaseInfo = createRelease(rel, product, changed_by, transaction, newReleaseData)
            except BlobValidationError as e:
                msg = "Couldn't create release: %s" % e
                log.warning("Bad input: %s", rel)
                return Response(status=400, response=json.dumps({"data": e.errors}))
            except ValueError as e:
                msg = "Couldn't create release: %s" % e
                log.warning("Bad input: %s", rel)
                return Response(status=400, response=json.dumps({"data": e.args}))
            old_data_version = 1

        extraArgs = {}
        if alias:
            extraArgs['alias'] = alias
        try:
            commitCallback(rel, product, incomingData, releaseInfo['data'], old_data_version, extraArgs)
        except BlobValidationError as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", rel)
            return Response(status=400, response=json.dumps({"data": e.errors}))
        except ReadOnlyError as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", rel)
            return Response(status=403, response=json.dumps({"data": e.args}))
        except (ValueError, OutdatedDataError) as e:
            msg = "Couldn't update release: %s" % e
            log.warning("Bad input: %s", rel)
            return Response(status=400, response=json.dumps({"data": e.args}))

    new_data_version = dbo.releases.getReleases(name=release, transaction=transaction)[0]['data_version']
    if new:
        status = 201
    else:
        status = 200
    return Response(status=status, response=json.dumps(dict(new_data_version=new_data_version)))


class SingleLocaleView(AdminView):
    """/releases/[release]/builds/[platform]/[locale]"""

    def get(self, release, platform, locale):
        try:
            locale = dbo.releases.getLocale(release, platform, locale)
        except KeyError as e:
            return Response(status=404, response=json.dumps(e.args), mimetype="application/json")
        data_version = dbo.releases.getReleases(name=release)[0]['data_version']
        headers = {'X-Data-Version': data_version}
        headers.update(get_csrf_headers())
        return Response(response=json.dumps(locale), mimetype='application/json', headers=headers)

    @requirelogin
    def _put(self, release, platform, locale, changed_by, transaction):
        """Something important to note about this method is that using the
           "copyTo" field of the form, updates can be made to more than just
           the release named in the URL. However, the release in the URL is
           still considered the primary one, and used to make decisions about
           what to set the status code to, and what data_version applies to.
           In an ideal world we would probably require a data_version for the
           releases named in copyTo as well."""
        def exists(rel, product):
            if rel == release:
                return dbo.releases.localeExists(name=rel, platform=platform,
                                                 locale=locale, transaction=transaction)
            return False

        def commit(rel, product, localeData, releaseData, old_data_version, extraArgs):
            return dbo.releases.addLocaleToRelease(name=rel, product=product, platform=platform,
                                                   locale=locale, data=localeData, alias=extraArgs.get('alias'),
                                                   old_data_version=old_data_version,
                                                   changed_by=changed_by, transaction=transaction)

        return changeRelease(release, changed_by, transaction, exists, commit, self.log)


class SingleReleaseView(AdminView):
    """ /releases/:release"""

    def get(self, release):
        release = dbo.releases.getReleases(name=release, limit=1)
        if not release:
            return Response(status=404, mimetype="application/json")
        headers = {'X-Data-Version': release[0]['data_version']}
        headers.update(get_csrf_headers())
        if request.args.get("pretty"):
            indent = 4
        else:
            indent = None
        return Response(response=json.dumps(release[0]['data'], indent=indent), mimetype='application/json', headers=headers)

    @requirelogin
    def _put(self, release, changed_by, transaction):
        form = CompleteReleaseForm()
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        blob = createBlob(form.blob.data)
        if dbo.releases.getReleases(name=release, limit=1):
            data_version = form.data_version.data
            try:
                dbo.releases.update(where={"name": release}, what={"data": blob, "product": form.product.data}, changed_by=changed_by,
                                    old_data_version=data_version, transaction=transaction)
            except BlobValidationError as e:
                msg = "Couldn't update release: %s" % e
                self.log.warning("Bad input: %s", msg)
                return Response(status=400, response=json.dumps({"data": e.errors}))
            except ReadOnlyError as e:
                msg = "Couldn't update release: %s" % e
                self.log.warning("Bad input: %s", msg)
                return Response(status=403, response=json.dumps({"data": e.args}))
            except ValueError as e:
                msg = "Couldn't update release: %s" % e
                self.log.warning("Bad input: %s", msg)
                return Response(status=400, response=json.dumps({"data": e.args}))
            # the data_version might jump by more than 1 if outdated blobs are
            # merged
            data_version = dbo.releases.getReleases(name=release, transaction=transaction)[0]['data_version']
            return jsonify(new_data_version=data_version)
        else:
            try:
                dbo.releases.insert(changed_by=changed_by, transaction=transaction, name=release,
                                    product=form.product.data, data=blob)
            except BlobValidationError as e:
                msg = "Couldn't update release: %s" % e
                self.log.warning("Bad input: %s", msg)
                return Response(status=400, response=json.dumps({"data": e.errors}))
            except ValueError as e:
                msg = "Couldn't update release: %s" % e
                self.log.warning("Bad input: %s", msg)
                return Response(status=400, response=json.dumps({"data": e.args}))
            return Response(status=201)

    @requirelogin
    def _post(self, release, changed_by, transaction):
        def exists(rel, product):
            if rel == release:
                return True
            return False

        def commit(rel, product, newReleaseData, releaseData, old_data_version, extraArgs):
            releaseData.update(newReleaseData)
            blob = createBlob(releaseData)
            return dbo.releases.update(where={"name": rel}, what={"data": blob, "product": product},
                                       changed_by=changed_by, old_data_version=old_data_version,
                                       transaction=transaction)

        return changeRelease(release, changed_by, transaction, exists, commit, self.log)

    @requirelogin
    def _delete(self, release, changed_by, transaction):
        releases = dbo.releases.getReleases(name=release)
        if not releases:
            return Response(status=404, response='bad release')
        release = releases[0]

        # Bodies are ignored for DELETE requests, so we need to force WTForms
        # to look at the arguments instead.
        # We only need the release name (which comes through the URL) and the
        # data version to process this request. Because of that, we can just
        # use this form to validate, because we're only validating CSRF
        # and data version.
        form = DbEditableForm(request.args)
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        try:
            dbo.releases.delete(where={"name": release["name"]}, changed_by=changed_by, old_data_version=form.data_version.data,
                                transaction=transaction)
        except ReadOnlyError as e:
                msg = "Couldn't delete release: %s" % e
                self.log.warning("Bad input: %s", msg)
                return Response(status=403, response=json.dumps({"data": e.args}))

        return Response(status=200)


class ReleaseReadOnlyView(AdminView):
    """/releases/:release/read_only"""

    def get(self, release):
        try:
            is_release_read_only = dbo.releases.isReadOnly(name=release, limit=1)
        except KeyError as e:
            return Response(status=404, response=json.dumps(e.args), mimetype="application/json")

        return jsonify(read_only=is_release_read_only)

    @requirelogin
    def _put(self, release, changed_by, transaction):
        form = ReadOnlyForm()
        data_version = form.data_version.data

        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))
        is_release_read_only = dbo.releases.isReadOnly(release)

        if form.read_only.data:
            if not is_release_read_only:
                dbo.releases.update(where={"name": release}, what={"read_only": True}, changed_by=changed_by, old_data_version=data_version,
                                    transaction=transaction)
                data_version += 1
        else:
            dbo.releases.update(where={"name": release}, what={"read_only": False}, changed_by=changed_by, old_data_version=data_version,
                                transaction=transaction)
            data_version += 1
        return Response(status=201, response=json.dumps(dict(new_data_version=data_version)))


class ReleaseHistoryView(HistoryAdminView):
    """/releases/:release/revisions"""

    def get(self, release):
        releases = dbo.releases.getReleases(name=release, limit=1)
        if not releases:
            return Response(status=404,
                            response='Requested release does not exist')
        release = releases[0]
        table = dbo.releases.history

        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            assert page >= 1
        except (ValueError, AssertionError) as e:
            self.log.warning("Bad input: %s", json.dumps(e.args))
            return Response(status=400, response=json.dumps({"data": e.args}))
        offset = limit * (page - 1)
        total_count = table.t.count()\
            .where(table.name == release['name'])\
            .where(table.data_version != null())\
            .execute()\
            .fetchone()[0]

        revisions = table.select(
            where=[
                table.name == release['name'],
                table.data_version != null()
            ],
            limit=limit,
            offset=offset,
            order_by=[table.timestamp.desc()],
        )

        self.annotateRevisionDifferences(revisions)

        return jsonify(revisions=revisions, count=total_count)

    @requirelogin
    def _post(self, release, transaction, changed_by):
        releases = dbo.releases.getReleases(name=release)
        if not releases:
            return Response(status=404, response='bad release')
        change_id = None
        if request.json:
            change_id = request.json.get('change_id')
        if not change_id:
            self.log.warning("Bad input: %s", release)
            return Response(status=400, response='no change_id')
        change = dbo.releases.history.getChange(change_id=change_id)
        if change is None:
            return Response(status=400, response='bad change_id')
        if change['name'] != release:
            return Response(status=400, response='bad release')
        release = releases[0]
        old_data_version = release['data_version']

        # now we're going to make a new update based on this change
        blob = createBlob(change['data'])

        try:
            dbo.releases.update(where={"name": change["name"]}, what={"data": blob, "product": change["product"]}, changed_by=changed_by,
                                old_data_version=old_data_version, transaction=transaction)
        except BlobValidationError as e:
            self.log.warning("Bad input: %s", e.args)
            return Response(status=400, response=json.dumps({"data": e.errors}))
        except ValueError as e:
            self.log.warning("Bad input: %s", e.args)
            return Response(status=400, response=json.dumps({"data": e.args}))

        return Response("Excellent!")


class ReleasesAPIView(AdminView):
    """/releases"""

    def get(self, **kwargs):
        kwargs = {}
        if request.args.get('product'):
            kwargs['product'] = request.args.get('product')
        if request.args.get('name_prefix'):
            kwargs['name_prefix'] = request.args.get('name_prefix')
        if request.args.get('names_only'):
            kwargs['nameOnly'] = True
        releases = dbo.releases.getReleaseInfo(**kwargs)
        if request.args.get('names_only'):
            names = []
            for release in releases:
                names.append(release['name'])
            data = {'names': names}
        else:
            _releases = []
            _mapping = {
                # return : db name
                'name': 'name',
                'product': 'product',
                'data_version': 'data_version',
                'read_only': 'read_only',
                'rule_ids': 'rule_ids',
            }
            for release in releases:
                _releases.append(dict(
                    (key, release[db_key])
                    for key, db_key in _mapping.items()
                ))
            data = {
                'releases': _releases,
            }

        return jsonify(data)

    @requirelogin
    def _post(self, changed_by, transaction):
        form = CompleteReleaseForm()
        if not form.validate():
            self.log.warning("Bad input: %s", form.errors)
            return Response(status=400, response=json.dumps(form.errors))

        try:
            blob = createBlob(form.blob.data)
            name = dbo.releases.insert(changed_by=changed_by, transaction=transaction,
                                       name=form.name.data, product=form.product.data,
                                       data=blob)
        except BlobValidationError as e:
            msg = "Couldn't update release: %s" % e
            self.log.warning("Bad input: %s", msg)
            return Response(status=400, response=json.dumps({"data": e.errors}))
        except ValueError as e:
            msg = "Couldn't update release: %s" % e
            self.log.warning("Bad input: %s", msg)
            return Response(status=400, response=json.dumps({"data": e.args}))

        release = dbo.releases.getReleases(
            name=name, transaction=transaction, limit=1
        )[0]
        return Response(status=201, response=json.dumps(dict(new_data_version=release["data_version"])))


class SingleReleaseColumnView(AdminView):
    """ /releases/columns/:column"""

    def get(self, column):
        releases = dbo.releases.getReleaseInfo()
        column_values = []
        if column not in releases[0].keys():
            return Response(status=404, response="Requested column does not exist")

        for release in releases:
            for key, value in release.items():
                if key == column and value is not None:
                    column_values.append(value)
        column_values = list(set(column_values))
        ret = {
            "count": len(column_values),
            column: column_values,
        }
        return jsonify(ret)
