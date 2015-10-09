@echo off
if exist venv (
	deactivate > \cygwin\tmp\setup.log 2>&1
	activate > \cygwin\tmp\setup.log 2>&1
	python setup.py clean > \cygwin\tmp\setup.log 2>&1
	python setup.py develop >> \cygwin\tmp\setup.log 2>&1
	pserve development.ini --reload
) else (
	echo.
	echo ERROR: Can't activate virtual environment. 
	echo Check that you are in the correct directory.
)
