# -*- coding: utf-8 -*-
"""
    plan.testsuite.output
    ~~~~~~~~~~~~~~~~~~~~~

    Tests the output for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import unittest

from plan.output import Output
from plan.testsuite import BaseTestCase


class OutputTestCase(BaseTestCase):

    def test_from_none(self):
        output = str(Output())
        self.assert_equal(output, '')

    def test_from_string(self):
        output = str(Output('null'))
        self.assert_equal(output, '> /dev/null 2>&1')
        output = str(Output('> /tmp/out.log 2> /tmp/error.log'))
        self.assert_equal(output, '> /tmp/out.log 2> /tmp/error.log')

    def test_from_dict(self):
        output = str(Output(dict()))
        self.assert_equal(output, '')
        output = str(Output(dict(key='value')))
        self.assert_equal(output, '> /dev/null 2>&1')
        output = str(Output(dict(stdout='/dev/null', stderr='/dev/null')))
        self.assert_equal(output, '> /dev/null 2>&1')
        output = str(Output(dict(stdout=None, stderr=None)))
        self.assert_equal(output, '')
        output = str(Output(dict(stdout='/tmp/test_out.log', stderr=None)))
        self.assert_equal(output, '>> /tmp/test_out.log')
        output = str(Output(dict(stdout='', stderr='/tmp/test_error.log')))
        self.assert_equal(output, '2>> /tmp/test_error.log')
        output = str(Output(dict(stdout='/t/out.log', stderr='/t/err.log')))
        self.assert_equal(output, '>> /t/out.log 2>> /t/err.log')

    def test_from_illegal(self):
        output = Output(1)
        self.assert_raises(TypeError, output.__str__)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(OutputTestCase))
    return suite
