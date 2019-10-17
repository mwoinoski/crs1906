@echo off
if exist venv (
	deactivate > nul 2> nul
	activate > nul 2> nul
	python setup.py clean develop > \software\cygwin\tmp\setup.log 2>&1
	pserve development.ini --reload
) else (
	echo.
	echo ERROR: Can't activate the virtual environment. 
	echo Check that you are in the correct directory.
)
