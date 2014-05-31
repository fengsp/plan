# -*- coding: utf-8 -*-
"""
    plan.core
    ~~~~~~~~~

    Core classes for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import os
import re
import sys
import tempfile
import subprocess

import click

from .commands import prompt_choices


class Plan(object):
    """The central object where you register jobs.

    :param output: the crontab job output logfile.
    """
    
    def __init__(self, name="main", output=None, environment=None, user=None):
        self.name = name
        self.output = output
        self.environment = environment
        self.user = user

    def command(self):
        """Register one command."""
        pass

    def script(self):
        """Register one script."""
        pass

    def job(self):
        """Register one job."""
        pass

    @property
    def comment_begin(self):
        return "# Begin Plan generated jobs for: %s" % self.name

    def cron(self):
        """Return a list of cron syntax jobs."""
        return []

    @property
    def comment_end(self):
        return "# End Plan generated jobs for: %s" % self.name

    def get_cron_content(self):
        """Your schedule jobs converted to cron syntax"""
        return "\n".join([self.comment_begin] + self.cron() + 
                                                    [self.comment_end])

    def _write_to_crontab(self, action, content):
        """The inside method used to modify the current crontab cronfile.
        """
        tmp_cronfile = tempfile.NamedTemporaryFile()
        tmp_cronfile.write(content)
        
        command = ['crontab']
        if self.user:
            command.extend(["-u", str(self.user)])
        command.append(tmp_cronfile.name)
        
        try:
            subprocess.call(command)
        except:
            click.echo("[fail] Couldn't write crontab; try running without "
                       "options to ensure your cronfile is valid.")
            sys.exit(1)
        else:
            click.echo("[write] crontab file %s" % action)
            sys.exit(0)
        finally:
            tmp_cronfile.close()

    def write_crontab(self):
        """C."""
        self._write_to_crontab("written", self.get_cron_content())

    def read_crontab(self):
        """R."""
        command = ['crontab', '-l']
        if self.user:
            command.extend(["-u", str(self.user)])
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        return p.stdout.read()

    def update_crontab(self, update_type):
        """Update the current cronfile.
        
        :param update_type: update or clear, if you choose update, the block
                            corresponding to this plan object will be replaced
                            with the new cron job entries, otherwise, they
                            will be wiped.
        """
        #: Get current running crontab cronfile content
        current_crontab = self.read_crontab()
        # Get this plan object's cron syntax file content
        if update_type == "update":
            action = "updated"
            crontab_content = self.get_cron_content()
        elif update_type == "clear":
            action = "cleared"
            crontab_content = ''

        # Check for unbegined or unended block
        comment_begin_re = re.compile(r"^%s\s*$" % self.comment_begin)
        comment_end_re = re.compile(r"^%s\s*$" % self.comment_end)
        cron_block_re = re.compile(r"^%s\s*$.+^%s\s*$" % 
                       (self.comment_begin, self.comment_end), re.M|re.S)
                       
        comment_begin_match = comment_begin_re.search(current_crontab)
        comment_end_match = comment_end_re.search(current_crontab)

        if comment_begin_match and not comment_end_match:
            click.echo("[fail] Your crontab file is not ended, it contains "
                 "'%s', but no '%s'" % (self.comment_begin, self.comment_end))
            sys.exit(1)
        elif not comment_begin_match and comment_end_match:
            click.echo("[fail] Your crontab file has no begining, it contains "                 "'%s', but no '%s'" % (self.comment_end, self.comment_begin))
            sys.exit(1)

        # Found our existing block and replace with the new one
        # Otherwise, append out new cron jobs after others
        if comment_begin_match and comment_end_match:
            updated_content = cron_block_re.sub(crontab_content, 
                                                current_crontab)
        else:
            updated_content = "\n\n".join(current_crontab, crontab_content)

        # Write the updated cronfile back to crontab
        self._write_to_crontab(action, updated_content)

    def run(self):
        """Run."""
        run_type = prompt_choices("Run", ["check", "write", "update", "clear"])
        if run_type == "update" or run_type == "clear":
            self.update_crontab(run_type)
        elif run_type == "write":
            self.write_crontab()
        else:
            click.echo(self.get_cron_content())
            click.echo("[message] Your crontab file was not updated.")

    def __call__(self):
        self.run()
