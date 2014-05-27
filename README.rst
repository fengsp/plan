Plan
====

Plan is a Python package for writing and deploying cron jobs with a clear
and beautiful syntax.  Plan will convert Python-style configuration to
cron syntax.

Installation
------------

::

    $ pip install plan

Quickstart
----------

::

    $ cd /web/my-app
    $ planize .

Now we have an `schedule.py` file like this:

.. code:: python

    # pass

Command
-------

::

    $ cd /web/my-app/schedule_file_location
    $ plan

Now you can get your `schedule.py` file in cron syntax.

Better
------

If you feel anything wrong, feedbacks or pull requests are welcomed.
