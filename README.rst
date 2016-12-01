Balrog
======
|Coverage|

Balrog is the software that runs the server side component of the update system used by Firefox and other Mozilla products.

Download
--------
Clone from git using

::

    $ git clone https://github.com/mozilla/balrog

Installation
------------
To run a development environment you must have Docker and docker-compose
installed (if you're on Windows or Mac you need "Docker for Windows" or "Docker
for Mac" at least v1.12.0)

Once these prerequisites are installed, run the
following command to create and run the necessary images:

::

    $ docker-compose up

Once it completes, you should be able to access

- The admin interface at http://127.0.0.1:8080
- The public interface on port 9090


Tests
-----

To execute all tests, run
::

    $ ./run-tests.sh

For executing test only for backend, run
::

    $ ./run-tests.sh backend

For executing test only for frontend, run
::

    $ ./run-tests.sh frontend

Tests can also run by using tox
::

    $ tox


Documentation
-------------

Balrog's documentation is hosted at http://mozilla-balrog.readthedocs.io/en/latest/index.html


Getting Involved
----------------
If you like to get involved in the development of Balrog there're lots of areas where we could use some help.
You can take look at the bugs filed at bugzilla for
`Balrog Backend <https://bugzilla.mozilla.org/buglist.cgi?product=Release%20Engineering&component=Balrog%3A%20Backend&resolution=---&list_id=13281625>`_
and
`Balrog Frontend <https://bugzilla.mozilla.org/buglist.cgi?product=Release%20Engineering&component=Balrog%3A%20Frontend&resolution=---&list_id=13281632>`_.

Come talk to us in #balrog if you're interested!

If you find a problem and wish to report it, please `file a bug <https://bugzilla.mozilla.org/enter_bug.cgi#h=dupes%7CRelease+Engineering>`_ .

License
-------
Balrog is released under `Mozilla Public License 2.0 <https://opensource.org/licenses/MPL-2.0>`_.



.. |Coverage| image:: https://coveralls.io/repos/github/mozilla/balrog/badge.svg?branch=master
   :target: https://coveralls.io/github/mozilla/balrog?branch=master
