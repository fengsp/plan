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


content = """\
# Use this file to easily define all of your cron jobs.
#
# It's helpful to understand cron before proceeding.
# http://en.wikipedia.org/wiki/Cron

# Example:
#
# set :output, "/path/to/my/cron_log.log"
#
# every 2.hours do
#   command "/usr/bin/some_great_command"
#   runner "MyModel.some_method"
#   rake "some:great:rake:task"
# end
#
# every 4.days do
#   runner "AnotherModel.prune_old_records"
# end

# Learn more: http://github.com/fengsp/plan
"""


@click.command()
@click.option('--path', default='./schedule.py', type=click.File('wb'), help='The filepath for your schedule file.')
def quickstart(path):
    """plan-quickstart"""
    write = True
    if os.path.isfile(path.name):
        write = click.confirm("'%s' already exists, override?" %s path.name)
    if write:
        click.echo("[add] writing '%s'" %s path.name)
        path.write(content)
        click.echo("[done]!")


def prompt_choices(name, choices):
    return click.prompt(name + ' - (%s)' % ', '.join(choices), 
                      type=click.Choice(choices), default=choices[0])


if __name__ == "__main__":
    quickstart()
