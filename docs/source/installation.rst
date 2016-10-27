=================
Installing Balrog
=================


Requirements
------------

These instructions assume you have the following installed( if not, you can follow the lonk for installation instrutions)

- `Git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_
- `Docker <https://docs.docker.com/v1.8/installation>`_
- `Docker Compose <https://docs.docker.com/compose/install/>`_

Cloning
-------

Clone the source files using
::
    $ git clone https://github.com/mozilla/balrog

Usage
-----
Once these prerequisites are installed, run the
following command to create and run the necessary images:
::
    $ docker-compose up

Once it completes, you should be able to access

- The admin interface at http://127.0.0.1:8080
- The public interface on port 9090


Running Tests
-------------

It is good idea to run all test to see if balrog is running properly.

To excuting  all tests, run
::

    $ ./run-tests.sh

For executing test only for backend, run

::

    $ ./run-tests.sh backend

For executing test only for frontend, run
::

    $ ./run-tests.sh frontend

Tests can also run by using `tox <http://tox.readthedocs.io/en/latest/install.html>`_
::

    $ tox
