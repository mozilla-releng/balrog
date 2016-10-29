============
Architecture
============

Database Model
--------------

Balrog's model centres around two concepts: Rules and Releases. 
When a request for update from an application is received it is matched up against the rules.
Once the correct rule has been found, it contains a pointer to a Release, which contains all of the metadata needed to construct a proper update response. 
Rules and Releases are described in greater detail below:

-----
Rules
-----
The most important part of Balrog to understand is its rules. 
When a request comes in it is matched against each of Balrog's rule to find the one that best suits it (more in this below). 
Once found, Balrog looks at that rule's "mapping", which points at a release that has the required information to serve an update back to the client. 
Without any rules, Balrog will never serve an update. 
With badly configured rules Balrog could do bad things like serve Firefox updates to B2G devices.

**What's in a rule?**

Each rule has mulitple columns. They all fall into one of the following Category:

-   **Matchable** : These correspond to information provided in the update request, and are used to filter out rules that don't apply to the request
-   **Decision** : These are also used to filter rules, but do not correspond to information in the request
-   **Response** : these contain information that ends up in the response
-   **Info** : Informational columns, not used as part of serving updates

**How are requests matched up to rules?**

The incoming request parts match up directly to incoming URL parts. 
For example, most update requests will send an URL in the following format  

::
    
    /update/3/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/update.xml?force=1

The following logic is used to figure out which rule an update matches and what to respond with:

-   If a rule specifies one of these fields and a request's field doesn't match it, the rule is considered not to be a match and the rule is ignored for that request. 

-   If "force" wasn't specified, the backgroundRate of the selected rule is looked at

-   If we still choose serve an update after accounting for backgroundRate we look at the rule's mapping. This is a foreign key that points at an entry in the releases table. That row has most of the information we need to construct the update.
  
-   Using the update_type and release that the mapping points to, construct and return an XML response with the details of the update for the client

--------
Releases
--------
To Balrog, a "release" is data about a related set of builds. 
This does _not_ match up with the concept of a "release" being on the "beta", "release" or "esr" channel elsewhere. In Balrog, each set of nightlies on any branch is considered a release.

While there's no enforced format on release names, there are a few conventions that we use:

- Nightly-style builds submit to releases named by product and branch. Each nightly generally submits to two different releases, one "dated" (eg: Firefox-mozilla-central-nightly-20150513010203) and one "latest" (eg: Firefox-mozilla-central-nightly-latest).

- Release-style builds submit to releases named by product, version number, and build number, eg: Firefox-38.0-build1

- GMP blobs are created by hand and generally named with the version of each plugin they contain in the name, eg: GMP-20150423-CDM-v4-OpenH264-v1.4

-----------
Permissions
-----------
The permissions table is a simple list of usernames and the ACLs(Access Control Lists) that they have. 
A user could be an "admin", giving them write access to everything, or could have one or more specific permissions. 
These specific ACLs let us do things such as give B2G folks access to Balrog without the risk of them or their tools accidentally messing up Firefox updates.

--------------
History Tables
--------------
Change attribution and recording is embedded deeply into Balrog.
The rules, releases, and permissions tables all have a corresponding history table that records the time a change was made and who made it.
his allows us to look back in time when debugging issues, attribute changes to people (aka blame), and quickly roll back bad changes.




