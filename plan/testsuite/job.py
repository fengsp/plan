# -*- coding: utf-8 -*-
"""
    plan.testsuite.job
    ~~~~~~~~~~~~~~~~~~

    Tests the Job classes for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import unittest

from plan.testsuite import PlanTestCase
from plan.job import is_month, is_week, get_frequency
from plan.job import CommandJob, ScriptJob, ModuleJob
from plan.exceptions import ParseError, ValidationError


class BasicTestCase(PlanTestCase):
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
        self.assert_equal(3, get_frequency('3.years'))
        self.assert_equal(3, get_frequency('3.'))


class JobTestCase(PlanTestCase):

    def test_task(self):
        job = CommandJob('/bin/task', every='weekend')
        self.assert_equal(job.cron, '0 0 * * 6,0 /bin/task')
        job = CommandJob('ls  -l ', every='weekend')
        self.assert_equal(job.cron, '0 0 * * 6,0 ls -l')

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
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='0.minute')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='61.minute')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='0.hour')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='25.hour')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='0.day')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='32.day')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='0.month')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='13.month')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='0.year')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='2.year')
        self.assert_raises(ParseError, lambda : job.cron)

    def test_minute_at(self):
        pass

    def test_hour_at(self):
        pass

    def test_day_at(self):
        pass

    def test_month_at(self):
        pass

    def test_week_at(self):
        pass

    def test_at_parse_error(self):
        job = CommandJob('task', every='jan', at='minute.60')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='jan', at='hour.24')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='jan', at='day.0')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='jan', at='day.32')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='jan', at='month.12')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='jan', at='year.1')
        self.assert_raises(ParseError, lambda : job.cron)
        job = CommandJob('task', every='jan', at='whenever')
        self.assert_raises(ParseError, lambda : job.cron)

    def test_every_at_validation_error(self):
        pass

    def test_path(self):
        pass

    def test_environment(self):
        pass

    def test_output(self):
        pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BasicTestCase))
    suite.addTest(unittest.makeSuite(JobTestCase))
    return suite
