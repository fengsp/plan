# -*- coding: utf-8 -*-
"""
    plan.job
    ~~~~~~~~

    Job classes for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import os


class Job(object):
    """The plan job base class.
    """

    def __init__(self):
        self.at = at
        self.template = self.get_template()
        self.output = output
        self.environment = environment
        self.path = path

    def get_template(self):
        raise NotImplementedError()


class CommandJob(Job):
    """The command job.
    """

    def get_template(self):
        return '{command} {output}'


class ScriptJob(Job):
    """The script job.
    """

    def get_template(self):
        return 'cd {path} && {environment_variable}={environment} {script}' 
