"""
multiprocessing_demo1.py - multiprocessing demo from Chapter 9

Creates a Process instance directly.
"""


from multiprocessing import Process
from zipfile import ZipFile, ZIP_DEFLATED


def zip_it(infile, outfile):
    with ZipFile(outfile, 'w', ZIP_DEFLATED) as f:
        f.write(infile)
    print('Finished', infile)

# On Windows the subprocesses will import (i.e. execute) the main module
# when they start. You need to protect the main code to avoid creating
# subprocesses recursively.
if __name__ == "__main__":

    # create a Process instance that will call zip_it, passing args tuple
    child_process = Process(target=zip_it,
                            args=('inventory.csv', 'inventory.zip'))

    child_process.start()  # start the Process executing

    print('Main process continues to run in foreground')

    child_process.join()  # Wait for the child process to finish

    print('Main process waited until child_process was done.')


