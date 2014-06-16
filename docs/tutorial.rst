.. _tutorial:

Tutorial
========

You want to manage your cron jobs with Python and Plan?  Here you can learn
that by this tutorial.  In this tutorial I will show you how to use Plan
to do cron jobs in Python.  After this you should be easily creating your own
cron jobs and learn the common patterns of Plan.

If you want the full source code, check out `example source`_.

.. _example source: https://github.com/fengsp/plan/tree/master/examples


Introducing
-----------

We will explain our needs here, basically we want to do the following things:

1. We want to log our server running status every 4 hours.
2. We are running one Python web application and want to run a few scripts
   at different times.
3. As time goes on, I have a few more commands and scripts to run.


Basic
-----

Let's get our basic schedule file::
    
    $ mkdir schedule
    $ cd schedule
    $ plan-quickstart

Now you can see a `schedule.py` under your schedule directory,
``plan-quickstart`` is the command that comes with Plan for creating one
example file, you can run ``plan-quickstart --help`` for more details.  Then
you can modify this file for your own needs, the file looks like this::
    
    # -*- coding: utf-8 -*-

    # Use this file to easily define all of your cron jobs.
    #
    # It's helpful to understand cron before proceeding.
    # http://en.wikipedia.org/wiki/Cron
    #
    # Learn more: http://github.com/fengsp/plan

    from plan import Plan

    cron = Plan()

    # cron.command('top', every='4.hour', output=
            dict(stdout='/tmp/top_stdout.log', stderr='/tmp/top_stderr.log'))
    # cron.script('script.py', every='1.day', path='/web/yourproject/scripts',
                             environment={'YOURAPP_ENV': 'production'})

    if __name__ == "__main__":
        cron.run()


One Command
-----------

Let's begin with one little command, quite clear::

    cron.command('top', every='4.hour', output=
            dict(stdout='/tmp/top_stdout.log', stderr='/tmp/top_stderr.log'))

Run ``python schedule.py`` and run it with check mode, you will see the
following cron syntax content::
    
    # Begin Plan generated jobs for: main
    0 0,4,8,12,16,20 * * * top >> /tmp/top_stdout.log 2>> /tmp/top_stderr.log
    # End Plan generated jobs for: main

When you call :meth:`~plan.Plan.run`, you can choose which run-type(default 
to be check) you want to use, for more details on run types, check 
:ref:`run_types` out.


Scripts
-------

I have one script I want to run every day::
    
    cron.script('script.py', every='1.day', path='/web/yourproject/scripts',
                             environment={'YOURAPP_ENV': 'production'})

And now we have one more cron entry::
    
    0 0 * * * cd /web/yourproject/scripts && YOURAPP_ENV=production python script.py


More Jobs
---------

As time goes on, I have more cron jobs.  For example, I have 10 more
scripts under `/web/yourproject/scripts` and 10 more commands to run.  Now
we have to think about how to manage these tons of jobs, first we do not
want to put these jobs in one place, second we do not want to repeat the
same path and environment parameter on all script jobs.  Luckily, you can do
that easily with Plan, basically, every :class:`~plan.Plan` instance is a
group of cron jobs::
    
    $ cp schedule.py schedule_commands.py
    $ cp schedule.py schedule_scripts.py

Now we modify schedule_commands.py::
    
    from plan import Plan

    cron = Plan("commands")

    cron.command('top', every='4.hour', output=
              dict(stdout='/tmp/top_stdout.log', stderr='/tmp/top_stderr.log'))
    cron.command('yourcommand', every='sunday', at='hour.12 minute.0 minute.30')
    # more commands here

    if __name__ == "__main__":
        cron.run()

Then schedule_scripts.py::

    from plan import Plan

    cron = Plan("scripts", path='/web/yourproject/scripts',
                                 environment={'YOURAPP_ENV': 'production'})

    cron.script('script.py', every='1.day')
    cron.script('script_2.py', every='1.month', at='hour.12 minute.0')
    # more scripts here

    if __name__ == "__main__":
        cron.run()

A problem arises, how do you update your crontab content when you have two
schedule files, it is simple, do not use ``write`` run-type, instead use,
``update`` run-type here.  ``write`` run-type
will replace the whole crontab cronfile content with that Plan object's
cron content, ``update`` will just add or update the corresponding block
distinguished by your Plan object name(here is ``"commands"`` and
``"scripts"``).

If you are still interested, now is your time to move on to the next part.
