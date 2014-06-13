# -*- coding: utf-8 -*-
"""
    plan.output
    ~~~~~~~~~~~

    Output for Plan.  This is used for cron job output redirection.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

from ._compat import string_types


class Output(object):
    """The plan output class used for command line output redirection.
    """

    def __init__(self, output=None):
        self.output = output

    def __str__(self):
        if not self.output:
            return ''
        if isinstance(self.output, string_types):
            return self.from_string()
        elif isinstance(self.output, dict):
            return self.from_dict()
        else:
            raise TypeError("Illegal output value %s" % self.output)

    def from_string(self):
        if self.output == "null":
            return "> /dev/null 2>&1"
        return self.output

    def from_dict(self):
        stdout = self.output.get('stdout', '/dev/null')
        stderr = self.output.get('stderr', '/dev/null')
        if stdout == '/dev/null' and stderr == '/dev/null':
            return "> /dev/null 2>&1"
        elif stdout and stderr:
            return ">> {stdout} 2>> {stderr}".format(stdout=stdout,
                                                     stderr=stderr)
        elif stdout:
            return ">> {stdout}".format(stdout=stdout)
        elif stderr:
            return "2>> {stderr}".format(stderr=stderr)
        else:
            return ''
