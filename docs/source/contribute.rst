======================
Contributing to Balrog
======================


If you like to get involved in the development of Balrog, there're lots of areas where we could use some help.

------------
Requirements
------------

These instructions assume you have the following installed (if not, you can follow the links for installation instructions).

-   `Git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_
-   `Docker <https://docs.docker.com/engine/getstarted/step_one/>`_
-   `Tox <http://tox.readthedocs.io/en/latest/install.html>`_ (Optional)

-----------------------
Cloning the  Repository
-----------------------

-   Fork the `Balrog Repository <https://github.com/mozilla/balrog>`_ on GitHub.
-   Clone the fork using

    ::

        $   git clone git@github.com:<user-id>/balrog.git

By creating a fork, you are able to generate a *pull request* so that the changes can be easily seen and reviewed by other community members.

-----
Usage
-----

Run the following command to create and run the necessary images:

::

    $ docker-compose up

After it completes, you should be able to access

-   The admin interface at https://localhost:8010
-   The public interface at http://localhost:9010, for example http://localhost:9010/update/3/Firefox/33.0/20141202185629/Darwin_x86_64-gcc3-u-i386-x86_64/en-US/release/default/default/default/update.xml?force=1

You'll need to use the "Sign in..." button to do anything useful with the admin interface, which will ask you to sign in with a third party provider (eg: gmail, github). Once you've done that, run the following to create a local admin user to gain write access:

::

    $ export LOCAL_ADMIN=<email address you signed in with>
    $ docker-compose run balrogadmin create-local-admin


-------------
Running Tests
-------------

It is a good idea to run all tests to see if Balrog is running properly.

To execute all tests, run
::

    $ ./run-tests.sh

For executing test only for backend, run

::

    $ ./run-tests.sh backend

For executing test only for frontend, run

::

    $ ./run-tests.sh frontend


In case  you can't or don't want to run tests within Docker for some reason,
tests can also run by using `tox <http://tox.readthedocs.io/en/latest/install.html>`_

::

    $ tox

Tests run fine on any posix-like environment, but are only run regularly within the Docker image,
so it's possible to have failures that aren't related to Balrog code or your changes when running directly with tox.

---------------------
Finding Bugs to Solve
---------------------

To start with, it's recommended that you look at a `Good First Bug <https://bugzilla.mozilla.org/buglist.cgi?list_id=13406850&emailtype1=exact&status_whiteboard_type=allwordssubstr&emailassigned_to1=1&status_whiteboard=%5Bgood%20first%20bug%5D&email1=nobody%40mozilla.org&resolution=---&query_format=advanced&component=Balrog%3A%20Backend&component=Balrog%3A%20Frontend>`_. Once you're more comfortable with Balrog, we've got a long list of `other bugs ready to be worked on <https://bugzilla.mozilla.org/buglist.cgi?list_id=13406852&emailtype1=exact&status_whiteboard_type=allwordssubstr&emailassigned_to1=1&status_whiteboard=%5Bready%5D&email1=nobody%40mozilla.org&resolution=---&query_format=advanced&component=Balrog%3A%20Backend&component=Balrog%3A%20Frontend>`_.

Once you have decided the work a bug you can comment on the Bug about any questions you have related to it.
You can also ask in irc://irc.mozilla.org/#balrog for help.


------------------
IRC best practices
------------------

If you want to message someone directly within the channel, precede your message
with their nick:. This will alert the person that they have a message especially
for them, and makes it easier for the person receiving the message to read it
in a busy channel. For example:

::

    johnsmith_: your message/query


------------
Git workflow
------------

When you want to start contributing, you should create a branch from master.
This allows you to work on different projects at the same time.

::

    $   git checkout master
    $   git checkout -b topic-branch

Once you're done with your changes, you'll need to describe those changes in
the commit message.

--------------------
Submitting your work
--------------------

Once you have made the required changes, make sure all the tests still pass.
Then, you should submit your work with a pull request to master.
Make sure you reference the Bug number on the Pull Request.
Now, you have to wait for the review.

Once your code has been positively reviewed, it will be deployed shortly after.
So if you want feedback on your code, but it's not ready to be deployed, you
should note it in the pull request.

