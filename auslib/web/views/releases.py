import simplejson as json

from sqlalchemy.exc import SQLAlchemyError

from flask import render_template, request, Response, jsonify, make_response

from mozilla_buildtools.retry import retry

from auslib.blob import ReleaseBlobV1, CURRENT_SCHEMA_VERSION
from auslib.web.base import app, db
from auslib.web.views.base import requirelogin, requirepermission, AdminView
from auslib.web.views.forms import NewReleaseForm

import logging
log = logging.getLogger(__name__)

__all__ = ["SingleLocaleView"]

class SingleLocaleView(AdminView):
    """/releases/[release]/builds/[platform]/[locale]"""
    def get(self, release, platform, locale):
        locale = db.releases.getLocale(release, platform, locale)
        return jsonify(locale)

    @requirelogin
    @requirepermission('/releases/:name/builds/:platform/:locale', options=[])
    def _put(self, release, platform, locale, changed_by, transaction):
        new = True
        try:
            # Collect all of the release names that we should put the data into
            product = request.form['product']
            version = request.form['version']
            localeBlob = json.loads(request.form['details'])
            copyTo = json.loads(request.form.get('copyTo', '[]'))
        # XXX: use JSONDecodeError instead of ValueError when the servers support it
        except (KeyError, ValueError), e:
            return Response(status=400, response=e.args)

        for rel in [release] + copyTo:
            try:
                releaseObj = db.releases.getReleases(name=rel, transaction=transaction)[0]
            except IndexError:
                releaseObj = None
            # If the release already exists, do some verification on it, and possibly update
            # the version.
            if releaseObj:
                # If the product name provided in the request doesn't match the one we already have
                # for it, fail. Product name changes shouldn't happen here, and any client trying to
                # is probably broken.
                if product != releaseObj['product']:
                    return Response(status=400, response="Product name '%s' doesn't match the one on the release object ('%s') for release '%s'" % (product, releaseObj['product'], rel))

                # However, we _should_ update the version because some rows (specifically,
                # the ones that nightly update rules point at) have their version change over time.
                if version != releaseObj['version']:
                    log.debug("SingleLocaleView.put: database version for %s is %s, updating it to %s", rel, releaseObj['version'], version)
                    def updateVersion():
                        old_data_version = db.releases.getReleases(name=rel, transaction=transaction)[0]['data_version']
                        db.releases.updateRelease(name=rel, version=version, changed_by=changed_by, old_data_version=old_data_version, transaction=transaction)
                        releaseObj['version'] = version
                    retry(updateVersion, sleeptime=5, retry_exceptions=(SQLAlchemyError,))
                # If it does exist, and this is this is the first release (aka, the one in the URL),
                # see if the locale exists, for purposes of setting the correct Response code.
                if rel == release:
                    try:
                        db.releases.getLocale(rel, platform, locale, transaction=transaction)
                        new = False
                    except:
                        pass
            # If the release doesn't exist, create it.
            else:
                releaseBlob = ReleaseBlobV1(name=rel, schema_version=CURRENT_SCHEMA_VERSION)
                retry(db.releases.addRelease, sleeptime=5, retry_exceptions=(SQLAlchemyError,),
                      kwargs=dict(name=rel, product=product, version=version, blob=releaseBlob, changed_by=changed_by, transaction=transaction))
            # We need to wrap this in order to make it retry-able.
            def updateLocale():
                old_data_version = db.releases.getReleases(name=rel, transaction=transaction)[0]['data_version']
                db.releases.addLocaleToRelease(rel, platform, locale, localeBlob, old_data_version, changed_by, transaction)
            retry(updateLocale, sleeptime=5, retry_exceptions=(SQLAlchemyError,))
        new_data_version = db.releases.getReleases(name=release, transaction=transaction)[0]['data_version']
        if new:
            status = 201
        else:
            status = 200
        return make_response(json.dumps(dict(new_data_version=new_data_version)), status)

class ReleasesPageView(AdminView):
    """ /releases.html """
    def get(self):
        releases = db.releases.getReleases()
        form = NewReleaseForm(prefix="new_release")
        return render_template('releases.html', releases=releases, addForm=form)

class SingleBlobView(AdminView):
    """ /releases/[release]/data"""
    def get(self, release):
        release_blob = retry(db.releases.getReleaseBlob, sleeptime=5, retry_exceptions=(SQLAlchemyError,),
                kwargs=dict(name=release))
        return jsonify(release_blob)

class SingleReleaseView(AdminView):
    """ /releases/[release]"""
    def get(self, release):
        release = retry(db.releases.getReleases, sleeptime=5, retry_exceptions=(SQLAlchemyError,),
                kwargs=dict(name=release, limit=1))
        return render_template('fragments/release_row.html', row=release[0])


    @requirelogin
    @requirepermission('/releases/:name', options=[])
    def _put(self, release, changed_by, transaction):
        form = NewReleaseForm()
        if not form.validate():
            return Response(status=400, response=form.errors)

        retry(db.releases.addRelease, sleeptime=5, retry_exceptions=(SQLAlchemyError,), 
                kwargs=dict(name=release, product=form.product.data, version=form.version.data, blob=form.blob.data, changed_by=changed_by,  transaction=transaction))
        return Response(status=201)

app.add_url_rule('/releases/<release>/builds/<platform>/<locale>', view_func=SingleLocaleView.as_view('single_locale'))
app.add_url_rule('/releases/<release>/data', view_func=SingleBlobView.as_view('release_data'))
app.add_url_rule('/releases/<release>', view_func=SingleReleaseView.as_view('release'))
app.add_url_rule('/releases.html', view_func=ReleasesPageView.as_view('releases.html'))
