============
Balrog Agent
============

The Balrog Agent is a long running process that is responsible for monitoring and enacting :ref:`scheduledChanges`. 
The Agent is a separate application that runs in its own Docker container. 
In order to ensure it cannot bypass permissions or history (accidentally or on purpose), the Agent acts as a client to the Admin App rather than interacting with the database directly. 
This means that it must be granted the "scheduled_change" permission to function.

In the future, the Agent may also act as a client to Telemetry, Crash Stats, or other systems that contain data that we may want to schedule changes with.
