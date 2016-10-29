==============
Infrastructure
==============

--------------------
Support & Escalation
--------------------

If the issue may be visible to users, please make sure `#moc <irc://irc.mozilla.org/#moc>`_ is also notified.
They can also assist with the notifications below.
RelEng is the first point of contact for issues. 
To contact them, follow the standard `RelEng escalation path <https://wiki.mozilla.org/ReleaseEngineering#Contacting_Release_Engineering>`_.
If RelEng is unable to correct the issue, they may escalate to `CloudOps <https://mana.mozilla.org/wiki/display/SVCOPS/Contacting+Cloud+Operations>`_.

--------------------
Monitoring & Metrics
--------------------
Metrics from RDS, EC2, and Nginx are available in the `Datadog Dashboard <https://app.datadoghq.com/dash/156924/balrog-web-aus5mozillaorg?live=true&page=0&is_auto=false&tile_size=m&fullscreen=false>`_.
We aggregate exceptions from both the `public apps <https://sentry.prod.mozaws.net/operations/prod-public/>`_ and `admin app <https://sentry.prod.mozaws.net/operations/prod-admin/>`_  to `CloudOps' Sentry instance <https://sentry.prod.mozaws.net/operations/>`_.

-------------------
Change Notification
-------------------
Changes made to Rules, Scheduled Rule Changes, Permissions, or the read-only flag of a Release will send e-mail notification to the `balrog-db-changes mailing list <https://groups.google.com/a/mozilla.com/forum/#!forum/balrog-db-changes>`_. 
This serves us an alert system - if we see changes made that we weren't expecting, we can go investigate them.

----------
Nginx Logs
----------
The nginx logs for the public-facing application are replicated to the balrog-us-west-2-elb-logs S3 bucket, located in us-west-2.
Logs are rotated very quickly, and we end up with tens of thousands of separate files each day.
Because of this, and the fact that S3 has a lot of overhead per-file, it can be tricky to do analysis on them.
You're unlikely to be able to download the logs locally in any reasonable amount of time (ie, less than a day), but mounting them on an EC2 instance in us-west-2 should provide you with reasonably quick access. 
Here's an example:

- Launch EC2 instance (you probably a compute-optimized one, and at least 100GB of storage).

- Generate an access token for your CloudOps AWS account. If you don't have a CloudOps AWS account, talk to Ben Hearsum or Bensong Wong. Put the token in a plaintext file somewher on the instance.

  - If you've chosen local storage, you'll probably need to format and mount volume.

- Install s3fs by following the instructions on https://github.com/s3fs-fuse/s3fs-fuse.

- Mount the bucket on your instance, eg:

::
    
    $   s3fs balrog-us-west-2-elb-logs /media/bucket -o passwd_file=pw.txt


- Do some broad grepping directly on the S3 logs, and store it in a local file. This should speed up subsequent queries. Eg:


::
    
    $   grep '/Firefox/.*WINNT.*/release/' /media/bucket/AWSLogs/361527076523/elasticloadbalancing/us-west-2/2016/09/17/* | gzip > /media/ephemeral0/sept-17-winnt-release.txt.gz


- Do additional queries on the new logfile.

-------
Backups
-------
Balrog uses the built-in RDS backups.
The database in snapshotted nightly, and incremental backups are done throughout the day. 
If necessary, we have the ability to recover to within a 5 minute window. Database restoration is done by CloudOps, and they should be contacted immediately if needed.


