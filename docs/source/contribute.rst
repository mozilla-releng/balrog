======================
Contributing to Balrog
======================


If you like to get involved in the development of Balrog, there're lots of areas where we could use some help.

------------
Requirements
------------

These instructions assume you have the following installed( if not, you can follow the link for installation instructions)

-   `Git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_
-   `Docker <https://docs.docker.com/v1.8/installation>`_
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

Once these prerequisites are installed, run the
following command to create and run the necessary images:

::

    $ docker-compose up

Once it completes, you should be able to access

-   The admin interface at http://127.0.0.1:8080
-   The public interface on port 9090, for example http://127.0.0.1:9090/update/3/Firefox/33.0/20141202185629/Darwin_x86_64-gcc3-u-i386-x86_64/en-US/release/default/default/default/update.xml?force=1


---------------------
Finding Bugs to Solve
---------------------

You can take look at the bugs filed at bugzilla for
`Balrog Backend <https://bugzilla.mozilla.org/buglist.cgi?product=Release%20Engineering&component=Balrog%3A%20Backend&resolution=---&list_id=13281625>`_
and
`Balrog Frontend <https://bugzilla.mozilla.org/buglist.cgi?product=Release%20Engineering&component=Balrog%3A%20Frontend&resolution=---&list_id=13281632>`_.

Once you have decided the work a bug you can comment on the Bug about any questions you have related to it.
You can also ask on #balrog for help.



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

-------------
Running Tests
-------------

It is a good idea to run all tests to see if Balrog is running properly.

To excute all tests, run
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

