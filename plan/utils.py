# -*- coding: utf-8 -*-
"""
    plan.utils
    ~~~~~~~~~~

    Various utilities for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

from subprocess import Popen, PIPE


def communicate_process(command, stdin=None, *args, **kwargs):
    """Run the command described by command, then interact with process.

    :param stdin: the data you want to send to stdin.
    :return: a tuple of stdout, stderr and returncode
    """
    p = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, *args, **kwargs)
    output, error = p.communicate(stdin)
    returncode = p.returncode
    return output, error, returncode
