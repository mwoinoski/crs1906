"""
encrypt.py - uses the subprocess module to encrypt multiple files in parallel.
"""

import getpass
import os
import sys
# TODO: import the subprocess module
import subprocess


# TODO: note the definition of the run_openssl() function. This function will
# be the target of the processes that you create.
# (no code change required)
def run_openssl(file, environ):
    try:
        # TODO: note how the input and output files are opened as
        # `in_file` and `out_file`
        # (no code change required)
        with open(file, 'r') as in_file:
            with open(file + '.aes', 'w') as out_file:

                # TODO: call subprocess.Popen() to launch a process running
                # openssl to encrypt the input file.
                # For the `stdin` argument, pass in_file
                # For the `stdout` argument, pass out_file
                # Assign the returned Popen instance to a local variable.
                # HINT: see slide 8-10
                proc = subprocess.Popen(
                    ['openssl', 'enc', '-e', '-aes256', '-pass', 'env:password'],
                    env=environ, stdin=in_file, stdout=out_file)

                # TODO: note that you don't need to write to or flush the
                # Popen instance's standard input because openssl is reading
                # from a file instead of a pipe.
                # (no code change required)

                # TODO: return the Popen instance
                return proc

    except Exception as e:
        print('Problem encrypting', file, e)
        raise


def main():
    if len(sys.argv) == 1:
        print('Usage: {} file...'.format(sys.argv[0]))
        sys.exit(1)

    pw = getpass.getpass()  # prompts and reads without echoing input
    environ = os.environ.copy()
    environ['password'] = pw    # store password in environment variable

    # TODO: initialize a local variable named `procs` with an empty list
    procs = []

    # TODO: note the following loop over the command line arguments
    # (no code changes required)
    for file in sys.argv[1:]:
        # TODO: Call run_openssl(), passing arguments file and environ
        # Save the returned Popen instance in a local variable.
        # HINT: see slide 8-11
        proc = run_openssl(file, environ)

        # TODO: append the Popen instance to the `procs` list
        procs.append(proc)

    # TODO: loop over all the Popen instances in the `procs` list
    for proc in procs:
        # TODO: for each Popen instance, call the communicate() method to wait
        # for the process to complete.
        # HINT: you don't need to save the return values of communicate()
        # because the processes are reading and writing directly to files.
        proc.communicate()

    print('Done encrypting', ' '.join(sys.argv[1:]))


if __name__ == '__main__':
    main()
