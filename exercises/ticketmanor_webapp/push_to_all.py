"""
Pushes changes from ticketmanor_webapp to all exercises cloned from it.
"""
import subprocess, os, glob, sys
projects = []
os.chdir('/crs1906/exercises')
try:
    for d in [
        # '*ex01_*',
        # '*ex02_*',
        # '*ex03_*',
        # '*ex04_*',
        '*ex98_*',
        '*ex99_*',
    ]:
        for clone in glob.glob(d):
            os.chdir(os.path.abspath(clone))
            print(os.getcwd())
            if not subprocess.call(r'echo hg pull ..\ticketmanor_webapp'):
                if not subprocess.call(r'echo hg update'):
                    projects.append(clone)
                else:
                    raise Exception("Couldn't update in {}, bailing", clone)
            else:
                raise Exception("Couldn't pull to {}, bailing", clone)
    print('Finished')
except Exception as e:
    print('Failed')
    print(e)
finally:
    if len(projects):
        print('Updated these projects from ticketmanor_update:',
              ', '.join(projects), sep='\n')
