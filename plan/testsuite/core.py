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

    def test_inject_kwargs(self):
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


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PlanTestCase))
    return suite
