==============
Infrastructure
==============

------------
Environments
------------

We have stage and production deployments of Balrog. Here's a quick summary:

+-------------+-----------+---------------------------------------------------------+-----------------------------------------+-------------------------------------------------------------------------------+
| Environment | App       | URL                                                     | Deploys                                 | Purpose                                                                       |
+=============+===========+=========================================================+=========================================+===============================================================================+
| Production  | Admin API | https://aus4-admin.mozilla.org/                         | Manually by CloudOps                    | Manage and serve production updates                                           |
+             +-----------+---------------------------------------------------------+                                         +                                                                               +
|             | Admin UI  | https://balrog.services.mozilla.com/                    |                                         |                                                                               |
+             +-----------+---------------------------------------------------------+                                         +                                                                               +
|             | Public    | https://aus5.mozilla.org/                               |                                         |                                                                               |
+-------------+-----------+---------------------------------------------------------+-----------------------------------------+-------------------------------------------------------------------------------+
| Stage       | Admin API | https://admin-stage.balrog.nonprod.cloudops.mozgcp.net/ | When version tags are created in Github | A place to submit staging Releases and verify new Balrog code with automation |
+             +-----------+---------------------------------------------------------+                                         +                                                                               +
|             | Admin UI  | https://balrog-admin-static-stage.stage.mozaws.net/     |                                         |                                                                               |
+             +-----------+---------------------------------------------------------+                                         +                                                                               +
|             | Public    | https://stage.balrog.nonprod.cloudops.mozgcp.net/       |                                         |                                                                               |
+-------------+-----------+---------------------------------------------------------+-----------------------------------------+-------------------------------------------------------------------------------+

--------------------
Support & Escalation
--------------------

RelEng is the first point of contact for issues. To contact them, follow `the standard RelEng escalation path <https://wiki.mozilla.org/ReleaseEngineering#Contacting_Release_Engineering>`_.

If RelEng is unable to correct the issue, they may `escalate to CloudOps <https://mana.mozilla.org/wiki/display/SVCOPS/Contacting+Cloud+Operations>`_.

--------------------
Monitoring & Metrics
--------------------

Metrics from deployment environments are available in `Grafana <https://earthangel-b40313e5.influxcloud.net/d/fRuT9IGZk/balrog?orgId=1&refresh=10s>`_ and `the GCP console <https://console.cloud.google.com/home/dashboard?project=moz-fx-balrog-prod-3fa2&folder=&organizationId=>`_.

We aggregate exceptions from both the Admin & Public apps to `Sentry <https://sentry.prod.mozaws.net/operations/>`_.

--------
ELB Logs
--------

Balrog publishes logs to S3 buckets which are `available for querying on Redash <https://sql.telemetry.mozilla.org>`_. The relevant tables are:

* balrog_elb_logs_aus{3,4,5} - These tables contain update request records sourced from the ELB logs of the named domain (eg: aus5). If you're looking to do ad-hoc queries of update request (eg: estimate how many users are on a particular version or channel), the balrog_elb_logs_aus5 is probably what you want to query.
* balrog_elb_logs_aus_api - This table contains request logs for the aus-api.mozilla.org domain
* log_balrog_admin_nginx_access - This table contains access logs for the admin app sourced from nginx access logs.
* log_balrog_admin_nginx_error - This table contains error logs for the admin app sourced from nginx error logs.
* log_balrog_admin_syslog_admin_fixed - This table contains syslog output from the admin app's Docker container.
* log_balrog_admin_syslog_agent - This table contains syslog output from the agent's Docker container.
* log_balrog_web_syslog_web_fixed - This table contains syslog output from the public app's Docker containers.

Redash should show you the table schemas in the pane on the left. If not, you can inspect with them with "describe $table".

-------
Backups
-------

Balrog uses the built-in RDS backups. The database in snapshotted nightly, and incremental backups are done throughout the day. If necessary, we have the ability to recover to within a 5 minute window. Database restoration is done by CloudOps, and they should be contacted immediately if needed.

-----------------
Deploying Changes
-----------------
Balrog's `stage and production infrastructure <https://mana.mozilla.org/wiki/display/SVCOPS/Balrog+%28aus5%2C+aus4%2C+...%29+Firefox+Update+Service>`_ are managed by `the CloudOps team <https://mana.mozilla.org/wiki/display/SVCOPS/Contacting+Cloud+Operations>`_.

