==============
Database Model
==============


Balrog's model centers around two concepts: Rules and Releases.
When a request for an update from an application is received it is matched up against the rules.
Once the correct rule has been found, it contains a pointer to a Release, which contains all of the metadata needed to construct a proper update response.
Rules and Releases are described in greater detail below:


.. _rulestable:

-----
Rules
-----

The most important part of Balrog to understand is its rules.
When a request comes in it is matched against each of Balrog's rule to find the one that best suits it (more in this below).
Once found, Balrog looks at that rule's "mapping", which points to a release that has the required information to serve an update back to the client.
Without any rules, Balrog will never serve an update.
With badly configured rules Balrog could do bad things like serve Firefox updates to B2G devices.

**What's in a rule?**

Each rule has multiple columns. They all fall into one of the following Category:

-   **Matchable** : These correspond to information provided in the update request, and are used to filter out rules that don't apply to the request
-   **Decision** : These are also used to filter rules, but do not correspond to information in the request
-   **Response** : these contain information that ends up in the response
-   **Info** : Informational columns, not used as part of serving updates


Following tables show columns according to different Categories:

  +------------------------+--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  | Category               | Attribute          | Description                                      | Matching Logic                  | Examples                   |
  +========================+====================+==================================================+=================================+============================+
  | Decision               | backgroundRate     | The percentage of background update requests that| N/A                             | Any number 0 to            |
  |                        |                    | if specified. Generally, this is used as a       |                                 | 100                        |
  |                        |                    | throttle to increase or decrease the rate at     |                                 |                            |
  |                        |                    | which the majority of users receive the latest   |                                 |                            |
  |                        |                    | update.                                          |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | Priority           | The priority of the rule, relative to other      | N/A                             | Any number, by             |
  |                        |                    | rules. If multiple rules match an incoming       |                                 | convention                 |
  |                        |                    | request based on the Matchable columns, the rule |                                 | positive                   |
  |                        |                    | with the highest priority is chosen.             |                                 | integers.                  |
  +------------------------+--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  | Info                   | Alias              | The id of the rule. This id is necessary to      | N/A                             | "firefox-release-betatest" |
  |                        |                    | make changes to the rule through the REST API.   |                                 | , "firefox-nightly"        |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | Comment            | A string describing the purpose of the           | N/A                             | Any string                 |
  |                        |                    | rule. Not always necessary for obvious rules.    |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | id                 | The id of the rule. This id is necessary to      | N/A                             | Autoincrementing           |
  |                        |                    | make changes to the rule through the REST API.   |                                 | integer                    |
  +------------------------+--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  | Matchable              | buildID            | The build ID of the application requesting an    | Exact string match or           | "201410010830"             |
  |                        |                    | update.                                          | operator plus buildid to        | or                         |
  |                        |                    |                                                  | compare the incoming one against| "<201512010830"            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | buildTarget        | The "build target" of the application            | Exact string match only         | "Darwin_x86_64-gcc3-       |
  |                        |                    | requesting an update. This is usually related    |                                 | u-i386-x86_64" or          |
  |                        |                    | to the target platform the app was built for.    |                                 | "flame-kk-userdebug"       |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | Channel            | The update channel of the application request an | Exact string match or a         | "nightly" or "beta*"       |
  |                        |                    | update.                                          | string with "*"                 |                            |
  |                        |                    |                                                  | character to glob               |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | distribution       | The partner distribution name of the application | Exact string match only         | "default" or               |
  |                        |                    | requesting an update or "default" if the         |                                 | "yahoo"                    |
  |                        |                    | application is not a partner build.              |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | distVersion        | The version of the partner distribution of the   | Exact string match only         | "default" or               |
  |                        |                    | application requesting an update or "default"    |                                 | "1.19"                     |
  |                        |                    | if the application is not a partner build.       |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | headerArchitecture | The architecture of the OS of the client as      | Exact string match only         | "PPC" and "Intel"          |
  |                        |                    | guessed based on build target. This field is     |                                 | are the only               |
  |                        |                    | mostly deprecated now that this information is   |                                 | possible values            |
  |                        |                    | included in the build target.                    |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | Locale             | The locale of the application requesting an      | Exact string match or           | "de" or                    |
  |                        |                    | update.                                          | comma separated list of         | "en-US,en-GB,id"           |
  |                        |                    |                                                  | locales to do an exact match on |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | osVersion          | The OS Version of the application requesting an  | Partial string match or         | "Windows_NT 5.0" or        |
  |                        |                    | update. This field is primarily used to point    | comma separated list of         | "Darwin 6,Darwin 7         |
  |                        |                    | desupported operating systems to their last      | partial strings to match on     | ,Darwin 8"                 |
  |                        |                    | supported build.                                 |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | Product            | The name of the application requesting an update.| Exact string match only         | "Firefox" or "B2G"         |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | systemCapabilities | The supported hardware features of the           | Full string match or            | 	"SSE" or "MMX,SSE"        |
  |                        |                    | application requesting an update. This field     | comma separated list of         |                            |
  |                        |                    | is primarily used to point desupported users     | full strings to match on        |                            |
  |                        |                    | based on their hardware. Eg: users who do not    |                                 |                            |
  |                        |                    | support SSE2                                     |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | Version            | The version of the application requesting an     | Exact string match or           | "36.0" or ">=38.0a1"       |
  |                        |                    | update.                                          | operator plus version           |                            |
  |                        |                    |                                                  | to compare the incoming         |                            |
  |                        |                    |                                                  | one against                     |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | Whitelist          | A pointer to a Whitelist blob (stored in the     | If a whitelist is present,      | Any valid release          |
  |                        |                    | Releases table) that can determine whether an    | its shouldServeUpdate is        | name, or NULL              |
  |                        |                    | update request is authorized to have the Release | called. If it returns True,     |                            |
  |                        |                    | this rule is mapped to. Commonly used in         | this rule is considered to      |                            |
  |                        |                    | whitelisting IMEIs for FirefoxOS updates.        | be matching. If it returns      |                            |
  |                        |                    |                                                  | False, this rule is thrown out. |                            |
  +------------------------+--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  | Response               | Fallback Mapping   | The Release to construct an update out of when   | N/A                             | Any valid release          |
  |                        |                    | the user is on the wrong side of a background    |                                 | name, or NULL              |
  |                        |                    | rate dice roll. This is a foreign key to the     |                                 |                            |
  |                        |                    | "name" column of the Releases table.             |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | Mapping            | The Release to construct an update out of if the | N/A                             | Any valid release          |
  |                        |                    | user is on the right side of a background rate   |                                 | name, or NULL              |
  |                        |                    | dice roll, or if the background rate is 100. This|                                 |                            |
  |                        |                    | is a foreign key to the "name" column of the     |                                 |                            |
  |                        |                    | Releases table.                                  |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | update_type        | The update_type to use in the XML response. It's | N/A                             | "minor" or "major"         |
  |                        |                    | very rare for a rule to use anything other than  |                                 |                            |
  |                        |                    | "minor" these days.                              |                                 |                            |
  +------------------------+--------------------+--------------------------------------------------+---------------------------------+----------------------------+



