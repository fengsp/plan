.. _job_types:

Job Types
=========

There are several Plan built-in cron job types.


Command Job
-----------

One command is a common executable program, check out :class:`~plan.CommandJob`.
Plan comes with one shortcut for register CommandJob :meth:`~plan.Plan.command`.


Script Job
----------

One script should be one Python pyfile, check out :class:`~plan.ScriptJob`.
Plan comes with one shortcut for register ScriptJob :meth:`~plan.Plan.script`.


Module Job
----------

One module should be one Python module, check out :class:`~plan.ModuleJob`.
Plan comes with one shortcut for register ModuleJob :meth:`~plan.Plan.module`.


Raw Job
-------

Maybe these job types are not what you want, you can define your job with
raw cron syntax::
    
    cron = Plan()
    cron.raw('cd /tmp && ruby script.rb > /dev/null 2>&1', every='1.day')

    # In this particular case, you should try Job
    job = Job('ruby script.rb', every='1.day', path='/tmp', output='null')
    cron.job(job)


Define Your Own Job Types
-------------------------

You can define your own job types if you want.  Before we talk about how to
do that, let's have a look on what a shortcut like :meth:`~plan.Plan.command`
do::
    
    plan = Plan()
    job = CommandJob(*args, **kwargs)
    plan.job(job)

What :meth:`~plan.Plan.job` does is registering one job on this plan object.
If you want to write one own job type, just define one subclass of
:class:`~plan.Job` and override :meth:`~plan.Job.task_template`, let's see
what *CommandJob* looks like inside Plan::
    
    class CommandJob(Job):

        def task_template(self):
            return '{task} {output}'
    
The *ScriptJob* and *ModuleJob* are almost the same, with different
template::
    
    # ScriptJob
    return 'cd {path} && {environment} %s {task} {output}' % sys.executable
    # ModuleJob
    return '{environment} %s -m {task} {output}' % sys.executable

Now I want to have one job type to run ruby script, I can define it like this::
    
    class RubyJob(Job):

        def task_template(self):
            return 'cd {path} && {environment} /usr/bin/ruby {task} {output}'

And use it like this::
    
    plan = Plan()
    job = RubyJob(*args, **kwargs)
    plan.job(job)

Mostly If *CommandJob*, *ScriptJob* and *ModuleJob* are not what you
need, you can just use :class:`~plan.Job` or even :class:`~plan.RawJob`.
