"""
threading_demo2.py - threading demo from Chapter 8

Creates a Thread instance directly, calls a method.
"""

from threading import Thread
from zipfile import ZipFile, ZIP_DEFLATED


class Zipper:
    def __init__(self, name):
        self.name = name

    def zip_it(self, infile, outfile):
        print(f'Zipper {self.name} is zipping {infile} to {outfile}...')
        f = ZipFile(outfile, 'w', ZIP_DEFLATED)
        f.write(infile)
        f.close()
        print('Finished', infile)

zip_instance = Zipper('my_zip')
# create a Thread instance that will call the zip_it method, passing args tuple
background = Thread(target=Zipper.zip_it,
                    args=(zip_instance, 'inventory.csv', 'inventory.zip'))

background.start()  # start the Thread executing

print('Main thread continues to run in foreground')

background.join()  # Wait for the child_process task to finish
print('Main thread waited until child_process was done.')


