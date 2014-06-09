# -*- coding: utf-8 -*-

# Use this file to easily define all of your cron jobs.
#
# It's helpful to understand cron before proceeding.
# http://en.wikipedia.org/wiki/Cron
#
# Learn more: http://github.com/fengsp/plan

from plan import Plan

cron = Plan("scripts", path='/web/yourproject/scripts',
                             environment={'YOURAPP_ENV': 'production'})

cron.script('script.py', every='1.day')
cron.script('script_2.py', every='1.month', at='hour.12 minute.0')
# more scripts here

if __name__ == "__main__":
    cron.run()
