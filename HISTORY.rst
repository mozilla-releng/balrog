=======
History
=======

2.79
----

* Support ``FirefoxVPN`` as new name for ``Guardian``

  * ``Guardian`` is now deprecated, and will be fully removed/renamed to ``FirefoxVPN`` in a future release

2.78
-----------------------

* Require signoff to change releases from read only -> read write (#983)

  * Includes UI component from https://github.com/mozilla-frontend-infra/balrog-ui/pull/229

* Pick up latest ``react-auth0-components`` to fix login issues when SSO session has expired (https://github.com/mozilla-frontend-infra/react-auth0-components/pull/11)
