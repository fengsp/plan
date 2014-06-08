.. _quickstart:

Quickstart
==========

This page gives a good introduction to Plan.  If you do not have Plan
installed, check out :ref:`installation` section.


A Minimal Example
-----------------

A simple usage looks like this::
    
    from plan import Plan

    cron = Plan()

    pass

    if __name__ == "__main__":
        cron.run()

Just save it as `schedule.py` (or whatever you want) and run it with your
Python interpreter.  Make sure to not name it `plan.py` becaure it would
conflict with Plan itself.

Now If you just select the default run_type check, you should see your
cron syntax jobs in the output of terminal.


Explanation
-----------

So what did the above code do?

1. First we imported the :class:`~plan.Plan` class.  An instance of this
   class will be one group of cron jobs.
2. Next we create an instance of this class.  We are not passing any argument
   here, though, the first argument is the name of this group of cron jobs.
   In our case, we have the default name 'main' here.  For more information
   have a look at the :class:`~plan.Plan` documentation.
3. We then use the :meth:`~plan.Plan.command` to register one command job on
   this Plan object.
4. Finally we run this Plan object and check your cron syntax jobs or write
   it to your crontab.
