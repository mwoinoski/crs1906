"""
encrypt.py - uses Threads to encrypt multiple files concurrently.
"""

import getpass
import os
import sys

# TODO: import Thread from the threading module
from threading import Thread

# TODO: import the subprocess module
import subprocess


# TODO: note the definition of the run_openssl() function. This function will
# be the target of the Threads that you create.
# (no code change required)
def run_openssl(file, environ):
    out_file = file + '.aes'
    try:
        subprocess.check_call(
            ['openssl', 'enc', '-e', '-aes256', '-pass', 'env:password',
             '-in', file, '-out', out_file],
            env=environ, timeout=2)
        # To capture output, pass PIPE for the stdout and/or stderr arguments.

        print('Encrypted {} to {}'.format(file, out_file), flush=True)
    except subprocess.CalledProcessError as e:
        print('openssl process returned {} when encrypting {}'
              .format(file, e.returncode), flush=True)
    except Exception as e:
        print('Problem encrypting', file, flush=True)
        raise


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
        child_thread = Thread(target=run_openssl,
                              args=(file, environ))

        # TODO: start the Thread instance
        child_thread.start()


if __name__ == '__main__':
    main()
