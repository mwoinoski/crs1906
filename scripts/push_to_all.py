"""
Pushes changes from ticketmanor_webapp to all solutions and exercises 
cloned from it.
"""

import subprocess, os

ex_dir = '/crs1906/exercises'

pull = r'hg pull'
merge = r'hg merge'
commit = r'hg commit -m "Merged from ticketmanor"'
# for solutions, hg pulls from ticketmanor. 
# for exercises, hg pulls from the solution.

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
	'ex09_multiprocessing',
]

projects = []
try:
    for clone in clones:
		print('Updating', clone)
		os.chdir(ex_dir + '/' + clone)
		if not subprocess.call(pull):
			if not subprocess.call(merge):
				if not subprocess.call(commit):
					projects.append(clone)
				else:
					raise Exception("Aborting, couldn't commit " + clone)
			else:
				raise Exception("Aborting, couldn't merge " + clone)
		else:
			raise Exception("Aborting, couldn't pull to " + clone)
    print('\nFinished')
except Exception as e:
    print('Failed', e)
finally:
    if len(projects):
        print('Updated these projects from ticketmanor_update:',
              ', '.join(projects), sep='\n')
