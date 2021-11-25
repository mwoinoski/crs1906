"""
executor_map_demo.py - Demo of Executor.map() from Chapter 8
"""

import os
from concurrent.futures import ThreadPoolExecutor


def ftp_get_file(args):
    """Connect to ftp site and download a file"""
    site, file, user, pw = args
    if site == 'bad':
        raise ValueError('bad site')
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
        ('bad',
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
        print('Launched all ftp processes')
        while True:
            try:
                result = next(results, None)
                if result is None:
                    break
                site, file = result
                print(f"Got {file} from {site}")
            except Exception as e:
                print("exception: " + str(e))
