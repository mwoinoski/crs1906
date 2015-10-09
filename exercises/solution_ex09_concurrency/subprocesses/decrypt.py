"""
decrypt.py - run multiple openssl processes
"""

import subprocess
import getpass
import os
import sys

from multiprocessing import Process
import re


def run_openssl(file, env):
    """Use openssl to decrypt some data using AES"""
    out_file = re.sub(r'\.des3$', '', file)
    try:
        subprocess.check_call(
            ['openssl', 'enc', '-d', '-aes256', '-pass', 'env:password',
             '-in', file, '-out', out_file], env=env, timeout=2)
        print('Decrypted {} to {}'.format(file, out_file), flush=True)
    except Exception as e:
        print('Problem decrypting', file)


def main():
    if len(sys.argv) == 1:
        print('Usage: {} file...'.format(sys.argv[0]))
        sys.exit(1)

    pw = getpass.getpass()  # prompts and reads without echoing input
    env = os.environ.copy()
    env['password'] = pw    # store password in environment variable

    for file in sys.argv[1:]:
        # TODO: note that we create and start Processes exactly as we did
        # in encrypt.py
        # (no code change required)
        child_process = Process(target=run_openssl,
                                args=(file, env))
        child_process.start()


if __name__ == '__main__':
    main()
