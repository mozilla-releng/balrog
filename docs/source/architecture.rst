Architecture
============

Database Model
==============

Balrog's model centres around two concepts: Rules and Releases. 
When a request for update from an application is received it is matched up against the rules.
Once the correct rule has been found, it contains a pointer to a Release, which contains all of the metadata needed to construct a proper update response. 
Rules and Releases are described in greater detail below:

Rules
-----
The most important part of Balrog to understand is its rules. 
When a request comes in it is matched against each of Balrog's rule to find the one that best suits it (more in this below). 
Once found, Balrog looks at that rule's "mapping", which points at a release that has the required information to serve an update back to the client. 
Without any rules, Balrog will never serve an update. 
With badly configured rules Balrog could do bad things like serve Firefox updates to B2G devices.


