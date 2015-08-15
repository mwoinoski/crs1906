"""
Pushes changes from ticketmanor_webapp to all exercises cloned from it.
"""
import subprocess, os, glob, sys
projects = []
ex_dir = '/crs1906/exercises'
os.chdir(ex_dir)
try:
    for d in [
        '*ex01_*',
        '*ex02_*',
        '*ex03_*',
        '*ex04_*',
        '*ex09_*',
        '*ex10_*',
    ]:
        os.chdir(ex_dir)
        for clone in glob.glob(d):
            os.chdir(ex_dir + '/' + clone)
            if not subprocess.call(r'hg pull ..\ticketmanor_webapp'):
                if not subprocess.call(r'hg update'):
                    projects.append(clone)
                else:
                    raise Exception("Couldn't update in {}, bailing", clone)
            else:
                raise Exception("Couldn't pull to {}, bailing", clone)
    print('\nFinished')
except Exception as e:
    print('Failed')
    print(e)
finally:
    if len(projects):
        print('Updated these projects from ticketmanor_update:',
              ', '.join(projects), sep='\n')
