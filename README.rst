Balrog
======
|CI| |Coverage|

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

The ``run-tests.sh`` script runs tests inside a Docker container,
which is convenient but can be slow. You can also set up a virtualenv
yourself and run tests "locally" using tox::

    $ tox

or py.test::

    $ py.test -n2 --cov=. --doctest-modules auslib

Note that Docker may have set files to be owned by root, so you may
need to ``chmod -R $(whoami) .`` to make them writable by tox and
hypothesis.

Documentation
-------------

Balrog's documentation is hosted at http://mozilla-balrog.readthedocs.io/en/latest/index.html


Getting Involved
----------------
If you like to get involved in the development of Balrog there're lots of areas where we could use some help. To start with, it's recommended that you look at a `Good First Bug <https://bugzilla.mozilla.org/buglist.cgi?list_id=13406850&emailtype1=exact&status_whiteboard_type=allwordssubstr&emailassigned_to1=1&status_whiteboard=%5Bgood%20first%20bug%5D&email1=nobody%40mozilla.org&resolution=---&query_format=advanced&component=Balrog%3A%20Backend&component=Balrog%3A%20Frontend>`_. Once you're more comfortable with Balrog, we've got a long list of `other bugs ready to be worked on <https://bugzilla.mozilla.org/buglist.cgi?list_id=13406852&emailtype1=exact&status_whiteboard_type=allwordssubstr&emailassigned_to1=1&status_whiteboard=%5Bready%5D&email1=nobody%40mozilla.org&resolution=---&query_format=advanced&component=Balrog%3A%20Backend&component=Balrog%3A%20Frontend>`_.

Come talk to us in #balrog if you're interested!

If you find a problem and wish to report it, please `file a bug <https://bugzilla.mozilla.org/enter_bug.cgi#h=dupes%7CRelease+Engineering>`_ .

License
-------
Balrog is released under `Mozilla Public License 2.0 <https://opensource.org/licenses/MPL-2.0>`_.


.. |CI| image:: https://github.taskcluster.net/v1/repository/mozilla/balrog/master/badge.svg
   :target: https://github.taskcluster.net/v1/repository/mozilla/balrog/master/latest
.. |Coverage| image:: https://coveralls.io/repos/github/mozilla/balrog/badge.svg?branch=master
   :target: https://coveralls.io/github/mozilla/balrog?branch=master
