# -*- coding: utf-8 -*-
"""
    plan.testsuite.core
    ~~~~~~~~~~~~~~~~~~~

    Tests the core classes for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import sys
import unittest

from plan.testsuite import BaseTestCase
from plan.core import Plan
from plan.exceptions import PlanError


class PlanTestCase(BaseTestCase):

    def test_empty_cron_content(self):
        plan = Plan()
        desired_cron_content = """\
# Begin Plan generated jobs for: main
# End Plan generated jobs for: main
"""
        self.assert_equal(plan.cron_content, desired_cron_content)

    def test_cron_content(self):
        plan = Plan()
        plan.command('command', every='1.day')
        plan.script('script.py', every='1.day', path='/web/scripts',
                    environment={'key': 'value'}, output='null')
        plan.module('calendar', every='1.day')
        desired_cron_content = """\
# Begin Plan generated jobs for: main
0 0 * * * command
0 0 * * * cd /web/scripts && key=value %s script.py > /dev/null 2>&1
0 0 * * * %s -m calendar
# End Plan generated jobs for: main
""" % (sys.executable, sys.executable)
        self.assert_equal(plan.cron_content, desired_cron_content)

    def test_environment_variables(self):
        plan = Plan()
        plan.env('MAILTO', 'user@example.com')
        plan.command('command', every='1.day')
        desired_cron_content = """\
# Begin Plan generated jobs for: main
MAILTO="user@example.com"
0 0 * * * command
# End Plan generated jobs for: main
"""
        self.assert_equal(plan.cron_content, desired_cron_content)

    def test_global_parameters(self):
        plan = Plan('test', path='/web/scripts',
                    environment={'testkey': 'testvalue'},
                    output=dict(stdout='/tmp/out.log'))
        plan.script('script.py', every='1.day')
        desired_cron_content = """\
# Begin Plan generated jobs for: test
0 0 * * * cd /web/scripts && testkey=testvalue %s script.py >> /tmp/out.log 2>> /dev/null
# End Plan generated jobs for: test
""" % sys.executable
        self.assert_equal(plan.cron_content, desired_cron_content)

        plan = Plan('test', path='/web/global/scripts',
                    environment={'globalkey': 'globalvalue'},
                    output=dict(stdout='/tmp/global.log'))
        plan.script('script.py', every='1.day', path='/web/scripts',
                    environment={'testkey': 'testvalue'},
                    output=dict(stdout='/tmp/out.log'))
        desired_cron_content = """\
# Begin Plan generated jobs for: test
0 0 * * * cd /web/scripts && testkey=testvalue %s script.py >> /tmp/out.log 2>> /dev/null
# End Plan generated jobs for: test
""" % sys.executable
        self.assert_equal(plan.cron_content, desired_cron_content)


class CrontabTestCase(BaseTestCase):
    """TestCase for communicating with crontab process."""

    def setup(self):
        self.plan = Plan()
        self.original_crontab_content = self.plan.read_crontab()
        self.write_crontab('', '')

    def write_crontab(self, action, content):
        self.plan._write_to_crontab(action, content)

    def test_read_and_write_crontab(self):
        test_crontab_content = """\
# TEST BEGIN
* * * * * test
# TEST END
"""

        self.assert_equal(self.plan.read_crontab(), '')
        self.write_crontab('', test_crontab_content)
        self.assert_equal(self.plan.read_crontab(), test_crontab_content)

    def test_update_crontab_error(self):
        test_crontab_content = """\
# Begin Plan generated jobs for: main
0 12 * * * ls /tmp
# End Plan generated jobs for:
"""
        self.write_crontab('', test_crontab_content)
        self.assert_raises(PlanError, self.plan.update_crontab, 'update')
        test_crontab_content = """\
# Begin Plan generated jobs for:
0 12 * * * ls /tmp
# End Plan generated jobs for: main
"""
        self.write_crontab('', test_crontab_content)
        self.assert_raises(PlanError, self.plan.update_crontab, 'update')

    def test_write_crontab_error(self):
        test_crontab_content = """\
test
"""
        self.assert_raises(PlanError, self.write_crontab, '',
                           test_crontab_content)

    def teardown(self):
        self.write_crontab('', self.original_crontab_content)
        self.plan = None


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PlanTestCase))
    suite.addTest(unittest.makeSuite(CrontabTestCase))
    return suite
