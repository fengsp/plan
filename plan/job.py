# -*- coding: utf-8 -*-
"""
    plan.job
    ~~~~~~~~

    Job classes for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import re


class Job(object):
    """The plan job base class.

    reboot yearly monthly weekly daily hourly perminute midnight
    """
    
    cron_time_syntax_re = re.compile(r"^.+\s+.+\s+.+\s+.+\s+.+$")
    predefined_definitions = {"yearly", "annually", "monthly", "weekly",
                              "daily", "hourly", "reboot"}

    def __init__(self):
        self.every = every
        self.at = at
        self.path = path
        self.environment = environment
        self.task = task
        self.output = output

    @property
    def main_template(self):
        return "/bin/bash -l -c {job}"

    def job_template(self):
        raise NotImplementedError()

    @property
    def job_in_cron_syntax(self):
        return self.main_template.format(job=self.job_template())

    @property
    def time_in_cron_syntax(self):
        """Parse every into cron time syntax

        every can be any of following values
        
        """
        if self.cron_time_syntax_re.match(self.every):
            return self.every
        elif self.every in self.predefined_definitions:
            return "@%s" % self.every
        else:
            return self.parse_time()
    
    def validate_time(self):
        """Validate every and at.

        every: can be [0-59].minute [0-23].hour [1-31].day 
                      [0-6].week [1-12].month [1].year
        at: can be minute.[0-59] hour.[0-23] day.[1-31] week.[0-6] 
                   month.[1-12]
        """
        pass

    def produce_frequency_time(self, frequency, maximum, start=0):
        """Get frequency into comma separated times.
        """
        # if every is the same with maximum
        if frequency == 0:
            return start
        # else if every is one unit, we use '*'
        elif frequency == 1:
            return '*'
        # otherwise, we make steps comma separated
        else:
            times = range(maximum+1)[start:maximum:frequency]
            if (maximum + 1) % frequency:
                del times[0]
            return ','.join(times)

    def parse_time(self):
        """Parse time into cron time syntax::

            # * * * * *  command to execute
            # ┬ ┬ ┬ ┬ ┬
            # │ │ │ │ │
            # │ │ │ │ │
            # │ │ │ │ └─── day of week (0 - 7) (0 to 6 are Sunday to Saturday)
            # │ │ │ └───── month (1 - 12)
            # │ │ └─────── day of month (1 - 31)
            # │ └───────── hour (0 - 23)
            # └─────────── min (0 - 59)

        """
        # validation
        time = ['*'] * 5
        if self.every = "1.year":
            self.every = "12.months"
        every_num, every_unit = self.every.split('.')
        at_unit, at_num = self.at.split('.')

        if every_unit == "minute":
            pass
        elif every_unit == "hour":
            pass
        elif every_unit == "day":
            pass
        elif every_unit == "week":
            pass
        elif every_unit == "month":
            pass

        return ' '.join(time)

    @property
    def cron_entry_content(self):
        return ' '.join([self.time_in_cron_syntax, self.job_in_cron_syntax])


class CommandJob(Job):
    """The command job.
    """

    def job_template(self):
        return '{command} {output}'


class ScriptJob(Job):
    """The script job.
    """

    def job_template(self):
        return 'cd {path} && {environment_variable}={environment} {script}' 
