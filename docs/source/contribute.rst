======================
Contributing to Balrog
======================


If you like to get involved in the development of Balrog there're lots of areas where we could use some help.

-----------------------
Cloning the  Repository
-----------------------

-   Fork the `Balrog Repository <https://github.com/mozilla/balrog>`_ on GitHub.
-   Clone the fork using 
    
    ::

        $   git clone git@github.com:<user-id>/balrog.git

By creating a fork, you are able to generate *pull request* so that the changes can be easily seen and reviewed by other community members. 


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
This allows you to work on different project at the same time.

::

    $   git checkout master
    $   git checkout -b topic-branch

Once you're done with your changes, you'll need to describe those changes in
the commit message.


--------------------
Submitting your work
--------------------

Once you have made the required changes make sure all the test still pass.
Then, you should submit your work with a pull request to master. 
Make sure you reference the Bug number on the Pull Request. 
Now, you have to wait for the review. 

Once your code has been positively reviewed, it will be deployed shortly after.
So if you want feedback on your code but it's not ready to be deployed, you
should note it in the pull request.

