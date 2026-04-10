@echo off
if exist venv\Scripts\activate.bat (
	call venv\Scripts\activate.bat || goto :fail
	python setup.py clean develop || goto :fail
	pserve development.ini --reload
	set "RC=%ERRORLEVEL%"
	call deactivate >nul 2>&1
	exit /b %RC%
) else (
	echo.
	echo ERROR: Can't activate the virtual environment.
	echo Check that you are in the correct directory.
	exit /b 1
)

:fail
set "RC=%ERRORLEVEL%"
echo.
echo ERROR: TicketManor startup failed with exit code %RC%.
call deactivate >nul 2>&1
exit /b %RC%
