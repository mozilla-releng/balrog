import simplejson as json

from flask import render_template, Response, jsonify, make_response, request

from auslib.blob import ReleaseBlobV1, CURRENT_SCHEMA_VERSION
from auslib.util import getPagination
from auslib.admin.base import db
from auslib.admin.views.base import (
    requirelogin, requirepermission, AdminView, HistoryAdminView
)
from auslib.admin.views.csrf import get_csrf_headers
from auslib.admin.views.forms import ReleaseForm, NewReleaseForm

__all__ = ["SingleReleaseView", "SingleLocaleView", "ReleasesPageView"]

def createRelease(release, product, version, changed_by, transaction, releaseData):
    blob = ReleaseBlobV1(schema_version=CURRENT_SCHEMA_VERSION, **releaseData)
    db.releases.addRelease(name=release, product=product, version=version,
        blob=blob, changed_by=changed_by, transaction=transaction)
    return db.releases.getReleases(name=release, transaction=transaction)[0]

def changeRelease(release, changed_by, transaction, existsCallback, commitCallback, log):
    """Generic function to change an aspect of a release. It relies on a
       ReleaseForm existing and does some upfront work and checks before
       doing anything. It will, for the named release and any found in the
       'copyTo' field of the ReleaseForm:
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
                      in the 'copyTo' field of the ReleaseForm will also be
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
                              - the product name from the ReleaseForm
                              - the version from the ReleaseForm
      @type  commitCallback: callable
      @param commitCallback: The callable to call after all prerequisite checks
                             and updates are done. It must receive 6 positional
                             arguments:
                              - the name of the release
                              - the product name from the ReleaseForm
                              - the version from the ReleaseForm
                              - the data from the ReleaseForm
                              - the most recent version of the data for the
                                release from the database
                              - the old_data_version from the ReleaseForm
    """
    new = True
    form = ReleaseForm()
    if not form.validate():
        return Response(status=400, response=form.errors)
    product = form.product.data
    version = form.version.data
    hashFunction = form.hashFunction.data
    incomingData = form.data.data
    copyTo = form.copyTo.data
    alias = form.alias.data
    old_data_version = form.data_version.data

    allReleases = [release]
    if copyTo:
        allReleases += copyTo
    for rel in allReleases:
        try:
            releaseInfo = db.releases.getReleases(name=rel, transaction=transaction)[0]
            if existsCallback(rel, product, version):
                new = False
            # "release" is the one named in the URL (as opposed to the
            # ones that can be provided in copyTo), and we treat it as
            # the "primary" one
            if rel == release:
                # Make sure that old_data_version is provided, because we need to verify it when updating.
                if not old_data_version:
                    return Response(status=400, response="Release exists, data_version must be provided")
                # If the product we're given doesn't match the one in the DB, panic.
                if product != releaseInfo['product']:
                    return Response(status=400, response="Product name '%s' doesn't match the one on the release object ('%s') for release '%s'" % (product, releaseInfo['product'], rel))
                if 'hashFunction' in releaseInfo['data'] and hashFunction != releaseInfo['data']['hashFunction']:
                    return Response(status=400, response="hashFunction '%s' doesn't match the one on the release object ('%s') for release '%s'" % (hashFunction, releaseInfo['data']['hashFunction'], rel))
            # If this isn't the release in the URL...
            else:
                # Use the data_version we just grabbed from the db.
                old_data_version = releaseInfo['data_version']
        except IndexError:
            # If the release doesn't already exist, create it, and set old_data_version appropriately.
            newReleaseData = dict(name=rel)
            if hashFunction:
                newReleaseData['hashFunction'] = hashFunction
            releaseInfo = createRelease(rel, product, version, changed_by, transaction, newReleaseData)
            old_data_version = 1

        # If the version doesn't match, just update it. This will be the case for nightlies
        # every time there's a version bump.
        if version != releaseInfo['version']:
            log.debug("database version for %s is %s, updating it to %s", rel, releaseInfo['version'], version)
            db.releases.updateRelease(name=rel, version=version,
                changed_by=changed_by, old_data_version=old_data_version,
                transaction=transaction)
            old_data_version += 1

        extraArgs = {}
        if alias:
            extraArgs['alias'] = alias
        commitCallback(rel, product, version, incomingData, releaseInfo['data'], old_data_version, extraArgs)

    new_data_version = db.releases.getReleases(name=release, transaction=transaction)[0]['data_version']
    if new:
        status = 201
    else:
        status = 200
    return make_response(json.dumps(dict(new_data_version=new_data_version)), status)


