# -*- coding: utf-8 -*-
"""
    plan.commands
    ~~~~~~~~~~~~~

    Command line tools for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""
import os

import click

from ._compat import get_binary_content


class Echo(object):
    """Echo class for Plan.  This is used to echo some common used content
    type in the command line.
    """

    @classmethod
    def echo(cls, message):
        click.echo(message)

    @classmethod
    def secho(cls, *args, **kwargs):
        click.secho(*args, **kwargs)

    @classmethod
    def message(cls, message):
        cls.secho("[message] %s" % message, fg="green")

    @classmethod
    def write(cls, message):
        cls.secho("[write] %s" % message, fg="green")

    @classmethod
    def fail(cls, message):
        cls.secho("[fail] %s" % message, fg="red")

    @classmethod
    def add(cls, message):
        cls.secho("[add] %s" % message, fg="green")

    @classmethod
    def done(cls, message=None):
        if message:
            cls.secho("[done] %s" % message, fg="green")
        else:
            cls.secho("[done]!", fg="green")


SCHEDULE_TEMPLATE = """\
# -*- coding: utf-8 -*-

# Use this file to easily define all of your cron jobs.
#
# It's helpful to understand cron before proceeding.
# http://en.wikipedia.org/wiki/Cron
#
# Learn more: http://github.com/fengsp/plan

from plan import Plan

cron = Plan()

# register one command, script or module
# cron.command('command', every='1.day')
# cron.script('script.py', path='/web/yourproject/scripts', every='1.month')
# cron.module('calendar', every='feburary', at='day.3')

if __name__ == "__main__":
    cron.run()
"""


@click.command()
@click.option('--path', default='./schedule.py',
              help='The filepath for your schedule file.')
def quickstart(path):
    """plan-quickstart"""
    write = True
    if os.path.isfile(path):
        write = click.confirm("'%s' already exists, override?" % path)
    if write:
        Echo.add("writing '%s'" % path)
        with open(path, 'wb') as f:
            f.write(get_binary_content(SCHEDULE_TEMPLATE))
        Echo.done()


def prompt_choices(name, choices):
    """One wrapper function for click.prompt to show choices to the user.
    """
    return click.prompt(name + ' - (%s)' % ', '.join(choices),
                        type=click.Choice(choices), default=choices[0])


if __name__ == "__main__":
    quickstart()