**How are requests matched up to rules?**

The incoming request parts match up directly to incoming URL parts.
For example, most update requests will send a URL in the following format

::

    /update/3/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<distribution>/<distVersion>/update.xml?force=1

The following logic is used to figure out which rule an update matches and what to respond with:

-   If a rule specifies one of these fields and a request's field doesn't match it, the rule is considered not to be a match and the rule is ignored for that request.

-   If "force" wasn't specified, the backgroundRate of the selected rule is looked at

-   If we still choose serve an update after accounting for backgroundRate we look at the rule's mapping. This is a foreign key that points to  an entry in the releases table. That row has most of the information we need to construct the update.

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

The table below describe all possible permissions:

  +------------------------+---------------------+-----------------------------------+-------------------------------+
  | Object                 |  Action             | Options                           | Comments                      |
  +========================+=====================+===================================+===============================+
  | admin                  | No supported actions| products - If specified, the user | An admin user with no options |
  |                        |                     | can perform any actions on Rules  | specified has completely      |
  |                        |                     | or Releases that affect the       | unrestricted access to Balrog |
  |                        |                     | specified products.               |                               |
  +------------------------+---------------------+-----------------------------------+-------------------------------+
  | rule                   | create              | products - If specified, the user |                               |
  |                        +---------------------+ only has permission for the       |                               |
  |                        | modify              | object and action if the changes  |                               |
  |                        +---------------------+ they are making only affect the   |                               |
  |                        | delete              | product specified.                |                               |
  +------------------------+---------------------+                                   |                               |
  | release                | create              |                                   |                               |
  |                        +---------------------+                                   |                               |
  |                        | modify              |                                   |                               |
  |                        +---------------------+                                   |                               |
  |                        | delete              |                                   |                               |
  +------------------------+---------------------+                                   |                               |
  | release_read_only      | set                 |                                   |                               |
  |                        +---------------------+                                   |                               |
  |                        | unset               |                                   |                               |
  +------------------------+---------------------+                                   |                               |
  | release_locale         | modify              |                                   |                               |
  +------------------------+---------------------+-----------------------------------+                               |
  | permission             | create              | No supported options.             |                               |
  |                        +---------------------+                                   |                               |
  |                        | modify              |                                   |                               |
  |                        +---------------------+                                   |                               |
  |                        | delete              |                                   |                               |
  +------------------------+---------------------+-----------------------------------+-------------------------------+
  | scheduled_change       | enact               | No supported options.             | Only the Balrog Agent should  |
  |                        |                     |                                   | be granted this permission.   |
  +------------------------+---------------------+-----------------------------------+-------------------------------+

--------------
History Tables
--------------
Change attribution and recording is embedded deeply into Balrog.
The rules, releases, and permissions tables all have a corresponding history table that records the time a change was made and who made it.
This allows us to look back in time when debugging issues, attribute changes to people (aka blame), and quickly roll back bad changes.

  .. _scheduledChanges:

-----------------
Scheduled Changes
-----------------

Rules may have changes scheduled in advance.
Currently, these changes may only be scheduled based on a timestamp,
but there is the possibility that they could be driven by release uptake, crashes, or other data in the future.
Permissions for Scheduled Changes are inherited from regular Rule permissions.
If you want to schedule a change to a Rule, you must have the right permissions to modify that Rule directly.
No special permission on top of that is needed to schedule a change.
Scheduled Changes are stored in a separate table that mirrors the main Rules table,
and tracks the extra information required to schedule and enact them.


