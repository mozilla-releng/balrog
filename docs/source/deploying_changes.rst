=================
Deploying Changes
=================
Balrog's stage and production infrastructure is managed by the Cloud Operations team.
This section describes how to go from a reviewed patch to deploying it in production.

-------------------
Is now a good time?
-------------------
Before you deploy, consider whether or not it's an appropriate time to. Some factors to consider:

-   Are we in the middle of an important release such as a chemspill? If so, it's probably not a good time to deploy.
  
-   How risky are your changes? If they're high risk, deploying on a Friday is probably a bad idea.

-   Do you need to migrate any data? If you do, make sure you have time to do so right after deploying.

-   Do you have enough time to safely do a push? Most pushes take at most 60 minutes to complete after the stage push has been done. This time is mostly affected by how long it takes you to verify your changes in stage and production.

-----------------------
Landing Schema Upgrades
-----------------------
If you need to do a schema change you must ensure that either the current production code can run with your schema change applied, or that your new code can run with the old schema.
Code and schema changes cannot be done at the same instant, so you must be able to support one of these scenarios.
Generally, additive changes (column or table additions) should do the schema change first, while destructive changes (column or table deletions) should do the schema change second. 
You can simulate the upgrade with your local Docker containers to verify which is right for you.
When you file the deployment bug (see below), include a note about the schema change in it. 
Something like:

    **This push requires a schema change that needs to be done _prior_ to the new code going out. 
    That can be performed by running the Docker image with the "upgrade-db" command, with DBURI set.**

-------
Testing
-------
Before asking for a push, you should do some functional testing on your local machine with the Docker images. 
You should do this against the master branch of the upstream repository to ensure you're testing the exact code that is to be deployed. 
At the very least, you should do explicit testing of all the new code that would be included in the push. 
Eg: if you're changing the format of a blob, make sure that you can add a new blob of that type, and that the XML response looks correct.

-------------------------------
Pushing to stage and production
-------------------------------
Pushing live is a two step process. 
First, you must push to the stage environment and ensure things are working there. 
Then, you can push live.


-  Bump the in-repo version.

-  Tag the repository with a "vX.Y" tag. Eg: "git tag -s vX.Y"

-  Wait for CI jobs to complete. Unit tests must pass and a new Docker Image for the webapps and the Agent must be pushed to Dockerhub before you proceed.

-  File a bug to have the new version pushed to stage. Be sure to include the new version number, and Docker image tags for the webapps and the Agent you want deployed.

-  Once stage has been updated, verify your changes again. Even though you've tested locally, it's important to retest in stage to make sure there's no deployment-specific issues.
   
-  When stage looks good, you're ready to comment in the bug to ask for production to be updated.
Reverify in production. When production has been updated, verify your changes again there. If you need to tweak rules or releases to do so, be careful not to touch any live channels (create new rules or releases if necessary). This final verification is as more about making sure the right thing got deployed than whether or not your code is correct.
