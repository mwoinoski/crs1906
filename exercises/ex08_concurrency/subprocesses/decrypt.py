"""
decrypt.py - uses Threads to decrypt multiple files concurrently.
"""

import subprocess
import getpass
import os
import sys

from threading import Thread
import re


def run_openssl(file, environ):
    """
    Use openssl to encrypt some data using AES (Advanced Encryption
    Standard), the replacement for DES (Data Encryption Standard).
    """
    out_file = re.sub(r'\.aes$', '', file)
    try:
        subprocess.check_call(
            ['openssl', 'enc', '-d', '-aes256', '-pass', 'env:password',
             '-in', file, '-out', out_file],
            env=environ, timeout=2)

        print('Decrypted {} to {}'.format(file, out_file), flush=True)
    except Exception as e:
        print('Problem decrypting', file)


def main():
    if len(sys.argv) == 1:
        print('Usage: {} file...'.format(sys.argv[0]))
        sys.exit(1)

    pw = getpass.getpass()  # prompts and reads without echoing input
    environ = os.environ.copy()
    environ['password'] = pw    # store password in environment variable

    for file in sys.argv[1:]:
        # TODO: note that we create and start Threads exactly as we did
        # in encrypt.py
        # (no code change required)
        child_thread = Thread(target=run_openssl,
                              args=(file, environ))
        child_thread.start()


if __name__ == '__main__':
    main()