class SingleLocaleView(AdminView):
    """/releases/[release]/builds/[platform]/[locale]"""
    def get(self, release, platform, locale):
        try:
            locale = db.releases.getLocale(release, platform, locale)
        except KeyError, e:
            return Response(status=404, response=e.args)
        data_version = db.releases.getReleases(name=release)[0]['data_version']
        headers = {'X-Data-Version': data_version}
        headers.update(get_csrf_headers())
        return Response(response=json.dumps(locale), mimetype='application/json', headers=headers)

    @requirelogin
    @requirepermission('/releases/:name/builds/:platform/:locale', options=[])
    def _put(self, release, platform, locale, changed_by, transaction):
        """Something important to note about this method is that using the
           "copyTo" field of the form, updates can be made to more than just
           the release named in the URL. However, the release in the URL is
           still considered the primary one, and used to make decisions about
           what to set the status code to, and what data_version applies to.
           In an ideal world we would probably require a data_version for the
           releases named in copyTo as well."""
        def exists(rel, product, version):
            if rel == release:
                return db.releases.localeExists(name=rel, platform=platform,
                    locale=locale, transaction=transaction)
            return False

        def commit(rel, product, version, localeData, releaseData, old_data_version, extraArgs):
            return db.releases.addLocaleToRelease(name=rel, platform=platform,
                locale=locale, data=localeData, alias=extraArgs.get('alias'), old_data_version=old_data_version,
                changed_by=changed_by, transaction=transaction)

        return changeRelease(release, changed_by, transaction, exists, commit, self.log)

class ReleasesPageView(AdminView):
    """ /releases.html """
    def get(self):
        releases = db.releases.getReleaseInfo()
        form = NewReleaseForm(prefix="new_release")
        return render_template('releases.html', releases=releases, addForm=form)

class SingleBlobView(AdminView):
    """ /releases/[release]/data"""
    def get(self, release):
        release_blob = db.releases.getReleaseBlob(name=release)
        return jsonify(release_blob)

class SingleReleaseView(AdminView):
    """ /releases/[release]"""
    def get(self, release):
        release = db.releases.getReleases(name=release, limit=1)
        if not release:
            return Response(status=404)
        headers = {'X-Data-Version': release[0]['data_version']}
        headers.update(get_csrf_headers())
        return Response(response=render_template('fragments/release_row.html', row=release[0]), headers=headers)

    @requirelogin
    @requirepermission('/releases/:name', options=[])
    def _put(self, release, changed_by, transaction):
        form = NewReleaseForm()
        if not form.validate():
            return Response(status=400, response=form.errors)

        db.releases.addRelease(name=release, product=form.product.data,
            version=form.version.data, blob=form.blob.data,
            changed_by=changed_by, transaction=transaction)
        return Response(status=201)

    @requirelogin
    @requirepermission('/releases/:name')
    def _post(self, release, changed_by, transaction):
        def exists(rel, product, version):
            if rel == release:
                return True
            return False

        def commit(rel, product, version, newReleaseData, releaseData, old_data_version, extraArgs):
            releaseData.update(newReleaseData)
            return db.releases.updateRelease(name=rel, blob=releaseData,
                changed_by=changed_by, old_data_version=old_data_version,
                transaction=transaction)

        return changeRelease(release, changed_by, transaction, exists, commit, self.log)


class ReleaseHistoryView(HistoryAdminView):
    """ /releases/<release>/revisions/ """

    def get(self, release):
        releases = db.releases.getReleases(name=release, limit=1)
        if not releases:
            return Response(status=404,
                            response='Requested release does not exist')
        release = releases[0]
        table = db.releases.history

        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
            assert page >= 1
        except (ValueError, AssertionError), msg:
            return Response(status=400, response=str(msg))
        offset = limit * (page - 1)
        total_count, = (table.t.count()
            .where(table.name == release['name'])
            .where(table.data_version != None)
            .execute()
            .fetchone()
        )
        if total_count > limit:
            pagination = getPagination(page, total_count, limit)
        else:
            pagination = None
        revisions = table.select(
            where=[
                table.name == release['name'],
                table.data_version != None
            ],
            limit=limit,
            offset=offset,
            order_by=[table.timestamp.asc()],
        )
        primary_keys = table.base_primary_key
        all_keys = self.getAllRevisionKeys(revisions, primary_keys)

        self.annotateRevisionDifferences(revisions)

        return render_template(
            'revisions.html',
            revisions=revisions,
            label='release',
            primary_keys=primary_keys,
            all_keys=all_keys,
            pagination=pagination,
            total_count=total_count,
        )

    @requirelogin
    @requirepermission('/releases', options=[])
    def _post(self, release, transaction, changed_by):
        change_id = request.form.get('change_id')
        if not change_id:
            return Response(status=400, response='no change_id')
        change = db.releases.history.getChange(change_id=change_id)
        if change is None:
            return Response(status=404, response='bad change_id')
        if change['name'] != release:
            return Response(status=404, response='bad release')
        releases = db.releases.getReleases(name=release)
        if releases is None:
            return Response(status=404, response='bad release')
        release = releases[0]
        old_data_version = release['data_version']

        # now we're going to make a new update based on this change
        releaseData = json.loads(change['data'])
        blob = ReleaseBlobV1(**releaseData)

        db.releases.updateRelease(changed_by=changed_by, name=change['name'],
            version=change['version'], blob=blob,
            old_data_version=old_data_version, transaction=transaction)

        return Response("Excellent!")
