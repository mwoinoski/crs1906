"""
subprocess_openssl.py - run multiple openssl processes
"""

import subprocess
import getpass
import os
import sys


def run_openssl(file, pw):
    """Use openssl to encrypt some data"""
    env = os.environ.copy()
    env['password'] = pw
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    with open(file, 'rb') as f:
        proc.stdin.write(f.read())
    proc.stdin.flush()
    return proc


def main():
    if len(sys.argv) == 1:
        print('Usage: {} file...'.format(sys.argv[0]))
        sys.exit(1)

    pw = getpass.getpass()  # prompts and reads without echoing input
    procs = []

    for file in sys.argv[1:]:
        proc = run_openssl(file, pw)
        procs.append((file, proc))

    for file, proc in procs:
        out, err = proc.communicate()
        with open(file + '.des3', 'wb') as f:
            f.write(out)

if __name__ == '__main__':
    main()
