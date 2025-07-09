|CI| |Coverage|

Balrog is the software that runs the server side component of the update system used by Firefox and other Mozilla products.

Installation
============
To run a development environment you must have Docker and docker-compose
installed (if you're on Windows or Mac you need "Docker for Windows" or "Docker
for Mac" at least v1.12.0)

If you have access to it, set up the machine token for the Agent. If you don't have access to it, just skip this step. The Agent will not function, but everything else will work.
::

    $ export AUTH0_M2M_CLIENT_SECRET=abcdef123456

Run the following command to create and run the necessary containers:
::

    $ docker-compose up

**Note**

*On ARM (M1) chips*

Make sure you are running a recent version of docker compose:
::

    $ docker-compose version
    Docker Compose version v2.2.3

Then, run the following command to create and run the necessary containers:
::

    $ docker-compose -f docker-compose.yml -f docker-compose.arm.yml up

Once it completes, you should be able to access

- http://localhost:9010 - The public API
- https://localhost:8010 - The admin API
- https://localhost:9000 - The admin interface
- http://localhost:8050 - A graphite interface

You'll need to accept the self signed SSL certificates in your browser for each of the https links above for everything (especially the UI) to function correctly.

You'll need to use the "Sign in..." button to do anything useful with the admin interface, which will ask you to sign in with a third party provider (eg: gmail, github). Once you've done that, run the following to create a local admin user to gain write access:
::

    $ export LOCAL_ADMIN=<email address you signed in with>
    $ docker-compose run balrogadmin create-local-admin


Tests
=====
To execute all tests, simply run:
::

    $ tox

This will run all unit tests within a Docker container.

Updating dependencies
=====================

To update the python dependencies, use `./maintenance/pin.sh`, do not run `pip-compile-multi` manually.

Documentation
=============

Balrog's documentation is hosted at http://mozilla-balrog.readthedocs.io/en/latest/index.html

License
=======
Balrog is released under `Mozilla Public License 2.0 <https://opensource.org/licenses/MPL-2.0>`_.


.. |CI| image:: https://firefox-ci-tc.services.mozilla.com/api/github/v1/repository/mozilla-releng/balrog/main/badge.svg
   :target: https://firefox-ci-tc.services.mozilla.com/api/github/v1/repository/mozilla-releng/balrog/main/latest
.. |Coverage| image:: https://coveralls.io/repos/github/mozilla-releng/balrog/badge.svg?branch=HEAD
   :target: https://coveralls.io/github/mozilla-releng/balrog?branch=HEAD
