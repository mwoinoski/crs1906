"""
encrypt.py - uses Threads to encrypt multiple files concurrently.
"""

import subprocess
import getpass
import os
import sys
from time import sleep

# TODO: import Thread from the threading module
from threading import Thread


# TODO: note the definition of the run_openssl() function. This function will
# be the target of the Threads that you create.
# (no code change required)
def run_openssl(file, environ):
    """
    Use openssl to encrypt some data using AES (Advanced Encryption
    Standard), the replacement for DES (Data Encryption Standard).
    """
    out_file = file + '.aes'
    try:
        subprocess.check_call(
            ['openssl', 'enc', '-e', '-aes256', '-pass', 'env:password',
             '-in', file, '-out', out_file],
            env=environ, timeout=2)

        sleep(1)  # pause for dramatic effect
        print('Encrypted {} to {}'.format(file, out_file), flush=True)
    except Exception as e:
        print('Problem encrypting', file)


def main():
    if len(sys.argv) == 1:
        print('Usage: {} file...'.format(sys.argv[0]))
        sys.exit(1)

    pw = getpass.getpass()  # prompts and reads without echoing input
    environ = os.environ.copy()
    environ['password'] = pw    # store password in environment variable

    for file in sys.argv[1:]:
        # TODO: create a Thread instance to execute the run_openssl() function
        # HINT: remember to pass file and env to the Thread
        # HINT: see slide 9-38
        child_thread = Thread(target=run_openssl,
                              args=(file, environ))

        # TODO: start the Thread instance
        child_thread.start()


if __name__ == '__main__':
    main()
