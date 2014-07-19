# -*- coding: utf-8 -*-
"""
    plan.job
    ~~~~~~~~

    Job classes for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import sys
import re
import collections

from .output import Output
from .exceptions import ParseError, ValidationError
from ._compat import iteritems


# Time types
MINUTE = "minute"
HOUR = "hour"
DAY = "day of month"
MONTH = "month"
WEEK = "day of week"

MONTH_MAP = {
    "jan": "1",
    "feb": "2",
    "mar": "3",
    "apr": "4",
    "may": "5",
    "jun": "6",
    "jul": "7",
    "aug": "8",
    "sep": "9",
    "oct": "10",
    "nov": "11",
    "dec": "12"
}
WEEK_MAP = {
    "sun": "0",
    "mon": "1",
    "tue": "2",
    "wed": "3",
    "thu": "4",
    "fri": "5",
    "sat": "6"
}

CRON_TIME_SYNTAX_RE = re.compile(r"^.+\s+.+\s+.+\s+.+\s+.+$")
PREDEFINED_DEFINITIONS = set(["yearly", "annually", "monthly", "weekly",
                              "daily", "hourly", "reboot"])


def is_month(time):
    """Tell whether time is one of the month names.

    :param time: a string of time.
    """
    return time[:3].lower() in MONTH_MAP


def is_week(time):
    """Tell whether time is one of the days of week.

    :param time: a string of time.
    """
    return time[:3].lower() in WEEK_MAP or \
        time.lower() in ('weekday', 'weekend')


def get_frequency(every):
    """Get frequency value from one every type value:

    >>> get_frequency('3.day')
    3

    :param every: One every type value.
    """
    return int(every[:every.find('.')])


def get_moment(at):
    """Get moment value from one at type value:

    >>> get_moment('minute.1')
    1

    :param at: One at type value.
    """
    return int(at[at.find('.') + 1:])


class Job(object):
    """The plan job base class.

    :param task: this is what the job does.
    :param every: how often does the job run.
    :param at: when does the job run.
    :param path: the path you want to run the task on,
                 default to be current working directory.
    :param environment: the environment you want to run the task under.
    :param output: the output redirection for the task.
    """

    def __init__(self, task, every, at=None, path=None,
                 environment=None, output=None):
        self.task = task
        self.every = every
        self.at = at
        self.path = path
        self.environment = environment
        self.output = str(Output(output))

    @property
    def env(self):
        if not self.environment:
            return ''
        kv_pairs = []
        for k, v in iteritems(self.environment):
            kv_pairs.append('='.join((k, v)))
        return ' '.join(kv_pairs)

    @property
    def main_template(self):
        """The main job template.
        """
        return "{task}"

    def task_template(self):
        """The task template.  You should implement this in your own job type.
        The default template is::

            'cd {path} && {environment} {task} {output}'
        """
        return 'cd {path} && {environment} {task} {output}'

    def process_template(self, template):
        """Process template content.  Drop multiple spaces in a row and strip
        it.
        """
        template = re.sub(r'\s+', r' ', template)
        template = template.strip()
        return template

    def produce_frequency_time(self, frequency, maximum, start=0):
        """Translate frequency into comma separated times.
        """
        # how many units one time type have
        length = maximum - start + 1
        # if every is the same with unit length
        if frequency == length:
            return str(start)
        # else if every is one unit, we use '*'
        elif frequency == 1:
            return '*'
        # otherwise, we make steps comma separated
        else:
            times = list(range(start, maximum + 1, frequency))
            if length % frequency:
                del times[0]
            times = map(str, times)
            return ','.join(times)

    def parse_month(self, month):
        """Parses month into month numbers.  Month can only occur in
        every value.

        :param month: this parameter can be the following values:

                          jan feb mar apr may jun jul aug sep oct nov dec
                          and all of those full month names(case insenstive)
                          or <int:n>.month
        """
        if '.' in month:
            frequency = get_frequency(month)
            return self.produce_frequency_time(frequency, 12, 1)
        else:
            month = month[:3].lower()
            return MONTH_MAP[month]

    def parse_week(self, week):
        """Parses day of week name into week numbers.

        :param week: this parameter can be the following values:

                         sun mon tue wed thu fri sat
                         sunday monday tuesday wednesday thursday friday
                         saturday
                         weekday weedend(case insenstive)
        """
        if week.lower() == "weekday":
            return "1,2,3,4,5"
        elif week.lower() == "weekend":
            return "6,0"
        else:
            week = week[:3].lower()
            return WEEK_MAP[week]

    def parse_every(self):
        """Parse every value.

        :return: every_type.
        """
        every = self.every

        if '.minute' in every:
            every_type, frequency = MINUTE, get_frequency(every)
            if frequency not in range(1, 61):
                raise ParseError("Your every value %s is invalid, out of"
                                 " minute range[1-60]" % every)
        elif '.hour' in every:
            every_type, frequency = HOUR, get_frequency(every)
            if frequency not in range(1, 25):
                raise ParseError("Your every value %s is invalid, out of"
                                 " hour range[1-24]" % every)
        elif '.day' in every:
            every_type, frequency = DAY, get_frequency(every)
            if frequency not in range(1, 32):
                raise ParseError("Your every value %s is invalid, out of"
                                 " month day range[1-31]" % every)
        elif '.month' in every or is_month(every):
            every_type = MONTH
            if '.' in every:
                frequency = get_frequency(every)
                if frequency not in range(1, 13):
                    raise ParseError("Your every value %s is invalid, out of"
                                     " month range[1-12]" % every)
        elif '.year' in every:
            every_type, frequency = MONTH, get_frequency(every)
            if frequency not in range(1, 2):
                raise ParseError("Your every value %s is invalid, out of"
                                 " year range[1]" % every)
            # Just handle months internally
            self.every = "12.months"
        elif is_week(every):
            every_type = WEEK
        else:
            raise ParseError("Your every value %s is invalid" % every)

        return every_type

    def preprocess_at(self, at):
        """Do preprocess for at value, just modify "12:12" style moment into
        "hour.12 minute.12" style moment value.

        :param at: The at value you want to do preprocess.
        """
        ats = at.split(' ')
        processed_ats = []
        for at in ats:
            if ':' in at:
                hour, minute = at.split(':')[:2]
                if minute.startswith('0') and len(minute) >= 2:
                    minute = minute[1]
                hour = 'hour.' + hour
                minute = 'minute.' + minute
                processed_ats.append(hour)
                processed_ats.append(minute)
            else:
                processed_ats.append(at)
        return ' '.join(processed_ats)

    def parse_at(self):
        """Parse at value into (at_type, moment) pairs.
        """
        pairs = dict()
        if not self.at:
            return pairs

        processed_at = self.preprocess_at(self.at)
        ats = processed_at.split(' ')
        at_map = collections.defaultdict(list)

        # Parse at value into (at_type, moments_list) pairs.
        # One same at_type can have multiple moments like:
        # at = "minute.5 minute.10 hour.2"
        for at in ats:
            if 'minute.' in at:
                at_type, moment = MINUTE, get_moment(at)
                if moment not in range(60):
                    raise ParseError("Your at value %s is invalid"
                                     " out of minute range[0-59]" % self.at)
            elif 'hour.' in at:
                at_type, moment = HOUR, get_moment(at)
                if moment not in range(24):
                    raise ParseError("Your at value %s is invalid"
                                     " out of hour range[0-23]" % self.at)
            elif 'day.' in at:
                at_type, moment = DAY, get_moment(at)
                if moment not in range(1, 32):
                    raise ParseError("Your at value %s is invalid"
                                     " out of month day range[1-31]" % self.at)
            elif 'month.' in at or 'year.' in at:
                raise ParseError("Your at value %s is invalid"
                                 " can not set month or year" % self.at)
            elif is_week(at):
                at_type = WEEK
                moment = self.parse_week(at)
            else:
                raise ParseError("Your at value %s is invalid" % self.at)
            if moment not in at_map[at_type]:
                at_map[at_type].append(moment)

        # comma seperate same at_type moments
        for at_type, moments in iteritems(at_map):
            moments = map(str, moments)
            pairs[at_type] = ','.join(moments)

        return pairs

    def validate_time(self):
        """Validate every and at value.

        every can be::

            [1-60].minute [1-24].hour [1-31].day
            [1-12].month [1].year
            jan feb mar apr may jun jul aug sep oct nov dec
            sun mon tue wed thu fri sat weekday weekend
            or any fullname of month names and day of week names
            (case insensitive)

        at::

            when every is minute, can not be set
            when every is hour, can be minute.[0-59]
            when every is day of month, can be minute.[0-59], hour.[0-23]
            when every is month, can be day.[1-31], day of week,
                                 minute.[0-59], hour.[0-23]
            when every is day of week, can be minute.[0-59], hour.[0-23]

            at can also be multiple at values seperated by one space.
        """
        every_type, every = self.parse_every(), self.every
        ats = self.parse_at()
        if every_type == MINUTE:
            if ats:
                raise ValidationError("at can not be set when every is"
                                      " minute related")
        elif every_type == HOUR:
            for at_type in ats:
                if at_type not in (MINUTE):
                    raise ValidationError("%s can not be set when every is"
                                          " hour related" % at_type)
        elif every_type == DAY:
            for at_type in ats:
                if at_type not in (MINUTE, HOUR):
                    raise ValidationError("%s can not be set when every is"
                                          " month day related" % at_type)
        elif every_type == MONTH:
            for at_type in ats:
                if at_type not in (MINUTE, HOUR, DAY, WEEK):
                    raise ValidationError("%s can not be set when every is"
                                          " month related" % at_type)
        elif every_type == WEEK:
            for at_type in ats:
                if at_type not in (MINUTE, HOUR):
                    raise ValidationError("%s can not be set when every is"
                                          " week day related" % at_type)

        return every_type, every, ats

    def parse_time(self):
        """Parse every and at into cron time syntax::

            # * * * * *  command to execute
            # ┬ ┬ ┬ ┬ ┬
            # │ │ │ │ │
            # │ │ │ │ │
            # │ │ │ │ └─── day of week (0 - 7) (0 to 6 are Sunday to Saturday)
            # │ │ │ └───── month (1 - 12)
            # │ │ └─────── day of month (1 - 31)
            # │ └───────── hour (0 - 23)
            # └─────────── minute (0 - 59)

        """
        every_type, every, ats = self.validate_time()
        time = ['*'] * 5

        if every_type == MINUTE:
            frequency = get_frequency(every)
            time[0] = self.produce_frequency_time(frequency, 59)
        elif every_type == HOUR:
            frequency = get_frequency(every)
            time[0] = ats.get(MINUTE, '0')
            time[1] = self.produce_frequency_time(frequency, 23)
        elif every_type == DAY:
            frequency = get_frequency(every)
            time[0] = ats.get(MINUTE, '0')
            time[1] = ats.get(HOUR, '0')
            time[2] = self.produce_frequency_time(frequency, 31, 1)
        elif every_type == MONTH:
            time[0] = ats.get(MINUTE, '0')
            time[1] = ats.get(HOUR, '0')
            time[2] = ats.get(DAY, '1')
            time[3] = self.parse_month(every)
            time[4] = ats.get(WEEK, '*')
        else:
            time[0] = ats.get(MINUTE, '0')
            time[1] = ats.get(HOUR, '0')
            time[4] = self.parse_week(every)

        return ' '.join(time)

    @property
    def task_in_cron_syntax(self):
        """Cron content task part.
        """
        kwargs = {
            "path": self.path,
            "environment": self.env,
            "task": self.task,
            "output": self.output
        }
        task = self.task_template().format(**kwargs)
        task = self.process_template(task)
        main = self.main_template.format(task=task)
        return self.process_template(main)

    @property
    def time_in_cron_syntax(self):
        """Cron content time part.
        """
        if CRON_TIME_SYNTAX_RE.match(self.every):
            return self.every
        elif self.every in PREDEFINED_DEFINITIONS:
            return "@%s" % self.every
        else:
            return self.parse_time()

    @property
    def cron(self):
        """Job in cron syntax."""
        return ' '.join([self.time_in_cron_syntax, self.task_in_cron_syntax])


class CommandJob(Job):
    """The command job.
    """

    def task_template(self):
        """Template::

            '{task} {output}'
        """
        return '{task} {output}'


class ScriptJob(Job):
    """The script job.
    """

    def task_template(self):
        """Template::

            'cd {path} && {environment} %s {task} {output}' % sys.executable
        """
        return 'cd {path} && {environment} %s {task} {output}' % sys.executable


class ModuleJob(Job):
    """The module job.
    """

    def task_template(self):
        """Template::

            '{environment} %s -m {task} {output}' % sys.executable
        """
        return '{environment} %s -m {task} {output}' % sys.executable


class RawJob(Job):
    """The raw job.
    """

    def task_template(self):
        """Template::

            '{task}'
        """
        return '{task}'
