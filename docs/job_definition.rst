.. _job_definition:

Job Definition
==============

This part shows you how to define a cron job in Plan.  One job takes following
parameters ``task``, ``every``, ``at``, ``path``, ``environment`` and 
``output``, you can have a look at :class:`~plan.Job` for more details.
Here is one example::
    
    from plan import Job

    job = Job('ruby script.rb', every='1.month', at='day.5',
                            path='/web/scripts', output='null',
                            environment={'RAILS_ENV': 'production'})


Every
-----

Every is used to define how often does the job run.  It takes the following
values::
    
    [1-60].minute
    [1-24].hour
    [1-31].day
    [1-12].month
    jan feb mar apr may jun jul aug sep oct nov dec
    and all of those full month names(case insenstive)
    sunday, monday, tuesday, wednesday, thursday, friday, saturday
    weekday, weekend (case insensitive)
    [1].year

There might be some cron time that you can not get with Plan which comes with
limited supporting syntax.  No worries, every takes raw cron syntax time
definition, and in this case, your at value will be ignored. For example, I can
do something like this::
    
    job = Job('demo', every='1,2 5,6 * * 3,4')


At
--

At value is used to define when does the job run.  It takes the following
values::
    
    minute.[0-59]
    hour.[0-23]
    hour:minute
    day.[1-31]
    sunday, monday, tuesday, wednesday, thursday, friday, saturday
    weekday, weekend (case insensitive)

How about multiple at values, you can do that by using one space to seperate
multiple values, for example I want to run one job every day at 12:15 and
12:45, I can define it like this::
    
    job = Job('onejob', every='1.day', at='hour.12 minute.15 minute.45')
    # or even better
    job = Job('onejob', every='1.day', at='12:15 12:45')


Path
----

The path you want to change to before run the task, default to be current
working directory.  For these job types that does not need one path, this
will be ignored, for example, :class:`~plan.CommandJob`.


Environment
-----------

The bash environment you want to run the task on.  You should use one Python
dictionary to define your environment key values pairs.


Output
------

The output redirection for the task.  It takes following values::
    
    "null"
    any raw output string
    one dictionary to define your stdout and stderr

For example::
    
    job = Job('job', every='1.day', output='null')
    job = Job('job', every='1.day', output='> /tmp/stdout.log 2> /tmp/stderr.log')
    job = Job('job', every='1.day', output=
                dict(stdout='/tmp/stdout.log', stderr='/tmp/stderr.log'))
