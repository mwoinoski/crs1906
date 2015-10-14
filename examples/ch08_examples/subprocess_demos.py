"""
subprocess_example.py - subprocess module examples from Chapter 8
"""

import subprocess
import platform
import time
import sys


def ex1():
    subprocess.call(['sort', 'inventory.csv'])


def ex2():
    subprocess.call('sort inventory.csv')


def ex3():
    for name in ['a', 'b', 'c']:
        open(name + '.bak', 'w')

    from glob import glob
    files = ' '.join(glob('*.bak'))
    subprocess.call('echo ' + files)

    # Some Windows commands
    subprocess.call('del *.bak', shell=True)


def ex4():
    host = 'google.com'
    option = '-n' if platform.system() == 'Windows' else '-c'
    status = 0

    try:
        output = subprocess.check_output(['ping', option, '1', host])
    except subprocess.CalledProcessError as exc:
        status = exc.returncode
        output = exc.output

    print('ping exit status = {}, output = {}'
          .format(status, output.decode('utf-8')))


def ex5():
    major, minor, *_ = sys.version_info
    if major > 3 or major == 3 and minor >= 5:
        host = 'google.com'
        option = '-n' if platform.system() == 'Windows' else '-c'
        status = 0
        try:
            result = subprocess.run(['ping', option, '1', host],
                                    check=True, stdout=subprocess.PIPE)
            output = result.stdout
        except subprocess.CalledProcessError as exc:
            status = exc.returncode
            output = exc.output

        print('ping exit status = {}, output = {}'
              .format(status, output.decode('utf-8')))


def ex6():
    proc = subprocess.Popen(['admin_script.bat'])
    while proc.poll() is None:
        print('Still working...')
        # do some time-consuming work here; we'll fake it with sleep
        time.sleep(1)

    print('admin_script exit status', proc.poll())


def ex7():
    grep = subprocess.Popen(['grep', 'Die-cast', 'inventory.csv'],
                            stdout=subprocess.PIPE)
    sort = subprocess.Popen(['sort'],
                            stdin=grep.stdout,
                            stdout=subprocess.PIPE)
    for line in sort.stdout:
        print('\t', line.decode('utf-8').strip())

if __name__ == '__main__':
    ex1()
    ex2()
    ex3()
    ex4()
    ex5()
    ex6()
    ex7()
