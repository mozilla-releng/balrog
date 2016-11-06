
.. _rulestable:

===========
Rules Table
===========

Each rule has mulitple columns. They all fall into one of the following Category:

-   **Matchable** : These correspond to information provided in the update request, and are used to filter out rules that don't apply to the request
-   **Decision** : These are also used to filter rules, but do not correspond to information in the request
-   **Response** : these contain information that ends up in the response
-   **Info** : Informational columns, not used as part of serving updates

**Different columns in the above categories are:**


--------------------
Category : Matchable
--------------------

1. Product
^^^^^^^^^^
    - **Description** : The name of the appliaction requesting an update

    - **Mactching Logic** : Exact string match only

    - **Examples** : "Firefox" or "B2G"

2. Version
^^^^^^^^^^
    - **Description** : The version of the application requesting an update

    - **Mactching Logic** : Exact string match or operator plus version to compare the incoming one against

    - **Examples** : "36.0" or ">=38.0a1"

3. Channel
^^^^^^^^^^

    - **Description** : The update channel of the application request an update.

    - **Mactching Logic** : Exact string match or a string with "*" character to glob

    - **Examples** : "nightly" or "beta*"

4. buildTarget
^^^^^^^^^^^^^^

    - **Description** : The "build target" of the application requesting an update. This is usually related to the target platform the app was built for

    - **Mactching Logic** : Exact string match only

    - **Examples** : "Darwin_x86_64-gcc3-u-i386-x86_64" or "flame-kk-userdebug"


5. buildID
^^^^^^^^^^

    - **Description** : The build ID of the application requesting an update

    - **Mactching Logic** : Exact string match or operator plus buildID to compare the incoming one against

    - **Examples** : "201410010830" or "<201512010830"

6. Locale
^^^^^^^^^

    - **Description** : The locale of the application requesting an update.

    - **Mactching Logic** : Exact string match or comma separated list of locales to do an exact match on

    - **Examples** : "de" or "en-US,en-GB,id"

7. osVersion
^^^^^^^^^^^^

    - **Description** : The OS Version of the application requesting an update. This field is primarily used to point desupported operating systems to their last supported build.

    - **Mactching Logic** : Partial string match or comma separated list of partial strings to match on

    - **Examples** : "Windows_NT 5.0" or "Darwin 6,Darwin 7,Darwin 8"

8. systemCapabilities
^^^^^^^^^^^^^^^^^^^^^

    - **Description** : The supported hardware features of the application requesting an update. This field is primarily used to point desupported users based on their hardware. Eg: users who do not support SSE2

    - **Mactching Logic** : Full string match or comma separated list of full strings to match on

    - **Examples** : "SSE" or "MMX,SSE"


9. distribution
^^^^^^^^^^^^^^^

    - **Description** : The partner distribution name of the application requesting an update or "default" if the application is not a partner build.

    - **Mactching Logic** : Exact string match only

    - **Examples** : "default" or "yahoo"

10. distVersion
^^^^^^^^^^^^^^^

    - **Description** : The version of the partner distribution of the application requesting an update or "default" if the application is not a partner build.

    - **Mactching Logic** : Exact string match only

    - **Examples** : "default" or "1.19"

11. headerArchitecture
^^^^^^^^^^^^^^^^^^^^^^

    - **Description** : The architecture of the OS of the client as guessed based on build target. This field is mostly deprecated now that this information is included in the build target.

    - **Mactching Logic** : Exact string match only

    - **Examples** : "PPC" and "Intel" are the only possible value

12. Whitelist
^^^^^^^^^^^^^

    - **Description** : A pointer to a Whitelist blob (stored in the Releases table) that can determine whether an update request is authorized to have the Release this rule is mapped to.

    - **Mactching Logic** : If a whitelist is present, its shouldServeUpdate is called. If it returns True, this rule is considered to be matching. If it returns False, this rule is thrown out.

    - **Examples** : Any valid release name, or NULL

-------------------
Category : Decision
-------------------

1. Priority
^^^^^^^^^^^
    - **Description** : The priority of the rule, relative to other rules. If multiple rules match an incoming request based on the Matchable columns, the rule with the highest priority is chosen.

    - **Value** : Any number, by convention positive integers.


2. backgroundRate
^^^^^^^^^^^^^^^^^
    - **Description** : The percentage of background update requests that should receive the latest update if they match this rule. Others receive the update from Fallback Mapping, if specified. Generally, this is used as a throttle to increase or decrease the rate at which the majority of users receive the latest update.

    - **Value** : Any number 0 to 100


-------------------
Category : Response
-------------------

1. Mapping
^^^^^^^^^^

    - **Description** : The Release to construct an update out of if the user is on the right side of a background rate dice roll, or if the background rate is 100. This is a foreign key to the "name" column of the Releases table.

    - **Value** : Any valid release name, or NULL.


2. Fallback Mapping
^^^^^^^^^^^^^^^^^^^

    - **Description** : The Release to construct an update out of when the user is on the wrong side of a background rate dice roll. This is a foreign key to the "name" column of the Releases table.

    - **Value** : Any valid release name, or NULL.


3. update_type
^^^^^^^^^^^^^^

    - **Description** : The update_type to use in the XML response. It's very rare for a rule to use anything other than "minor" these days.

    - **Value** : "minor" or "major"

---------------
Category : info
---------------

1. id
^^^^^

    - **Description** : The id of the rule. This id is necessary to make changes to the rule through the REST API.

    - **Value** : Autoincrementing integer

2. Alias
^^^^^^^^

    - **Description** : A unique alias for the rule. Can be used in place of id in any REST operation that doesn't involve rule history.

    - **Examples** : "firefox-release-betatest", "firefox-nightly"

3. Comment
^^^^^^^^^^

    - **Description** : A string describing the purpose of the rule. Not always necessary for obvious rules.

    - **Value** : Any string


