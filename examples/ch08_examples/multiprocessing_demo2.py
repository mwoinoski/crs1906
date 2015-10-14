"""
multiprocessing_demo2.py - multiprocessing demo from Chapter 8

Defines a Process subclass
"""

from multiprocessing import Process
from zipfile import ZipFile, ZIP_DEFLATED


class AsyncZip(Process):
    """Process subclass that zips a file"""

    def __init__(self, infile, outfile):
        super().__init__()
        self.infile = infile
        self.outfile = outfile

    def run(self):
        with ZipFile(self.outfile, 'w', ZIP_DEFLATED) as f:
            f.write(self.infile)
        print('Finished child_process zip of:', self.infile)


if __name__ == '__main__':
    # Create an instance of the Process subclass
    child_process = AsyncZip('inventory.csv', 'inventory.zip')

    child_process.start()  # start the Process executing

    print('Main process continues to run in foreground')

    child_process.join()  # Wait for the child_process task to finish
    print('Main process waited until child_process was done.')
