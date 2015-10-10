"""
executor_map_demo.py - Demo of Executor.map() from Chapter 9
"""

import os
from concurrent.futures import ThreadPoolExecutor


def ftp_get_file(args):
    """Connect to ftp site and download a file"""
    site, file, user, pw = args
    # import pexpect  # pexpect is available only on *ix platforms
    # child = pexpect.spawn('ftp ' + site)
    # child.expect('User .*: ')
    # child.sendline(user)
    # child.expect('Password:')
    # child.sendline(pw)
    # child.expect('ftp> ')
    # child.sendline('cd ' + os.path.dirname(file))
    # child.expect('ftp> ')
    # child.sendline('get ' + os.path.basename(file))
    # child.expect('ftp> ')
    # child.sendline('bye')
    return site, file


if __name__ == '__main__':
    ftp_args = [
        ('ftp.kernel.org',
         '/pub/software/utils/script/flock/flock-1.0.tar.gz',
         'anonymous',
         'anonymous@gmail.com'),
        ('ftp.kernel.org',
         '/pub/software/utils/script/flock/flock-2.0.tar.gz',
         'anonymous',
         'anonymous@gmail.com'),
    ]
    with ThreadPoolExecutor() as executor:
        results = executor.map(ftp_get_file, ftp_args, timeout=5)
        try:
            print('Launched all ftp processes')
            for site, file in results:
                print("Got {} from {}".format(file, site))
        except Exception as e:
            print("Got an exception: " + str(e))