"""
daemon_demo1.py - daemon thread demo from Chapter 9

Defines a Thread subclass
"""

from threading import Thread
import zipfile
import time
import sys


class AsyncZip(Thread):
    """Thread subclass that zips a file"""

    def __init__(self, infile, outfile):
        super().__init__()
        self.infile = infile
        self.outfile = outfile

    def run(self):
        for i in range(5):
            time.sleep(1)
            sys.stdout.write(".")
            sys.stdout.flush()
        sys.stdout.write('\n')
        f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
        print('Finished child_process zip of:', self.infile)


background = AsyncZip('inventory.csv', 'inventory.zip')

# if daemon is True, this thread won't prevent Python interpreter from exiting
background.daemon = True
background.start()

print('main thread exiting')
exit()
# if child_process is a daemon thread, Python interpreter exits.
# if child_process is not a daemon thread, Python interpreter waits until
# child_process terminates.
