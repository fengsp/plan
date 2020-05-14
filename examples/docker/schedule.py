# -*- coding: utf-8 -*-
from plan import Plan

cron = Plan()

output = dict(stdout='/var/log/stdout.log', stderr='/var/log/stderr.log')

cron.command('top', every='1.hour', output=output)
cron.command('echo ok', path='/home', every='1.minute', output=output)

if __name__ == '__main__':
    cron.run("write")