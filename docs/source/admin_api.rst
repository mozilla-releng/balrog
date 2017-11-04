.. _adminapi:

=========
Admin API
=========

Balrog's Admin app provides an API that allows for retrieval and modification of Rules, Releases, and Permissions.
This page documents all of the available endpoints, their parameters, and responses.
POST and PUT requests may submit parameters as multipart form data or json.

-----
Rules
-----


**/rules**
----------

GET
***

Returns all of the Rules in Balrog's database inside of a JSON Object in the following format:

::

    {
        "count": 2,
        "rules": [
    		{
    		    "rule_id": 1,
      			...
    		},
    		{
      		    "rule_id": 2,
      		    ...
    		}
        ]
    }


POST
****
Creates a new rule with the provided values.
The following parameters are supported:

-   priority (required)
-   backgroundRate (required)
-   mapping
-   alias
-   product
-   version
-   buildID
-   channel
-   locale
-   distribution
-   buildTarget
-   osVersion
-   distVersion
-   comment
-   headerArchitecture

For detailed information on parameters see :ref:`rulestable`


**/rules/<id_or_alias>**
------------------------

GET
***

Returns the entire rule identified by the id or alias given in JSON format. Eg:

::

    {
        "rule_id": 3,
        "product": "Firefox",
        ...
    }

POST
****

Modifies the rule identified by the id or alias given according to the parameters given.
The following parameters are supported:

- 	data_version (required)
-   priority
-   backgroundRate
-   mapping
-   alias
-   product
-   version
-   buildID
-   channel
-   locale
-   distribution
-   buildTarget
-   osVersion
-   distVersion
-   comment
-   headerArchitecture

For detailed information on parameters see :ref:`rulestable`

DELETE
******

Deletes the rule identified by the id or alias given. The following parameters are supported:

-	data_version (required)



**/rules/<id_or_alias>/revisions**
----------------------------------

GET
***

Returns previous versions of the rule identified by the id or alias given in a JSON Object in the following format:

::

    {
        "count": 2,
        "rules": [
        {
            "id": 1,
            "change_id": 4,
            "timestamp": 1451610061000,
            "changed_by": "jane",
            "product": "Firefox",
            ...
        },
        {
            "id": 1,
            "change_id": 4,
            "timestamp": 1451610061000,
            "changed_by": "jane",
            "product": "Firefox",
            ...
        }
        ]
    }

This endpoint supports pagination.
If "page" and "limit" are present in the query args, a slice of the revisions is returned instead of the full history.
Eg: if the page is "2" and the limit is "5", the 6th through 10th revisions would be returned. "count" is not affected by pagination - it will always return the total number of revisions that exist.


POST
****

Reverts the rule identified by the given id (alias is not supported here) to the version identified by the change_id given in the request body.
The request body must be a JSON object containing a "change_id" key.


**/rules/columns/<column>**
---------------------------

GET
***

Returns a JSON Object containing the unique values for the given column.
For example, /rules/columns/product would return something like:

::

    {
      "count": 10,
      "product": [
        "Firefox",
        "Graphene",
        "Thunderbird",
        "MetroFirefox",
        "Horizon",
        "B2G",
        "GMP",
        "Fennec",
        "SystemAddons",
        "B2GDroid"
      ]
    }


--------
Releases
--------

**/releases**
-------------

GET
***

Returns a JSON Object containing metadata about Releases in Balrog's database.
Due to its size, the actual Release "blob" is never returned from this endpoint.
There are a few query arguments that affect its response.
If no arguments are provided, it returns information about all of the Releases in the database in the following format:

::

    {
      "releases": [
        {
          "name": "Firefox-34.0-build1",
          "product": "Firefox",
          "data_version": 4,
          "read_only": null
        },
        {
          "name": "Fennec-34.0-build1",
          "product": "Fennec",
          "data_version": 43,
          "read_only": true
          },
          ...
      ]
    }



If "product" is passed, only Releases with the given product name will be returned.
If "name_prefix" is passed, only Releases whose name starts with the given prefix will be returned.
If "names_only" is set to true, the response changes format and provides a list of all of the Release names in the database:

