.. _installation:

Installation
============

You will need Python 2.6 or newer to get started, so firstly you should have
an up to date Python 2.x installation.  If you want to use Plan with Python 3
have a look at :ref:`python3-support`.

.. _virtualenv:


virtualenv
----------

Virtualenv is really great, maybe it is what you want to use during 
development.  Why virtualenv?  There are chances that you use Python for
other projects besides Plan-managed cron jobs.  It is likely that you will
be working with different versions of Python, or libraries.  And virtualenv
is the solution if two of your projects have conflicting dependencies.

You can install virtualenv by the following commands::

    $ sudo easy_install virtualenv
    
or better::

    $ sudo pip install virtualenv

Once you have virtualenv installed, it is easy to set up one working 
environment.  Let's create one project folder and one `venv` folder
for example::
    
    $ mkdir myproject
    $ cd myproject
    $ virtualenv venv
    New python executable in venv/bin/python
    Installing setuptools, pip...done.

Now if you want to activate the corresponding environment, just do::
    
    $ . venv/bin/activate


Install Plan
------------

You can just type the following command to get Plan::
    
    $ pip install plan

If you are not using :ref:`virtualenv`, you will have to do one system-wide
installation::
    
    $ sudo pip install plan


Development Version
-------------------

Get the source code from github and run it in development mode::
    
    $ git clone https://github.com/fengsp/plan.git
    $ cd plan
    $ virtualenv venv
    New python executable in venv/bin/python
    Installing setuptools, pip...done.
    $ . venv/bin/activate
    $ python setup.py develop
    ...
    Finished processing dependencies for Plan

Then you can use ``git pull origin`` to update to the latest version.
