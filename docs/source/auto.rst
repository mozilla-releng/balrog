==============
Database Model
==============


Balrog's model centres around two concepts: Rules and Releases. 
When a request for update from an application is received it is matched up against the rules.
Once the correct rule has been found, it contains a pointer to a Release, which contains all of the metadata needed to construct a proper update response. 
Rules and Releases are described in greater detail below:

Rules
-----

.. autoclass:: auslib.db.Rules

Releases
--------
.. autoclass:: auslib.db.Releases

Permissions
-----------
.. autoclass:: auslib.db.Permissions

History
-------
.. autoclass:: auslib.db.History


