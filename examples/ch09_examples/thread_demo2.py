"""
threading_demo2.py - threading demo from Chapter 9

Defines a Thread subclass
"""

from threading import Thread
import zipfile


class AsyncZip(Thread):
    """Thread subclass that zips a file"""

    def __init__(self, infile, outfile):
        super().__init__()
        self.infile = infile
        self.outfile = outfile

    def run(self):
        f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
        print('Finished child_process zip of:', self.infile)


# Create an instance of the Thread subclass
background = AsyncZip('inventory.csv', 'inventory.zip')

background.start()  # start the Thread executing

print('Main thread continues to run in foreground')

background.join()  # Wait for the child_process task to finish
print('Main thread waited until child_process was done.')