This section describes how to go from a reviewed patch to deploying it in production.

~~~~~~~~~~~~~~~~~~~
Is now a good time?
~~~~~~~~~~~~~~~~~~~
Before you deploy, consider whether or not it's an appropriate time to. Some factors to consider:

* Are we in the middle of an important release such as a chemspill? If so, it's probably not a good time to deploy.
* Is it Friday? You probably don't want to deploy on a Friday except in extreme circumstances.
* Do you have enough time to safely do a push? Most pushes take at most 60 minutes to complete once the production push has begun.

~~~~~~~~~~~~~~~
Schema Upgrades
~~~~~~~~~~~~~~~
If you need to do a schema change you must ensure that either the current production code can run with your schema change applied, or that your new code can run with the old schema. Code and schema changes cannot be done at the same instant, so you must be able to support one of these scenarios. Generally, additive changes (column or table additions) should do the schema change first, while destructive changes (column or table deletions) should do the schema change second. You can simulate the upgrade with your local Docker containers to verify which is right for you.

A quick way to find out if you have a schema change is to diff the current tip of the master branch against the currently deployed tag, eg:
::

 tag=REPLACEME
 git diff $tag


When you file the deployment bug (see below), include a note about the schema change in it. Something like:
::

 This push requires a schema change that needs to be done _prior_ to the new code going out. That can be performed by running the Docker image with the "upgrade-db" command, with DBURI set.

`Bug 1295678 <https://bugzilla.mozilla.org/show_bug.cgi?id=1295678>`_ is an example of a push with a schema change.

~~~~~~~~~~~~~~~~~~
Deploying to Stage
~~~~~~~~~~~~~~~~~~
To get the new code in stage you must create a new Release in Github as follows:

1. Tag the repository with a ``vX.Y`` tag. Eg: ``git tag -s vX.Y && git push --tags``
2. Diff against the previous release tag. Eg: ``git diff v2.24 v2.25``, to double whether or not there's schema changes.

  * Look for anything unexpected, or any schema changes. If schema changes are present, see the above section for instructions on handling them.

3. `Create a new Release on Github <https://github.com/mozilla/balrog/releases>`_. This create new Docker images tagged with your version, and deploys them to stage. It may take upwards of 30 minutes for the deployment to happen.

Once the changes are deployed to stage, let them bake for at least 24 hours. You can do additional targeted testing here if you wish, or simply wait for nightlies/releases to prod things along. It's a good idea to watch Sentry for new exceptions that may show up, and Datadog for any notable changes in the shape of the traffic.

**Important Note!** Only two-part version numbers (like shown above) are supported by our deployment pipeline.

~~~~~~~~~~~~~~~~~~~~~
Verification in Stage
~~~~~~~~~~~~~~~~~~~~~
After deploying, you should do some functional testing in stage. At the very least, you should do explicit testing of all the new code that would be included in the push. Eg: if you're changing the format of a blob, make sure that you can add a new blob of that type, and that the response looks correct. In many cases you should `push a Release to try <https://firefox-source-docs.mozilla.org/tools/try/selectors/release.html?highlight=release>`_ as well.

~~~~~~~~~~~~~~~~~~~~~
Pushing to Production
~~~~~~~~~~~~~~~~~~~~~

Pushing live requires CloudOps. For non-urgent pushes, you should begin this procedure a few hours in advance to give CloudOps time to notice and respond. For urgent pushes, file the bug immediately and escalate if no action is taken quickly. Either way, you must follow this procedure to push:

1. File a bug to have the new version pushed to production

  * Wednesdays around 11am Pacific are usually the best day to push to production, because they are generally free of release events, nightlies, and cronjobs. Unless you have a specific need to deploy on a different day, you should request the prod push for a Wednesday between those hours
  * You should link any bugs being deployed is the "Blocks" field.
  * Make sure you substitute the version number and choose the correct options from the bug template.

2. Once the push has happened, verify that the code was pushed to production by checking the __version__ endpoints on `the Admin <https://aus4-admin.mozilla.org/__version__>`_ and `Public <https://aus5.mozilla.org/__version__>`_ apps.
3. Bump the `in-repo version <https://github.com/mozilla/balrog/blob/master/version.txt>`_ to the next available one to ensure the next push gets a new version.
