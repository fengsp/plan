# -*- coding: utf-8 -*-
"""
    plan.testsuite.commands
    ~~~~~~~~~~~~~~~~~~~~~~~

    Tests the command line tools for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import unittest

import click
from click.testing import CliRunner

from plan.commands import Echo
from plan.testsuite import BaseTestCase


class EchoTestRunner(object):

    def __init__(self):
        self.runner = CliRunner()

    def invoke(self, echo_method, message):
        @click.command()
        @click.argument('message')
        def command(message):
            echo_method(message)
        return self.runner.invoke(command, [message])


class EchoTestCase(BaseTestCase):

    def setup(self):
        self.runner = EchoTestRunner()

    def teardown(self):
        self.runner = None

    def test_echo(self):
        result = self.runner.invoke(Echo.echo, 'echo')
        self.assert_true(result.exit_code == 0)
        self.assert_equal(result.output, 'echo\n')

    def test_secho(self):
        result = self.runner.invoke(Echo.secho, 'secho')
        self.assert_true(result.exit_code == 0)
        self.assert_equal(result.output, 'secho\n')

    def test_message(self):
        result = self.runner.invoke(Echo.message, 'message')
        self.assert_true(result.exit_code == 0)
        self.assert_equal(result.output, '[message] message\n')

    def test_write(self):
        result = self.runner.invoke(Echo.write, 'write')
        self.assert_true(result.exit_code == 0)
        self.assert_equal(result.output, '[write] write\n')

    def test_fail(self):
        result = self.runner.invoke(Echo.fail, 'fail')
        self.assert_true(result.exit_code == 0)
        self.assert_equal(result.output, '[fail] fail\n')

    def test_add(self):
        result = self.runner.invoke(Echo.add, 'add')
        self.assert_true(result.exit_code == 0)
        self.assert_equal(result.output, '[add] add\n')

    def test_done_with_message(self):
        result = self.runner.invoke(Echo.done, 'done')
        self.assert_true(result.exit_code == 0)
        self.assert_equal(result.output, '[done] done\n')

    def test_done_without_message(self):
        result = self.runner.invoke(Echo.done, '')
        self.assert_true(result.exit_code == 0)
        self.assert_equal(result.output, '[done]!\n')


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EchoTestCase))
    return suite
