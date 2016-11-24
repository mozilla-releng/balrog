=============
Code Overview
=============

Balrog's code is divided into the following parts:

-   `Blobs <https://github.com/mozilla/balrog/tree/master/auslib/blobs>`_: These contain most of the brains (business logic) behind Balrog. They know how to validate new data coming into the system and translate existing data into useful responses to update requests.

-   `Database Abstraction Layer <https://github.com/mozilla/balrog/blob/master/auslib/db.py>`_:This layer sits between the actual database and the applications. It defines the database schema, performs permissions checking, and ensures all changes are written to history tables. Higher level code should never touch the database directly - they should always go through this layer.

-   `User-facing application <https://github.com/mozilla/balrog/tree/master/auslib/web>`_: The entry point to requests from applications looking for updates.

-   `Admin API <https://github.com/mozilla/balrog/tree/master/auslib/admin>`_: A simple RESTful API that allows the Admin UI and automation to make changes to Balrog's database.

-   `The Admin UI <https://github.com/mozilla/balrog/tree/master/ui>`_ : A human-friendly interface to manage updates.

-   `The Balrog Agent <https://github.com/mozilla/balrog/tree/master/agent>`_: A long running process that is responsible for enacting Schedule Changes.
