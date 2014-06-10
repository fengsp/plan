.. _plan_definition:

Plan Definition
===============

This part shows how to initialize one plan object.  One plan object takes
parameters ``name``, ``path``, ``environment``, ``output`` and ``user``,
for more details check out :class:`~plan.Plan`.  Path, environment and output
are the same with :ref:`job_definition`, they are used to set global
parameters for all jobs registered on this plan object.  If a job does not
set one parameter, and a global parameter is set, the global one will be
used.


Name
----

The name of one plan object.  Should be passed as the first parameter.


User
----

If you want to run `crontab` command with a certain user, remember to set
this parameter.


Patterns
--------

One Plan object should be a group of cron jobs.  The name of the plan object
should be unique so that this object can be distinguished from another object.
Now you can have multiple plan object around and run it with update run_type,
only the corresponding content block will be renewed in the cronfile, for more
details go to :ref:`run_types` part.
