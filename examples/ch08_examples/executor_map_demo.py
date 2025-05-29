"""
executor_map_demo.py - Demo of Executor.map() from Chapter 8
"""

from concurrent.futures import ThreadPoolExecutor
import wexpect  # wexpect lets us control a Windows console application


def ftp_get_file(args):
    """Connect to a ftp site and download files"""
    ftp_site, file_name, user, pw = args

    child = wexpect.spawn('ftp ' + ftp_site)
    child.expect('User .*: ')
    child.sendline(user)
    child.expect('Password:')
    child.sendline(pw)
    child.expect('ftp> ')
    child.sendline(f'get {file_name}')
    child.expect('ftp> ')
    child.sendline('bye')

    return ftp_site, file_name


if __name__ == '__main__':
    ftp_args = [
        ('cygwin.mirror.rafal.ca',
         '/pub/vim/doc/README',
         'ftp',
         'email@example.com'),
        ('cygwin.mirror.rafal.ca',
         '/pub/vim/doc/book/vimbook-OPL.pdf',
         'ftp',
         'email@example.com'),
    ]
    with ThreadPoolExecutor() as executor:
        results = executor.map(ftp_get_file, ftp_args, timeout=5)
        try:
            print('Launched all ftp processes')
            for site, file in results:
                print(f"Got {file} from {site}")
        except Exception as e:
            print("Got an exception: " + str(e))
