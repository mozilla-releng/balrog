=========
Admin App
=========

-------------
**Admin API**
-------------

Balrog's Admin app provides an API that allows for retrieval and modification of Rules, Releases, and Permissions. 
This page documents all of the available endpoints, their parameters, and responses.
POST and PUT requests may submit parameters as multipart form data or json.

For detailed information look at :ref:`adminapi`

----------------
**UI Use Cases**
----------------

Locking/Unlocking Nightlies
***************************

One of the most common uses for the Balrog UI is to lock a nightly update channel to a specific release for a period of time, and then unlock it later (so that users on that channel start receiving the latest available build again). 
This is often done if a serious bug is introduced to minimize the number of users affected by it.

Taking the B2G nightly channel as an example, let's see how we would lock it to the nightlies from 20150505160203:

1.	Log in to https://aus4-admin.mozilla.org
2.	Click on the "Rules" link at the top of the page
3.	Use the filter in the top right to narrow down the rules to "product:B2G channel:nightly"
4.	Locate the rule (or rules) on the "nightly" channel
	-	Changing the sort to "Product, Channel" will group things together better.
5.	For each rule on the channel:
	-	Click the "Update" button to enter edit mode
	-	Find the mapping field and replace the "-latest" part with "-20150505160203" (the UI will autocomplete this for you if you start typing).
	-	Scroll down and click "Save Changes"

When you're ready to unlock the updates, follow the same steps as above but replace the "-20150505160203" part of the mapping with "-latest" again.

Adding a rule for a new update channel
**************************************

When nightly builds are set up on a new branch, rules need to be added to Balrog for updates to be served. 
Note that the nightly build automation is responsible for providing metadata about each new set of builds to Balrog.
As an example, here is how B2G updates could be set up on a hypothetical "mozilla-b2g40" branch:

1.	Log in to https://aus4-admin.mozilla.org
2.	Click on the "Rules" link at the top of the page
3.	Click on "Add a new Rule" near the top left of the page
4.	Fill out the form as follows:
	-	Product: B2G
	-	Channel: nightly-b2g40
	-	Mapping: B2G-mozilla-b2g40-nightly-latest
	-	Rate: 100
	-	Priority: 90
5.	Click "Save Changes"

Modify an existing release
**************************

Most modifications to releases are done by automation, but sometimes we need to tweak them by hand. 
For example, if you wanted to modify the "Firefox-38.0-build3" release, follow these steps:

1.	Log in to https://aus4-admin.mozilla.org/
2.	Click the "Releases" link at the top of the page
3.	Find the "Firefox-38.0-build3" release and click the "Download" link
4.	Save the file locally and modify it to your liking
5.	Click the "Update" link for "Firefox-38.0-build3"
6.	Click "Browse" and choose your new local version
7.	Click "Save Changes"

