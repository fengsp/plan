# -*- coding: utf-8 -*-
"""
    demo
    ~~~~

    :copyright: (c) 2014 by Shipeng Feng.
    :license: BSD, see LICENSE for more details.
"""

from plan import Plan

cron = Plan()

cron.command('ls /tmp', every='1.day', at='12:00')
cron.command('pwd', every='2.month')
cron.command('date', every='weekend')

if __name__ == "__main__":
    cron.run()
