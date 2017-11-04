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
When a request comes in it is matched against Balrog's rules to find the one that best suits it (more on this in :ref:`How are requests match to a rule?`).
Once found, Balrog looks at that rule's "mapping", or "fallbackMapping", which points to a release that has the required information to serve an update back to the client.
Without any rules, Balrog will never serve an update.
With badly configured rules Balrog could do bad things like serve Firefox updates to Thunderbird users.


*****************
What's in a rule?
*****************

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
  |                        | channel            | The update channel of the application request an | Exact string match or a         | "nightly" or "beta*"       |
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
  |                        | locale             | The locale of the application requesting an      | Exact string match or           | "de" or                    |
  |                        |                    | update.                                          | comma separated list of         | "en-US,en-GB,id"           |
  |                        |                    |                                                  | locales to do an exact match on |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | osVersion          | The OS Version of the application requesting an  | Simplified boolean string       | "Windows_NT 5.0" or        |
  |                        |                    | update. This field is primarily used to point    | match. '&&' ANDs terms while    | "Darwin 6,Darwin 7," or    |
  |                        |                    | desupported operating systems to their last      | ',' ORs them. Terms are matched | "Windows && (websense-"    |
  |                        |                    | supported build.                                 | using partial strings.          |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | product            | The name of the application requesting an update.| Exact string match only         | "Firefox" or "B2G"         |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | instructionSet     | The most modern instruction set supported by the | Full string match or comma      | "SSE" or "MMX,SSE"         |
  |                        |                    | client requesting an update. This field          | separated list of full strings  |                            |
  |                        |                    | is primarily used to desupport users             | to match on                     |                            |
  |                        |                    | based on their hardware. Eg: users who do not    |                                 |                            |
  |                        |                    | support SSE2                                     |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | memory             | The amount of RAM, in megabytes, that the client | Exact match or operator plus    | "8096" or "<8096" or       |
  |                        |                    | requesting the update has                        | memory to compare the incoming  | ">=8096"                   |
  |                        |                    |                                                  | one against                     |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | jaws               | Whether or not the the Rule should apply to      | Exact match only                | True, False, or NULL       |
  |                        |                    | queries that indicate a client thas has an       |                                 |                            |
  |                        |                    | incompatible version of the JAWS screen reader   |                                 |                            |
  |                        |                    | installed. If set to True or False the Rule and  |                                 |                            |
  |                        |                    | the query must match precisely.                  |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | mig64              | Whether or not the Rule should apply to queries  | Exact match only                | True, False, or NULL       |
  |                        |                    | that have opted into 32 -> 64-bit migration.     |                                 |                            |
  |                        |                    | If set to True or False the Rule and the query   |                                 |                            |
  |                        |                    | must match precisely.                            |                                 |                            |
  |                        +--------------------+--------------------------------------------------+---------------------------------+----------------------------+
  |                        | version            | The version of the application requesting an     | Exact string match or exact     | "36.0" or "36.0,36.1,36.2" |
  |                        |                    | update.                                          | matches from list of values or  | or ">=38.0a1"              |
  |                        |                    |                                                  | operator plus version           |                            |
  |                        |                    |                                                  | to compare the incoming         |                            |
  |                        |                    |                                                  | one against                     |                            |
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


*********************************
How are requests match to a rule?
*********************************

Most of the Matchable database fields are present as distinct parts of the update URL. For example, most update requests will send a URL in the following format

::

    /update/6/<product>/<version>/<buildID>/<buildTarget>/<locale>/<channel>/<osVersion>/<systemCapabilities>/<distribution>/<distVersion>/update.xml?force=1

There are a few special cases to consider:

-   systemCapabilities contains comma separated data and breaks down into multple database columns (instructionSet, memory, jaws)

-   headerArchitecture is extracted from the User-Agent header

-   mig64 is optional, and comes from the query string instead of the path


The following logic is used to figure out which rule a request matches, and how to respond:

