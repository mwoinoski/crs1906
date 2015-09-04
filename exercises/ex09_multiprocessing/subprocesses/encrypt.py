"""
encrypt.py - run multiple openssl processes
"""

import subprocess
import getpass
import os
import sys
from time import sleep

# TODO: import Process from the multiprocessing module
...


# TODO: note the run_openssl() function. This function will be the target
# of the Processes that you create.
# (no code change required)
def run_openssl(file, env):
    """Use openssl to encrypt some data using AES"""
    out_file = file + '.des3'
    try:
        subprocess.check_call(
            ['openssl', 'enc', '-e', '-aes256', '-pass', 'env:password',
             '-in', file, '-out', out_file], env=env, timeout=2)
        sleep(1)  # pause for dramatic effect
        print('Encrypted {} to {}'.format(file, out_file), flush=True)
    except Exception as e:
        print('Problem encrypting', file)


def main():
    if len(sys.argv) == 1:
        print('Usage: {} file...'.format(sys.argv[0]))
        sys.exit(1)

    pw = getpass.getpass()  # prompts and reads without echoing input
    env = os.environ.copy()
    env['password'] = pw    # store password in environment variable

    for file in sys.argv[1:]:
        # TODO: create a Process instance to execute the run_openssl() function
        # HINT: remember to pass file and env to the Process
        # HINT: see slide 9-38
        # run_openssl(file, env)
        ...

        # TODO: start the Process instance
        ...


if __name__ == '__main__':
    main()
