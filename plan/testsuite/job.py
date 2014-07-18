# -*- coding: utf-8 -*-
"""
    plan.testsuite.job
    ~~~~~~~~~~~~~~~~~~

    Tests the Job classes for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import sys
import unittest

from plan.testsuite import BaseTestCase
from plan.job import is_month, is_week, get_frequency, get_moment
from plan.job import Job, CommandJob, ScriptJob, ModuleJob, RawJob
from plan.exceptions import ParseError, ValidationError


class BasicTestCase(BaseTestCase):
    """Tests basic functions used by Job class."""

    def test_is_month(self):
        self.assert_true(is_month('jan'))
        self.assert_true(is_month('JAN'))
        self.assert_true(is_month('JANUARY'))
        self.assert_true(is_month('january'))
        self.assert_false(is_month('sunday'))

    def test_is_week(self):
        self.assert_true(is_week('mon'))
        self.assert_true(is_week('MON'))
        self.assert_true(is_week('monday'))
        self.assert_true(is_week('MONDAY'))
        self.assert_true(is_week('weekend'))
        self.assert_false(is_week('feburary'))

    def test_get_frequency(self):
        self.assert_equal(3, get_frequency('3.month'))
        self.assert_equal(3, get_frequency('3.'))

    def test_get_moment(self):
        self.assert_equal(3, get_moment('day.3'))
        self.assert_equal(3, get_moment('.3'))


class JobTestCase(BaseTestCase):

    def test_task(self):
        job = CommandJob('/bin/task', every='weekend')
        self.assert_equal(job.cron, '0 0 * * 6,0 /bin/task')
        job = CommandJob('ls  -l ', every='weekend')
        self.assert_equal(job.cron, '0 0 * * 6,0 ls -l')

    def test_raw_every(self):
        job = Job('task', every='0 1 2 3 *', at='minute.2', path='/path')
        self.assert_equal(job.cron, '0 1 2 3 * cd /path && task')

    def test_predefined_every(self):
        job = Job('task', every='yearly', at='minute.2', path='/path')
        self.assert_equal(job.cron, '@yearly cd /path && task')
        job = Job('task', every='monthly', at='minute.2', path='/path')
        self.assert_equal(job.cron, '@monthly cd /path && task')
        job = Job('task', every='weekly', at='minute.2', path='/path')
        self.assert_equal(job.cron, '@weekly cd /path && task')
        job = Job('task', every='daily', at='minute.2', path='/path')
        self.assert_equal(job.cron, '@daily cd /path && task')
        job = Job('task', every='hourly', at='minute.2', path='/path')
        self.assert_equal(job.cron, '@hourly cd /path && task')
        job = Job('task', every='reboot', at='minute.2', path='/path')
        self.assert_equal(job.cron, '@reboot cd /path && task')

    def test_minute_every(self):
        job = CommandJob('task', every='1.minute')
        self.assert_equal(job.cron, '* * * * * task')
        job = CommandJob('task', every='2.minute')
        self.assert_equal(job.cron, '0,2,4,6,8,10,12,14,16,18,20,22,24,26,'
                                    '28,30,32,34,36,38,40,42,44,46,48,50,52,'
                                    '54,56,58 * * * * task')
        job = CommandJob('task', every='10.minute')
        self.assert_equal(job.cron, '0,10,20,30,40,50 * * * * task')
        job = CommandJob('task', every='30.minute')
        self.assert_equal(job.cron, '0,30 * * * * task')
        job = CommandJob('task', every='60.minute')
        self.assert_equal(job.cron, '0 * * * * task')
        job = CommandJob('task', every='11.minute')
        self.assert_equal(job.cron, '11,22,33,44,55 * * * * task')

    def test_hour_every(self):
        job = CommandJob('task', every='1.hour')
        self.assert_equal(job.cron, '0 * * * * task')
        job = CommandJob('task', every='24.hour')
        self.assert_equal(job.cron, '0 0 * * * task')
        job = CommandJob('task', every='3.hour')
        self.assert_equal(job.cron, '0 0,3,6,9,12,15,18,21 * * * task')
        job = CommandJob('task', every='5.hour')
        self.assert_equal(job.cron, '0 5,10,15,20 * * * task')

    def test_day_every(self):
        job = CommandJob('task', every='1.day')
        self.assert_equal(job.cron, '0 0 * * * task')
        job = CommandJob('task', every='3.day')
        self.assert_equal(job.cron, '0 0 4,7,10,13,16,19,22,25,28,31 * * task')
        job = CommandJob('task', every='31.day')
        self.assert_equal(job.cron, '0 0 1 * * task')

    def test_month_every(self):
        job = CommandJob('task', every='1.month')
        self.assert_equal(job.cron, '0 0 1 * * task')
        job = CommandJob('task', every='2.month')
        self.assert_equal(job.cron, '0 0 1 1,3,5,7,9,11 * task')
        job = CommandJob('task', every='5.month')
        self.assert_equal(job.cron, '0 0 1 6,11 * task')
        job = CommandJob('task', every='january')
        self.assert_equal(job.cron, '0 0 1 1 * task')

    def test_week_every(self):
        job = CommandJob('task', every='monday')
        self.assert_equal(job.cron, '0 0 * * 1 task')
        job = CommandJob('task', every='sunday')
        self.assert_equal(job.cron, '0 0 * * 0 task')
        job = CommandJob('task', every='saturday')
        self.assert_equal(job.cron, '0 0 * * 6 task')
        job = CommandJob('task', every='weekday')
        self.assert_equal(job.cron, '0 0 * * 1,2,3,4,5 task')
        job = CommandJob('task', every='weekend')
        self.assert_equal(job.cron, '0 0 * * 6,0 task')

    def test_every_parse_error(self):
        job = CommandJob('task', every='1.century')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='0.minute')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='61.minute')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='0.hour')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='25.hour')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='0.day')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='32.day')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='0.month')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='13.month')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='0.year')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='2.year')
        self.assert_raises(ParseError, lambda: job.cron)

    def test_preprocess_at(self):
        job = Job('job', every='1.hour')
        at = job.preprocess_at('0:0')
        self.assert_equal(at, 'hour.0 minute.0')
        at = job.preprocess_at('1:00')
        self.assert_equal(at, 'hour.1 minute.0')
        at = job.preprocess_at('23:01')
        self.assert_equal(at, 'hour.23 minute.1')
        at = job.preprocess_at('23:10')
        self.assert_equal(at, 'hour.23 minute.10')
        at = job.preprocess_at('12:59')
        self.assert_equal(at, 'hour.12 minute.59')
        at = job.preprocess_at('14:09:0')
        self.assert_equal(at, 'hour.14 minute.9')

    def test_minute_at(self):
        job = CommandJob('task', every='1.hour', at='minute.5')
        self.assert_equal(job.cron, '5 * * * * task')
        job = CommandJob('task', every='1.day', at='minute.1')
        self.assert_equal(job.cron, '1 0 * * * task')
        job = CommandJob('task', every='1.month', at='minute.59')
        self.assert_equal(job.cron, '59 0 1 * * task')
        job = CommandJob('task', every='monday', at='minute.30')
        self.assert_equal(job.cron, '30 0 * * 1 task')

    def test_hour_at(self):
        job = CommandJob('task', every='1.day', at='hour.1')
        self.assert_equal(job.cron, '0 1 * * * task')
        job = CommandJob('task', every='1.month', at='hour.0')
        self.assert_equal(job.cron, '0 0 1 * * task')
        job = CommandJob('task', every='monday', at='hour.23')
        self.assert_equal(job.cron, '0 23 * * 1 task')

    def test_day_at(self):
        job = CommandJob('task', every='1.month', at='day.5')
        self.assert_equal(job.cron, '0 0 5 * * task')

    def test_week_at(self):
        job = CommandJob('task', every='1.month', at='sunday')
        self.assert_equal(job.cron, '0 0 1 * 0 task')

    def test_at(self):
        job = CommandJob('task', every='1.month', at='day.1 hour.1 minute.0')
        self.assert_equal(job.cron, '0 1 1 * * task')
        job = CommandJob('task', every='1.month', at='day.1 12:00')
        self.assert_equal(job.cron, '0 12 1 * * task')
        job = CommandJob('task', every='1.month',
                         at='day.1 hour.1 minute.5 minute.10')
        self.assert_equal(job.cron, '5,10 1 1 * * task')
        job = CommandJob('task', every='1.month',
                         at='day.15 10:55 10:56')
        self.assert_equal(job.cron, '55,56 10 15 * * task')

    def test_at_parse_error(self):
        job = CommandJob('task', every='jan', at='minute.60')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='jan', at='hour.24')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='jan', at='day.0')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='jan', at='day.32')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='jan', at='month.12')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='jan', at='year.1')
        self.assert_raises(ParseError, lambda: job.cron)
        job = CommandJob('task', every='jan', at='whenever')
        self.assert_raises(ParseError, lambda: job.cron)

    def test_every_at_validation_error(self):
        job = CommandJob('task', every='1.minute', at='minute.1')
        self.assert_raises(ValidationError, lambda: job.cron)
        job = CommandJob('task', every='1.minute', at='hour.23')
        self.assert_raises(ValidationError, lambda: job.cron)
        job = CommandJob('task', every='1.minute', at='day.1')
        self.assert_raises(ValidationError, lambda: job.cron)
        job = CommandJob('task', every='1.minute', at='sunday')
        self.assert_raises(ValidationError, lambda: job.cron)
        job = CommandJob('task', every='1.hour', at='hour.23')
        self.assert_raises(ValidationError, lambda: job.cron)
        job = CommandJob('task', every='1.hour', at='day.1')
        self.assert_raises(ValidationError, lambda: job.cron)
        job = CommandJob('task', every='1.hour', at='sunday')
        self.assert_raises(ValidationError, lambda: job.cron)
        job = CommandJob('task', every='1.day', at='day.1')
        self.assert_raises(ValidationError, lambda: job.cron)
        job = CommandJob('task', every='1.day', at='sunday')
        self.assert_raises(ValidationError, lambda: job.cron)
        job = CommandJob('task', every='sunday', at='day.1')
        self.assert_raises(ValidationError, lambda: job.cron)
        job = CommandJob('task', every='sunday', at='sunday')
        self.assert_raises(ValidationError, lambda: job.cron)

    def test_path(self):
        job = ScriptJob('script.py', every='1.day', path='/web/scripts')
        self.assert_equal(job.cron, '0 0 * * * cd /web/scripts && %s script.py'
                                    % sys.executable)

    def test_environment(self):
        job = ScriptJob('script.py', every='1.day', path='/web/scripts',
                        environment={'k': 'v'})
        self.assert_equal(job.cron, '0 0 * * * cd /web/scripts && k=v %s'
                          ' script.py' % sys.executable)

    def test_output(self):
        job = ScriptJob('script.py', every='1.day', path='/web/scripts',
                        output=dict(stdout='/log/out.log',
                                    stderr='/log/err.log'))
        self.assert_equal(job.cron, '0 0 * * * cd /web/scripts && %s script.py'
                          ' >> /log/out.log 2>> /log/err.log' % sys.executable)

    def test_job(self):
        job = Job('job', every='1.day', path='/tmp',
                  environment={'key': 'value'}, output='null')
        self.assert_equal(job.cron, '0 0 * * * cd /tmp && key=value job '
                          '> /dev/null 2>&1')

    def test_command_job(self):
        job = CommandJob('command', every='1.day', output='null')
        self.assert_equal(job.cron, '0 0 * * * command > /dev/null 2>&1')

    def test_script_job(self):
        job = ScriptJob('script.py', every='1.day', path='/tmp',
                        environment={'key': 'value'}, output='null')
        self.assert_equal(job.cron, '0 0 * * * cd /tmp && key=value %s'
                          ' script.py > /dev/null 2>&1' % sys.executable)

    def test_module_job(self):
        job = ModuleJob('calendar', every='1.day',
                        environment={'key': 'value'}, output='null')
        self.assert_equal(job.cron, '0 0 * * * key=value %s -m calendar'
                                    ' > /dev/null 2>&1' % sys.executable)

    def test_raw_job(self):
        job = RawJob('raw ????  my job', every='1.day')
        self.assert_equal(job.cron, '0 0 * * * raw ???? my job')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicTestCase))
    suite.addTest(unittest.makeSuite(JobTestCase))
    return suite