-   Retrieve all rules where product, buildTarget, distribution, and distVersion are (each) unspecified, or match the request with a simple string match.

-   Discard any rules where the rule specifies a channel, version, buildID, osVersion, any part of systemCapabilities, and/or locale, and that doesn't match the request. The method for each match is described in the table above.

    -   The channel has special handling to try "falling back" to a simpler channel, for example a request with release-cck-foo will also consider rules for 'release'. This only applies to channels containing '-cck-'.

-   Sort the remaining rules by priority, and keep the one with highest.

-   The rule's value for backgroundRate modifies the response

    - if the request has a query parameter force=1 then the background rate is ignored, and all requests will be served using the release in Mapping

    - if force is absent then backgroundRate is the percentage of requests which will be served using Mapping

    - the remaining requests will be served fallbackMapping, if that is specified on the rule, otherwise nothing.

-   The Release, combined with the update_type specified by the rule, is used to construct an XML response with the details of the update.


*************
Rules example
*************

Rules are usually set up like this, in increasing order of priority:

-   The lowest priority rule is the main path, providing the latest release for a channel

-   Special cases are slightly higher, e.g. whatsnew pages for some locales

-   Watersheds are higher again, to ensure that older release update to the watershed first. The older the watershed the higher the priority, so that X --> Y --> Z is preserved.

-   The oldest operating system deprecations are highest priority.

Here is a simplified set of rules for Firefox on the release channel, with a throttled main release, a Windows-specific watershed, and the deprecation of Windows 98 along time ago. All other values unspecified, except for update_type being 'minor' for all rules.

  +----------+---------+----------+-----------+------------+-----------------------+-----------------------+-----------------+
  | Priority | Product | Channel  | Version   | OS Version | Mapping               | Fallback Mapping      | Background Rate |
  +==========+=========+==========+===========+============+=======================+=======================+=================+
  |      400 | Firefox | release* |           | Windows_98 | No-Update             |                       |             100 |
  +----------+---------+----------+-----------+------------+-----------------------+-----------------------+-----------------+
  |      300 | Firefox | release  | < 43.0.1  | Windows_NT | Firefox-43.0.1-build1 |                       |             100 |
  +----------+---------+----------+-----------+------------+-----------------------+-----------------------+-----------------+
  |      100 | Firefox | release  |           |            | Firefox-51.0.1-build3 | Firefox-50.1.0-build2 |              25 |
  +----------+---------+----------+-----------+------------+-----------------------+-----------------------+-----------------+

The first two rules are static, while the last has the two mapping values updated as new releases are created.
Future watersheds would be placed with priority below 300, while special cases are closer to 100.


.. _releasestable:

--------
Releases
--------

To Balrog, a "release" is data about a related set of builds.
This does _not_ match up with the concept of a "release" being on the "beta", "release" or "esr" channel elsewhere. In Balrog, each set of nightlies on any branch is considered a release.

While there's no enforced format on release names, there are a few conventions that we use:

- Nightly-style builds submit to releases named by product and branch. Each nightly generally submits to two different releases, one "dated" (eg: Firefox-mozilla-central-nightly-20150513010203) and one "latest" (eg: Firefox-mozilla-central-nightly-latest).

- Release-style builds submit to releases named by product, version number, and build number, eg: Firefox-38.0-build1

- GMP blobs are created by hand and generally named with the version of each plugin they contain in the name, eg: GMP-20150423-CDM-v4-OpenH264-v1.4


.. _permissionstable:

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
  +------------------------+---------------------+                                   |                               |
  | required_signoff       | create              |                                   |                               |
  |                        +---------------------+                                   |                               |
  |                        | modify              |                                   |                               |
  |                        +---------------------+                                   |                               |
  |                        | delete              |                                   |                               |
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


----------
User Roles
----------

Users may hold any number of Roles. Roles are used when signing off on Scheduled Changes.

