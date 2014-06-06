# -*- coding: utf-8 -*-
"""
    plan.core
    ~~~~~~~~~

    Core classes for Plan.

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

import re
import sys
import tempfile
import subprocess

from .commands import Echo, prompt_choices
from .job import CommandJob, ScriptJob, ModuleJob


class Plan(object):
    """The central object where you register jobs.  One Plan instance should 
    manage a group of jobs.

    :param name: the unique identity for this plan object, default to be main
    :param environment: the global crontab job bash environment.
    :param output: the global crontab job output logfile for this object.
    :param user: the user you want to run `crontab` command with.
    """
    
    def __init__(self, name="main", environment=None, output=None, user=None):
        self.name = name
        self.environment = environment
        self.output = output
        self.user = user

        # All jobs registered on this Plan object
        self.jobs = []

    def inject_kwargs(self, kwargs):
        if self.environment:
            kwargs.setdefault('environment', self.environment)
        if self.output:
            kwargs.setdefault('output', self.output)

    def command(self, *args, **kwargs):
        """Register one command."""
        self.inject_kwargs(kwargs)
        job = CommandJob(*args, **kwargs)
        self.job(job)

    def script(self, *args, **kwargs):
        """Register one script."""
        self.inject_kwargs(kwargs)
        job = ScriptJob(*args, **kwargs)
        self.job(job)

    def module(self, *args, **kwargs):
        """Register one module."""
        self.inject_kwargs(kwargs)
        job = ModuleJob(*args, **kwargs)
        self.job(job)

    def job(self, job):
        """Register one job.
        
        :param job: one :class:`Plan.Job` instance.
        """
        self.jobs.append(job)

    @property
    def comment_begin(self):
        """Comment begin content for this object, this will be added before
        the actual cron syntax jobs content.  Different name is used to
        distinguish different Plan object, so we can locate the cronfile
        content corresponding to this object.
        """
        return "# Begin Plan generated jobs for: %s" % self.name

    @property
    def crons(self):
        """Return a list of registered jobs's cron syntax content."""
        return [job.cron for job in self.jobs]

    @property
    def comment_end(self):
        return "# End Plan generated jobs for: %s" % self.name

    @property
    def cron_content(self):
        """Your schedule jobs converted to cron syntax."""
        return "\n".join([self.comment_begin] + self.crons +
                                                [self.comment_end]) + "\n"

    def _write_to_crontab(self, action, content):
        """The inside method used to modify the current crontab cronfile.
        This will write the content into current crontab cronfile.

        :param action: the action that is done, could be written, updated or
                       cleared.
        :param content: the content that is written to the crontab cronfile.
        """
        tmp_cronfile = tempfile.NamedTemporaryFile()
        tmp_cronfile.write(content)
        
        # command used to write crontab
        # $ crontab -u username cronfile
        command = ['crontab']
        if self.user:
            command.extend(["-u", str(self.user)])
        command.append(tmp_cronfile.name)
        
        try:
            subprocess.call(command)
        except:
            Echo.fail("couldn't write crontab; try running check to "
                      "ensure your cronfile is valid.")
            sys.exit(1)
        else:
            Echo.write("crontab file %s" % action)
            sys.exit(0)
        finally:
            tmp_cronfile.close()

    def write_crontab(self):
        """Write the crontab cronfile with this object's cron content, used
        by run_type `write`.  This will replace the whole cronfile.
        """
        self._write_to_crontab("written", self.cron_content)

    def read_crontab(self):
        """Get the current working crontab cronfile content."""
        command = ['crontab', '-l']
        if self.user:
            command.extend(["-u", str(self.user)])
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        return p.stdout.read()

    def update_crontab(self, update_type):
        """Update the current cronfile, used by run_type `update` or `clear`.
        This will find the block inside cronfile corresponding to this Plan
        object and replace it.
        
        :param update_type: update or clear, if you choose update, the block
                            corresponding to this plan object will be replaced
                            with the new cron job entries, otherwise, they
                            will be wiped.
        """
        current_crontab = self.read_crontab()
        
        if update_type == "update":
            action = "updated"
            crontab_content = self.cron_content
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
            Echo.fail("Your crontab file is not ended, it contains '%s', "
                      "but no '%s'" % (self.comment_begin, self.comment_end))
            sys.exit(1)
        elif not comment_begin_match and comment_end_match:
            Echo.fail("Your crontab file has no begining, it contains '%s', "
                      "but no '%s'" % (self.comment_end, self.comment_begin))
            sys.exit(1)

        # Found our existing block and replace it with the new one
        # Otherwise, append out new cron jobs after others
        if comment_begin_match and comment_end_match:
            updated_content = cron_block_re.sub(crontab_content, 
                                                        current_crontab)
        else:
            updated_content = "\n\n".join(current_crontab, crontab_content)

        # Write the updated cronfile back to crontab
        self._write_to_crontab(action, updated_content)

    def run(self):
        """Use this to do any action on this Plan object."""
        run_type = prompt_choices("Run", ["check", "write", "update", "clear"])
        if run_type == "update" or run_type == "clear":
            self.update_crontab(run_type)
        elif run_type == "write":
            self.write_crontab()
        else:
            Echo.echo(self.cron_content)
            Echo.message("Your crontab file was not updated.")

    def __call__(self):
        """Shortcut for :method:`run`."""
        self.run()