::

    {
      "names": [
        "Firefox-34.0-build1",
        "Fennec-34.0-build1",
        ...
       ]
    }


POST
****

Creates a new Release with the provided values. The following parameters are supported:

-	name (required)
-	product (required)
-	blob (required)


**/releases/<release>**
-----------------------

GET
***

Returns the "data" portion of the named Release, which is a JSON Object.
If "pretty" is present in the query string and set to true, it will be pretty formatted. For example:

::

    {
      "name": "Firefox-mozilla-central-nightly-latest",
      "schema_version": 4,
      "platforms": {
        "WINNT_x86-msvc": {
        ...
        }
      }
    }


PUT
***

Overwrites the named Release with the data given.
The "blob" field is completely overridden with the new one, not updated.
If the Release does not exist, it is created. The following parameters are supported:

-	name (required)
-	product (required)
-	blob (required)
-	data_version (required if the Release already exists)

POST
****

Updates the named Release with the data given.
The "blob" field is updated with the new one instead of being completely overridden.
If the Release does not exist, it is created.
The following parameters are supported:

-	product (required)
-	data (required)
-	data_version (required if the Release already exists)
-	hashFunction
-	schema_version
-	copyTo
-	alias

DELETE
******

Deletes the named Release.
The following parameters are supported:

- data_version (required)


**/releases/<release>/read_only**
---------------------------------

GET
***

Returns whether or not the named Release is marked as read_only. Eg:

::

    {
      "read_only": true
    }


**/releases/<release>/builds/<platform>/<locale>**
--------------------------------------------------

GET
***

Returns the platform+locale specific data of the named Release, which is a JSON Object. Eg:


::

    {
      "buildID": "20160329030246",
      "appVersion": "48.0a1",
      "displayVersion": "48.0a1",
      "platformVersion": "48.0a1",
      "partials": [
        {
            "fileUrl": "https://mozilla-nightly-updates.s3.amazonaws.com/mozilla-central/20160329030246/Firefox-mozilla-central-48.0a1-win32-de-20160327030437-20160329030246.partial.mar?versionId=uIza17vCjTuL6XVvCvtpzlVVQSelUdJm",
            "from": "Firefox-mozilla-central-nightly-20160327030437",
            "hashValue": "0d36245eedef3bfce927339ee89da58400f8afa5a8cc8b4323f7407660f291bbfa1f00527665d5f16614de679723b874d92d650dbf319ffbfa1e672729ba09c9",
            "filesize": 10388948
        }
      ],
      "completes": [
        {
            "fileUrl": "https://mozilla-nightly-updates.s3.amazonaws.com/mozilla-central/20160329030246/Firefox-mozilla-central-48.0a1-win32-de.complete.mar?versionId=sdNQURDy9.8GH3P4SLdO1V.XtA9MLIzu",
            "from": "*",
            "hashValue": "981082f1b7f5264d88aa017f45362aac362990842b82a0934e70506c1536304b0fda6beb229b7ef56b153d71b69669cc92b5f2987d282cc026e9ed993b88e582",
            "filesize": 53656493
        }
      ]
    }


PUT
***

Sets or unsets the read_only flag of the named Release.
The following parameters are supported:

-	name (required)
-	data_version (required)
-	read_only


**/releases/<release>/revisions**
---------------------------------

GET
***

Returns previous versions of the named Release in a JSON Object in the following format:

::

    {
      "count": 1
      "rules": [
        {
          "id": 1,
          "change_id": 4,
          "timestamp": 1451610061000,
          "changed_by": "jane",
          "product": "Firefox",
          ...
        }
      ]
    }


This endpoint supports pagination.
If "page" and "limit" are present in the query args, a slice of the revisions are returned instead of the full history.
Eg: if the page is "2" and the limit is "5", the 6th through 10th revisions would be returned. "count" is not affected
by pagination - it will always return the total number of revisions that exist.

POST
****

Reverts the named Release to the version identified by the change_id given in the request body.
The request body must be a JSON object containing a "change_id" key.


**/releases/columns/<column>**
------------------------------

