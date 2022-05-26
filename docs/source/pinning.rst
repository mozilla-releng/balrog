===============
Release Pinning
===============

Firefox update supports a feature known as update pinning.
The purpose of this feature is to allow users (primarily enterprise users) to set a version beyond which installations should not update.
Two types of pins can be set: major version pins (ex: ``102.``) and minor version pins (ex: ``102.1.``).

This feature is a bit more complicated than simply not installing an update if it is beyond the specified version.
The problem with that approach is that, without the changes made to accommodate this feature, Balrog will always provide the newest version that the installation can be updated to.
Balrog needs to be aware of what version the installation is pinned to.
To understand why, consider an installation at version 102 that is pinned to version 103 when the newest version is 104.
If Balrog wasn't aware of the pinned version, the installation would ask for updates and would get the update to 104 in response.
Since that is newer than the pin, instead of updating to 103, it wouldn't update at all.
To accommodate update pinning, the application needs to send the pin as part of the update URL so that Balrog knows the correct version to return in cases like this.

-----------------
How Pinning Works
-----------------

~~~~~~~~~~~~~~~~~~
Release Automation
~~~~~~~~~~~~~~~~~~

The process starts when a new release is built.
When the build has completed, Release Automation automatically submits the release to Balrog.
The Balrog submission Taskcluster jobs specify one or more channels that the release should be pinned for (See `Bug 1762979 <https://bugzilla.mozilla.org/show_bug.cgi?id=1762979>`_ for details).

These channel names are passed, along with the rest of the release submission data to `balrogscript <https://github.com/mozilla-releng/scriptworker-scripts/tree/master/balrogscript>`_.
Balrogscript then makes 2 requests (one for the major pin and one for the minor pin) to the Balrog REST API to associate the release with its pin for the specified channel (See `Bug 1770827 <https://bugzilla.mozilla.org/show_bug.cgi?id=1770827>`_ for details).

Balrog handles each request by first ensuring that the release being pinned is not older than the release that currently has that pin (if any).
Then it associates the pin with the release name in its ``pinnable_releases`` table.

~~~~~~~~~~~~~~~~~~
Application Update
~~~~~~~~~~~~~~~~~~

When an installation of Firefox has an update pin set, it simply includes the pin as a query parameter in the update URL in order to communicate it to Balrog.

.. note::
  When Balrog responds, Firefox does not actually check that the update returned complies with the requested pin.
  It simply assumes that Balrog gave it the correct version.
  One important reason why it does this is that Firefox cannot always validate the pin 100% reliably.
  In order for a pin to be valid, it must specify an existing version of Firefox.
  Since Firefox does not know what versions exist and what do not, it cannot always reject invalid pins.
  And in the case that the pin is invalid, Firefox should continue updating to the newest possible version rather than obeying the invalid pin.

  At first glance, it may seem like it would be better to attempt to obey pins, even if no such version exists.
  This, however, would lead to subtle problems that are best avoided.
  Say, for example, that an installation is pinned to ``102.15.``, but no such version is ever released.
  When the newest version is less than the pin, everything works fine and the installation stays up-to-date.
  But when the newest version is greater than the pin (say, ``140.0.0``), Balrog is effectively faced with the choice of whether to return the newest available version, or whether to return nothing.
  Returning nothing does two things: it suggests that ``102.15.`` is a valid pin, because installations do not update beyond it, and it essentially prevents any installation with that pin from updating, potentially trapping it on a version much older than ``102``.

~~~~~~
Balrog
~~~~~~

When Firefox requests updates, Balrog first evaluates the :ref:`rules` normally.
If the resulting release is not newer than the pin, that is returned.
This is important for ensuring that the installation doesn't skip over a watershed.

If the release that the rules evaluate to is newer than the pin, the ``pinnable_releases`` table is consulted.
If there is a matching pin in the pinning table that wouldn't result in the installation downgrading, that is returned.
