"""
encrypt.py - uses the subprocess module to encrypt multiple files in parallel.
"""

import getpass
import os
import sys
import subprocess


# The run_openssl function will be the target of the processes that we create
def run_openssl(file, pw):
    """
    Use openssl to encrypt some data using AES (Advanced Encryption Standard),
    the replacement for DES (Data Encryption Standard).
    """
    try:
        # Note how the input and output files are opened as
        # `in_file` and `out_file`
        with open(file, 'r') as in_file:
            with open(file + '.aes', 'w') as out_file:
                environ = os.environ.copy()
                environ['secret'] = pw    # store password in env variable
                
                # Call subprocess.Popen() to launch a process running
                # openssl to encrypt the input file.
                cmd = ['openssl', 'enc', '-e', '-aes256', '-pass', 'env:secret']
                proc = subprocess.Popen(cmd, env=environ, 
                                        stdin=in_file, stdout=out_file)

                # We don't need to write to or flush the
                # Popen instance's standard input because openssl is reading
                # from a file instead of a pipe.

                return proc

    except Exception as e:
        print('Problem encrypting', file, e)
        raise


def main():
    if len(sys.argv) == 1:
        print(f'Usage: {sys.argv[0]} file...')
        sys.exit(1)

    pw = getpass.getpass()  # prompts and reads without echoing input

    procs = []

    # loop over the command line arguments
    for file in sys.argv[1:]:
        proc = run_openssl(file, pw)
        procs.append(proc)

    # loop over all the Popen instances in the `procs` list
    for proc in procs:
        # For each Popen instance, call the communicate() method to wait
        # for the process to complete.
        # We don't need to save the return values of communicate()
        # because the processes are reading and writing directly to files.
        proc.communicate()

    print('Done encrypting', ' '.join(sys.argv[1:]))


if __name__ == '__main__':
    main()
