# -*- coding: utf-8 -*-
"""
    plan.testsuite.output
    ~~~~~~~~~~~~~~~~~~~~~

    Tests the output for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import unittest

from plan.testsuite import PlanTestCase


class OutputTestCase(PlanTestCase):
    
    def test_testcase(self):
        self.assert_equal(1, 1)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(OutputTestCase))
    return suite
