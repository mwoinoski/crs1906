"""
decrypt.py - uses the subprocess module to decrypt multiple files in parallel.
"""

import getpass
import os
import sys
import re
import subprocess


def run_openssl(file, environ):
    try:
        with open(file, 'r') as in_file:
            with open(re.sub(r'\.aes$', '', file), 'w') as out_file:
                # TODO: note that we call subprocess.Popen() exactly as we did
                # in encrypt.py
                # (no code change required)
                proc = subprocess.Popen(
                    ['openssl', 'enc', '-d', '-aes256', '-pass', 'env:password'],
                    env=environ, stdin=in_file, stdout=out_file)
                return proc
    except Exception as e:
        print('Problem decrypting', file, e)
        raise


def main():
    if len(sys.argv) == 1:
        print('Usage: {} file...'.format(sys.argv[0]))
        sys.exit(1)

    pw = getpass.getpass()  # prompts and reads without echoing input
    environ = os.environ.copy()
    environ['password'] = pw    # store password in environment variable

    procs = []
    for file in sys.argv[1:]:
        # TODO: note that we call run_openssl() exactly as we did in encrypt.py
        # (no code change required)
        proc = run_openssl(file, environ)
        procs.append(proc)

    for proc in procs:
        proc.communicate()

    print('Done decrypting', ' '.join(sys.argv[1:]))


if __name__ == '__main__':
    main()
