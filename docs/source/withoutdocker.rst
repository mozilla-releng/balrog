==============================
Running without Docker Compose
==============================

Generally, this is only done in production. For local development, Docker Compose is always recommended.

-------------------
Creating a database
-------------------

Balrog's database is controlled through sqlalchemy-migrate. 
To initialize a new Balrog database, run the following:

::

    docker run --entrypoint python mozilla/balrog /app/scripts/manage-db.py -d DBURI create
    docker run -e "DBURI=<database uri>" -e "LOCAL_ADMIN=<email address of initial admin>" mozilla/balrog create-local-admin

Similarly, to upgrade the schema of an existing Balrog database, run the following:

::

    docker run --entrypoint python mozilla/balrog /app/scripts/manage-db.py -d DBURI upgrade

See the "Environment Variables" section below for DBURI format. If your testing out local changes that affect database creation or upgrades, you should replace "mozilla/balrog" with your local image.

--------------------
Environment Variable
--------------------

The following environment variables are required by the Balrog WSGI apps:

-   **DBURI** - The database to use, in the format: driver://user:password@host/database.
-   **SECRET_KEY** - A pseudorandom string to use when generating CSRF tokens. Only used for the admin app.

These are optional:

-   **LOG_LEVEL** - Controls the python level the app logs at. Set to INFO by default.
-   **LOG_FORMAT** - Controls the log format. If unset, mozlog format (json) will be used. Can be overridden with "plain" to log simple plain-text messages. The former is recommended for production, the latter for local development.
-   **NOTIFY_TO_ADDR** - An address to send an e-mail to if a Rule or Permission changes. Unset by default, and only used for the admin app. If set, the following additional variables are required:
    
    -   **SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD** - Information about the SMTP relay to send mail through.
    -   **NOTIFY_FROM_ADDR** - The "from" address to use when sending mail.
