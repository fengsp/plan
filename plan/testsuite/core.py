# -*- coding: utf-8 -*-
"""
    plan.testsuite.core
    ~~~~~~~~~~~~~~~~~~~

    Tests the core classes for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import unittest

from plan.testsuite import PlanTestCase
from plan.core import Plan


class PlanTestCase(PlanTestCase):
    
    def test_test(self):
        self.assert_true(True)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PlanTestCase))
    return suite
