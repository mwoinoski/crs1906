"""
Pushes changes from ticketmanor_webapp to all solutions and exercises 
cloned from it.
"""

import subprocess, os

ex_dir = '/crs1906/exercises'

build = r'python setup.py develop'

clones = [
    'solution_ex01_inheritance',
    'ex01_inheritance',
    'solution_ex02_template_method',
    'ex02_template_method',
    'solution_ex03_unit_testing',
    'ex03_unit_testing',
    'solution_ex03_with_mocks',
    'ex03_with_mocks',
    'solution_ex09_concurrency',
    'ex09_concurrency',
    'solution_ex09_multiprocessing',
]

projects = []
try:
    for clone in clones:
        print('\n', '='*35, ' Building ' '='*35, clone)
        os.chdir(ex_dir + '/' + clone)
        if subprocess.call(build):
            print("Couldn't build", clone)
    print('\nFinished')
except Exception as e:
    print('Failed', e)
finally:
    if len(projects):
        print('Built these projects :', ', '.join(projects), sep='\n')
