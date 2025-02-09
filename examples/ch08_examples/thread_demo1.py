"""
threading_demo1.py - threading demo from Chapter 8

Creates a Thread instance directly.
"""


from threading import Thread
from zipfile import ZipFile, ZIP_DEFLATED


def zip_it(infile, outfile):
    with ZipFile(outfile, 'w', ZIP_DEFLATED) as f:
        f.write(infile)
    print('Finished', infile)


# create a Thread instance that will call zip_it, passing args tuple
background = Thread(target=zip_it,
                    args=('inventory.csv', 'inventory.zip'))

background.start()  # start the Thread executing

print('Main thread continues to run in foreground')

background.join()  # Wait for the child_process task to finish
print('Main thread waited until child_process was done.')