Roles and Permissions are not directly related - assigning a User a Role does not inherently grant them any Permissions.


-----------------
Required Signoffs
-----------------

Some types of changes to Balrog's database require more than one person to approve them before they can be done. The Required Signoffs tables specify how many signoffs are needed from different Roles for each type of change. For example, a change may required 3 signoffs from users that hold the "releng" Role as well as 1 signoff from a user that holds the "relman" role.

Changes to Required Signoffs tables generally require signoff as well. If you are adding, modifying, or removing signoff requirements for something that already has signoff requirements, you must obtain signoff to do so. For example, if a change requires 2 signoffs from users who hold the "releng" Role, and you want to also require signoff from 1 user who holds the "relman" Role, you must get signoff from 2 "releng" users first. The one exception to this is that if you are adding a new signoff requirement for something that doesn't require any signoff yet, you do not need any signoff to do so.

You cannot require more signoffs than a Role has users. Eg: if only 3 users hold the "releng" Role, you cannot require 4 "releng" signoffs for anything. Similarly, if 3 "releng" signoffs are currently required for something, and 3 users hold that Role, you cannot remove that Role from any user.

Changes that require signoff will either be Product changes or Permissions changes. Required Signoffs for each are managed independently, and described in more detail below.


.. _product_rs_table:

*************************
Product Required Signoffs
*************************

Changes that directly affect updates that clients receive (the Rules and Releases tables) are considered Product changes. Our paranoia level for changes to these varies greatly depending on the Product and Channel. Eg: we're far more concerned about changes to Firefox's release channel than we are about Thunderbird's nightly channel. Because of this, we specify Required Signoffs for these with a product and channel combination.

Any changes to a Rule that would affect a product and channel combination specified in this table will require signoff. This includes Rules that don't specify a product or channel at all (because that is treated as a wildcard).

Releases which are mapped to be a Rule's mapping or fallbackingMapping field require the same signoffs as the Rule. Releases that are not mapped to by a rule never require any signoff. It's important that they are inspected before mapping to them for the first time.

If a change affects more than one product and channel combination, *all* affected combinations' required signoffs will be combined to find the full set of required. For example, if Firefox's release channel requires 3 signoffs from "relman" and Firefox's beta channel requires 2 signoffs from "releng", a change to a Rule that affects both channels will require 3 signoffs from "relman" and 2 from "releng". Changing a Release that is mapped to by Rules on the "release" and "beta" channel would also require the same signoffs.


.. _permissions_rs_table:

*****************************
Permissions Required Signoffs
*****************************

Changes to the Permissions table may also require signoff. These Required Signoffs are specified by product, which most Permissions support as an option. Changing a Permission that affects the named product wil require the signoffs from the Roles specified in this table. Changing a Permission that does not specify a product will require signoff the signoffs from *all* Roles specified in this table, because such Permissions grant access to all products. This includes the "admin" Permission and "permission" Permission, which are often used without a product specified.


--------------
History Tables
--------------
Change attribution and recording is embedded deeply into Balrog.
The rules, releases, permissions, required signoffs, and all associated scheduled changes tables have a corresponding history table that records the time a change was made and who made it.
This allows us to look back in time when debugging issues, attribute changes to people (aka blame), and quickly roll back bad changes.

  .. _scheduledChanges:

-----------------
Scheduled Changes
-----------------

Some tables (Rules, Releases, and Permissions) support having changes to them scheduled in advance. Tables with Scheduled Changes enabled will have additional related tables to store the necessary information about them.

The primary Scheduled Changes table stores the desired new version of the object and the user who scheduled it. The Conditions table stores information about when to enact the Scheduled Change. Finally, the Signoffs table stores information about who (if anybody) has signed off on the Scheduled Change. All of these tables have their own History tables too.

Permissions for Scheduled Changes are inherited from their asociated base table. Eg: to scheduled a change to a Rule, you must have permission to modify that Rule directly. No special permission is required on top of that.
