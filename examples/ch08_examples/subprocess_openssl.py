"""
subprocess_openssl.py - run multiple openssl processes.

You must run this script from the command line so it can read a password.
"""

import subprocess
import getpass
import os


def run_openssl(data, pw):
    """Use openssl to encrypt some data"""
    env = os.environ.copy()
    env['password'] = pw
    print("About to write", data)
    proc = subprocess.Popen(
        ['openssl', 'enc', '-aes', '-pass', 'env:password'],
        env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    print("Writing", data)
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc


def raw_data():
    """Generator function that yields one string each time it's called"""
    lines = [  # data to be encrypted
        'What a piece of work is a man!',
        'How noble in reason, how infinite in faculty!',
        'In form and moving how express and admirable!',
        'In action how like an Angel!',
        'In apprehension how like a god!',
        'The beauty of the world!',
        'The paragon of animals!',
    ]
    for next_line in lines:
        yield next_line.encode('utf-8')


pw = getpass.getpass()  # prompts and reads without echoing input
procs = []

print("About to start")
for data in raw_data():
    print("About to call run_openssl with", data)
    proc = run_openssl(data, pw)
    procs.append(proc)

for proc in procs:
    out, err = proc.communicate()
    print(out)