GET
***
Returns a JSON Object containing the unique values for the given column.
For example, /releases/columns/product would return something like:
vpn
::

    {
      "count": 10,
      "product": [
        "Firefox",
        "Graphene",
        "Thunderbird",
        "MetroFirefox",
        "Horizon",
        "B2G",
        "GMP",
        "Fennec",
        "SystemAddons",
        "B2GDroid"
      ]
    }


-----
Users
-----

**/users**
----------

GET
***

Returns all of the users known to Balrog inside of a JSON Object in the following format:

::

    {
      "users": [
        "bhearsum@mozilla.com",
        "ffxbld",
        "nthomas@mozilla.com",
        ...
      ]
    }


Note that Balrog only tracks permissions, not accounts, so this list does not include users who are able to log in, but have no permissions to change anything.

**/users/<username>/permissions**
---------------------------------

GET
***

Returns all of the permissions that the given username has been granted in a JSON Object in the following format:

::

    {
      "/releases/:name": {
        "data_version": 1,
        "options": {
          "method": "POST,
          "product": [
            "Firefox",
            "Fennec"
          ]
        }
      },
        ...
    }


**/users/<username>/permissions/<permission>**
----------------------------------------------

GET
***

Returns the details of the named permission for the username given in a JSON Object in the following format:

::

    {
      "data_version": 1,
      "options": {
        "method": "POST,
        "product": [
          "Firefox",
          "Fennec"
        ]
      }
    }

PUT
***

Overwrites the details of named permission for the username given. If the permission does not exist, it is created. The following parameters are supported:

-	data_version (required if the permission already exists)
-	options

POST
****

Overwrites the details of named permission for the username given. The following parameters are supported:

-	data_version (required)
-	options

DELETE
******

Deletes the named permission for the username given. The following parameters are supported:

-	data_version (required)

**/users/<username>/roles**
---------------------------------

GET
***

Returns all of the roles that the given username holds in a JSON Object in the following format:

::

    {
      "roles": [
        "qa",
        "releng"
      ]
    }


**/users/<username>/roles/<role>**
----------------------------------------------

PUT
***

Grants the given username the given role. If the user already holds that role, this is a no-op.

DELETE
******

Revokes the given role from the given username. The "data_version" parameter must be provided.


-------------------------
Product Required Signoffs
-------------------------

Endpoints to view and create new :ref:`product_rs_table`. In most cases, these will be managed with :ref:`scheduledChangesApi` instead, because they themselves require signoff.

**/required_signoffs/product**
------------------------------

GET
***

Returns all of the :ref:`product_rs_table`. Example response:

::

    {
      "count": 2,
      "required_signoffs": [
        {
          "product": "Firefox",
          "channel": "release",
          "role": "releng",
          "signoffs_required": 2,
          "data_version": 1
        },
        {
          "product": "Firefox",
          "channel": "release",
          "role": "relman",
          "signoffs_required": 1,
          "data_version": 1
        }
      ]
    }

POST
****

Create a new Product Required Signoff. "product", "channel", "role", and "signoffs_required" are all required. If the product and channel provided already require signoff, a 400 will be returned (you must use a Scheduled Change and meet the existing signoff requirements to modify Required Signoffs for things that already require it).


-----------------------------
Permissions Required Signoffs
-----------------------------

Endpoints to view and create new :ref:`permissions_rs_table`. In most cases, these will be managed with :ref:`scheduledChangesApi` instead, because they themselves require signoff.

**/required_signoffs/permissions**
------------------------------

GET
***

Returns all of the :ref:`permissions_rs_table`. Example response:

::

    {
      "count": 2,
      "required_signoffs": [
        {
          "product": "Firefox",
          "role": "releng",
          "signoffs_required": 3,
          "data_version": 1
        },
        {
          "product": "SystemAddons",
          "role": "gofaster",
          "signoffs_required": 2,
          "data_version": 1
        }
      ]
    }

POST
****

Create a new Permissions Required Signoff. "product", "role", and "signoffs_required" are all required. If the product provided already requires a signoff, a 400 will be returned (you must use a Scheduled Change and meet the existing signoff requirements to modify Required Signoffs for things that already require it).


.. _scheduledChangesApi:

-----------------
Scheduled Changes
-----------------

