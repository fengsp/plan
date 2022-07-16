.. _run_types:

Run Types
=========

There are several mode Plan can run on, you should pass the run_type parameter
when you run your plan object, check out :meth:`~plan.Plan.run`, for example::
    
    cron = Plan()
    cron.run('check') # could be 'check', 'write', 'update', 'clear'


Check
-----

Check mode will just echo your cron syntax jobs out in the terminal and your
crontab file will not be updated.  This is used to check whether everything
goes fine as you expected.


Write
-----

Write mode will erase everything from your crontab cronfile and write this
plan object's cron content to the cronfile, your crontab file will be fresh.


Update
------

Update mode will find the corresponding block of this plan object in the
crontab cronfile and replace it with the latest content.  The other content
will be keeped as they were, this is distinguished by your plan object name,
so make sure it's unique if you have more than one plan object.


Clear
-----

Clear mode will find the corresponding block of this plan object in the 
crontab cronfile and erase it.  The other content will not be affected.
