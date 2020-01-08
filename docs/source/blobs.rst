=====
Blobs
=====

Balrog's Blobs are classes that encapsulate the logic pertaining to a type of Release.
Blobs are responsible for defining their own data structure format (with a jsonschema), the response format, and making decisions about when a response should be returned.
This page documents the Blobs we have in Balrog, what they're used for, and what responses from them look like.

App Release
-----------

App Release blobs are used for Gecko Application updates - generally anything that receives updates through MAR files (eg: Firefox, Fennec, Thunderbird).
Each App Release Blob contains all of the metadata for all platforms and locales of a particular release.
There are many versions of the App Release blob to support the various Firefox versions, and implement various Balrog features.

Schema 1
********
Legacy format to support Firefox 1.5 through 3.6.x and Thunderbird 1.5 to 3.1.y.

Schema 2
********
Compatible with Firefox and Thunderbird 4.0 and above.

Supports client side changes from https://bugzilla.mozilla.org/show_bug.cgi?id=530872

Changes from V1:

* appv and extv become appVersion, platformVersion, and displayVersion
* Added actions, billboardURL, openURL, notificationURL, alertURL, showPrompt, showNeverForVersion, isOSUpdate
* Removed oldVersionSpecialCases

Schema 3
********
Compatible with Firefox and Thunderbird 4.0 and above.

This was an internal change to add multiple partials support to Balrog. It replaces the "partial" and "complete"
properties at the local level with new "partials" and "completes" properties.

Schema 4
********
Compatible with Firefox and Thunderbird 4.0 and above.

This was an internal change to add support for pushing release channel builds to the beta channel. It replaces the
top level "fileUrls", "bouncerProducts", and "ftpFilenames" properties with a single, unified "fileUrls" properties.

Here is an example that shows the :ref:`appreleaseExample`, with all of its platforms and locales.

Schema 5
********
Compatible with Firefox and Thunderbird 19.0 and above.

Driven by a client side change made in https://bugzilla.mozilla.org/show_bug.cgi?id=813322 that added support for
the optional "promptWaitTime" attribute.

Schema 6
********
Compatible with Firefox and Thunderbird 51.0 and above.

This version removes support for platformVersion, billboardURL, licenseURL, version, and extensionVersion which are
no longer supported by the client.

Schema 7
********
This schema was never used and no longer exists. It was briefly added to support the backgroundInterval attribute
which was never used.

Schema 8
********
Compatible with Firefox and Thunderbird 51.0 and above.

This was an internal change to add support for the binary transparency attributes (https://bugzilla.mozilla.org/show_bug.cgi?id=1384296).

Schema 9
********
Compatible with Firefox and Thunderbird 51.0 and above.

This was an internal change to allow the App Release blob to make decisions about when to return most <update> parameters. Most notably,
it allows us to return (or not) What's New Pages based on incoming client information. This work happened in https://bugzilla.mozilla.org/show_bug.cgi?id=1400016.

Here is an example that shows a single :ref:`appreleasev9Example` that supports both WNP and no-WNP updates.

Response Format (App Release)
*****************************

The response for App Releases is as follows (different versions of the App Release blob use different <update> line parameters, but the general structure is consistent):

.. code-block:: xml

    <updates>
        <update type="minor" displayVersion="43.0.2" appVersion="43.0.2" platformVersion="43.0.2" buildID="20151221130713" detailsURL="https://www.mozilla.org/en-US/firefox/43.0.2/releasenotes/">
            <patch type="complete" URL="http://download.mozilla.org/?product=firefox-43.0.2-complete&os=osx&lang=en-US&force=1" hashFunction="sha512" hashValue="781478556846b719ebc906a8a9613a421e24449b4456c4ccee990e878b3be9fb0478a78821a499a4c1f1a76d75078acf3fdfa3d0be69d2f6c94e3b6340fc935b" size="80329415"/>
            <patch type="partial" URL="http://download.mozilla.org/?product=firefox-43.0.2-partial-41.0.2&os=osx&lang=en-US&force=1" hashFunction="sha512" hashValue="6edd0803e36a03117e12a36e9fc8941e8f6321071fb00c7e8489f67b332d1cbfa95d00218e5c1b61115752fc0aecde8b2535424c521d45530455a4c5d571f889" size="39520883"/>
        </update>
    </updates>

Some responses may have only a type="complete" patch line, but if an <update> line is included it must have at least a <patch> block whose type="complete".


GMP/System Addons
-----------------

GMP and System Addon updates are very similar in that they both provide a list of the latest version of addons/plugins that Firefox should install.
Although the payloads they point to are different, the data structure and response are exactly the same, so they share a Blob.
Here is an example that shows a :ref:`gmpExample` that serves OpenH264 and CDM updates.

Response Format (GMP/System Addons)
***********************************

The response format for GMP and System Addons is as follows:


.. code-block:: xml

    <updates>
        <addons>
            <addon id="gmp-eme-adobe" URL="https://cdmdownload.adobe.com/firefox/win/x86/primetime_gmp_win_x86_gmc_30527.1.zip" hashFunction="sha512" hashValue="d0077885971419a5db8e8ab9f0cb2cac236be98497aa9b6f86ff3b528788fc01a755a8dd401f391f364ff6e586204a766e61afe20cf5e597ceeb92dee9ed1ebc" size="3696996" version="15"/>
            <addon id="gmp-gmpopenh264" URL="http://ciscobinary.openh264.org/openh264-win32-2706e36bf0a8b7c539c803ed877148c005ffca59.zip" hashFunction="sha512" hashValue="45124a776054dcfc81bfc65ad4ff85bd65113900c86f98b70917c695cd9d8924d9b0878da39d14b2af5708029bc0346be6d7d92f1d856443b3051f0d3180894d" size="341180" version="1.5.3"/>
        </addons>
    </updates>


Similar to App Release blobs, not all <addon> lines are required, but if an <addons> block is present, at least one <addon> must be inside of it.
There is no limit to the number of <addon> blocks that can be in a response, but each one must have a unique "id".


Superblobs
----------

Superblobs are used to serve multiple updates for GMP and System Addons releases.
They point at the releases that should be severed for the respective query.

Superblob Example
*****************

.. code-block:: json

  {
    "products": [
      "CDM",
      "OpenH264",
      "Widevine"
    ],
    "name": "GMP-Superblob",
    "schema_version": 4000
  }
