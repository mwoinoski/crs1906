"""
threading_demo1.py - threading demo from Chapter 9

Creates a Thread instance directly.
"""


from threading import Thread
import zipfile

def zip_it(infile, outfile):
    f = zipfile.ZipFile(outfile, 'w', zipfile.ZIP_DEFLATED)
    f.write(infile)
    f.close()
    print('Finished', infile)

# create a Thread instance that will call zip_it, passing args tuple
background = Thread(target=zip_it,
                    args=('inventory.csv', 'inventory.zip'))

background.start()  # start the Thread executing

print('Main thread continues to run in foreground')

background.join()  # Wait for the child_process task to finish
print('Main thread waited until child_process was done.')


