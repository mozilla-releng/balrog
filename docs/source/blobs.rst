=====
Blobs
=====

Balrog's Blobs are classes that encapsulate the logic pertaining to a type of Release.
Blobs are responsible for defining their own data structure format (with a jsonschema), the response format, and making decisions about when a response should be returned.
This page documents the Blobs we have in Balrog, what they're used for, and what responses from them look like.

App Release
-----------

App Release blobs are used for Gecko Application updates - generally anything that receives updates through MAR files (eg: Firefox, Fennec, B2G, Thunderbird).
Each App Release Blob contains all of the metadata for all platforms and locales of a particular release.
Here is an example that shows the Firefox-43.0.2-build1 blob, with all of its platforms and locales.

Response Format
***************

The response for App Releases is as follows:

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

Response Format
***************

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