Endpoints to create and manage :ref:`scheduledChanges` and Signoffs. Each type of object that supports Scheduled Changes has its own set of endpoints. These objects are:

- rules (:ref:`rulestable`)
- releases (:ref:`releasestable`)
- permissions (:ref:`permissionstable`)
- required_signoffs/product (:ref:`product_rs_table`)
- required_signoffs/permissions (:ref:`permissions_rs_table`)

**/scheduled_changes/<object>**
-------------------------------

GET
***

Returns the Scheduled Changes for the named object. If the query arg "all" evaluates to True, Scheduled Changes that have been enacted
will be returned along with pending ones. If "all" evaluates to False, only active Scheduled Changes will be returned. Example response:

::

    {
        "count": 2,
        "scheduled_changes": [
        {
            "sc_id": 1,
            "when": 100000,
            "complete": True,
            "scheduled_by": "janet",
            "signoffs": {
                "janet": "relman"
            },
            # base attributes follow...
        },
        {
            "sc_id": 2,
            "when": 20000000000,
            "complete": False,
            "scheduled_by": "charlie",
            "signoffs": {
                "charlie": "releng",
                "janet": "relman"
            },
            # base attributes follow...
        }
        ]
    }

POST
****

Creates a new Scheduled Change for the named object. The following parameters are supported:

- when
- telemetry_product
- telemetry_channel
- telemetry_uptake

Either "when" or the full set of "telemetry" parameters must be provided as a condition. Details of the object to be created or modified are also required. Eg, "product", "channel", "priority", "backgroundRate" and "mapping" might be included if a Scheduled Change for a Rule was being created.

**/scheduled_changes/<object>/<sc_id>**
---------------------------------------

POST
****

Modifies an existing Scheduled Change for the named object. Supported parameters are the same as /scheduled_changes/<object> POST.

DELETE
******

Deletes the given Scheduled Change for the named object. "data_version" must be provided.

**/scheduled_changes/<object>/<sc_id>/enact**
---------------------------------------------

POST
****

Enacts the given Scheduled Change for the named object. This endpoint should only be used by the :ref:`balrog_agent`.

**/scheduled_changes/<object>/<sc_id>/signoffs**
------------------------------------------------

POST
****

Signs off on the given Scheduled Change for the named object. "role" must be provided in the request body.

DELETE
******

Removes an existing Signoff from the Scheduled Change for the named object.

**/scheduled_changes/<object>/<sc_id>/<id>/revisions**
------------------------------------------------------

GET
***

Returns previous versions of the scheduled change identified by the id given in a JSON Object in the following format:

::

    {
        "count": 2,
        "scheduled_changes": [
        {
            "change_id": 4,
            "timestamp": 1451610061000,
            "changed_by": "jane",
            "sc_id": 1,
            "complete": False,
            "when": 1000000000,
            "scheduled_by": "jane",
            "signoffs": {
                "jane": "relman"
            },
            # base attributes follow...
        },
        {
            "change_id": 4,
            "timestamp": 1451610061000,
            "changed_by": "jane",
            "sc_id": 1,
            "complete": False,
            "when": 2000000000,
            "scheduled_by": "jane",
            "signoffs": {
                "jane": "relman"
            },
            # base attributes follow...
        }
        ]
    }

This endpoint supports pagination.
If "page" and "limit" are present in the query args, a slice of the revisions is returned instead of the full history.
Eg: if the page is "2" and the limit is "5", the 6th through 10th revisions would be returned. "count" is not affected by pagination - it will always return the total number of revisions that exist.


POST
****

Reverts the scheduled change identified by the given sc_id to the version identified by the change_id given in the request body.
The request body must be a JSON object containing a "change_id" key.


------
Others
------

**/csrf_token**
---------------


GET
***

Returns an empty response with a valid CSRF token in the X-CSRF-Token header.

**/history/view/<object>/<change_id>/<field>**
----------------------------------------------

GET
***

Returns the value of the named field from the named object at the specified change_id.

**/history/diff/<object>/<change_id>/<field>**
----------------------------------------------

GET
***

Returns a diff of the value of the named field from the named object at the specified change_id vs. the previous change to that object.
