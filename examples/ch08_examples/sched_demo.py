"""
sched_demo.py - demo of sched module from Chapter 8
"""

import sched, time

scheduler = sched.scheduler(time.time, time.sleep)

def do_task(name):
    print('Running {} at time {}'.format(name, time.strftime("%X %x")))

print('Starting at time ' + time.strftime("%X %x"))

priority = 1
scheduler.enter(2, priority, do_task, ('first',))
scheduler.enter(3, priority, do_task, ('second',))

start_str = '2015-07-02 23:00'
fmt = '%Y-%m-%d %H:%M'
start_time = time.mktime(time.strptime(start_str, fmt))

scheduler.enterabs(start_time, priority, do_task, ('abs time',))
# if start_time is in the past, do_task runs immediately

scheduler.run()
