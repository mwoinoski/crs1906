LEARNING TREE 
COURSE 1906 - ADVANCED PYTHON: BEST PRACTICES AND DESIGN PATTERNS

This file describes how to configure your system to run the examples from
Learning Tree International's "Advanced Python: Best Practices and Design 
Patterns" using the software from the course. 

For 90 days after the course, Learning Tree provides you with a Computing 
Sandbox, which is the same virtual machine that you used during the course. 
If you prefer, you can work on the course exercises using the Sandbox 
instead of installing all the required software on your computer. To access 
the Computing Sandbox, log into the Learning Tree web site at 
www.LearningTree.com/MyLearningTree and then navigate to:
   Course History > Advanced Python > Details > Computing Sandbox

Links for software packages for other hardware and software are included at the
end of this file. For instructions on configuring Python applications using
other hardware or software, you can register for an hour of free After-Course
Instructor Coaching from the My Learning Tree page of the Learning Tree web
site. Log into the Learning Tree web site at www.LearningTree.com/MyLearningTree
and then navigate to:
   Course History > Advanced Python > Details > After Course Instructor Coaching

Note that most of the software used in the course is open-source and
may be used for any purpose, including commercial applications, with no
restrictions. However, before using open-source software in a commercial
application, you should check the software's licensing requirements. The
license is usually included in the distribution.

OVERVIEW

1. Unzip course 1906 projects
2. Install Python 3.14
3. Install PyCharm
4. (Optional) Install Tcl/Tk
5. (Optional) Install Anaconda
6. Install MySQL
7. Test a class project


DETAILS

The software distributions included in this zip file are for 64-bit Windows 
systems. See the end of this file for links to download installation packages 
for other systems.

Unzip Course 1906 Projects
    Unzip crs1906.zip to the directory of your choice.
    In the steps below, the directory that contains the crs1906 files will be 
    referred to as INSTALL_DIR
    
    
Install Python 3.13
    If you already have Python 3.13 installed, skip this step.
    Otherwise, download the Python 3.13 installer from
    https://www.python.org/downloads
        Click the approprite link after "Looking for a specific release?"
        For a Windows 64-bit platform, select the link for 
        "Windows x86-64 executable installer"
    Run the Python 3.13 installer file to install Python to the directory
    of your choice.
        Install Python for all users; otherwise, MySQL will not find the
        required Python connector.
        If you want to use Python 3.13 as your default Python interpreter, in 
        the "Customize Python" step, click "Add Python 3.13 to PATH".
		If possible, select "Install for all users".
		If possible, select "Disable path length limit" on the final 
		"Setup was successful" dialog.
	NOTE: Python 3.13 is not the latest version of Python. But some modules 
	required by the TicketManor application (for example, Pyramid 2.0 or 
	SQLAlchemy 2.0) may not work with a newer version of Python. Remember that 
	you can install multiple versions of Python: simply choose a different 
	installation directory for each version. Just be sure to use Python 3.13 
	to build the virtual environments for the TicketManor applications.

               
Install PyCharm
    Download PyCharm Community Edition from
    https://www.jetbrains.com/pycharm/download
    Run the PyCharm installer to install PyCharm to the directory of 
    your choice.

    
Install Tcl/Tk (optional)
    If you want to run tkinter scripts (for example, the GUI unit test runner 
    script from the chapter 4 exercise), install the Tcl/Tk toolkit:
    1. Download the ActiveTcl Community Edition from
	   https://platform.activestate.com/ActiveState/ActiveTcl-8.6 
    2. Run the ActiveTcl installer to install ActiveTcl to the directory
       of your choice.

    
Install Ananconda (optional)
    If you want to run the Mandelbrot scripts from chapter 5, you'll need to 
    install several Python scientific programming and math modules. The easiest 
    way to get all the required modules is to install the Anaconda toolkit:
    1. Browse to https://www.anaconda.com/download
	2. Click the "Get Started" link
	3. Install Anaconda's Navigator application


Install MySQL
    Download the latest MySQL Community Server installer from
    http://dev.mysql.com/downloads/mysql/
		Select your operating system
		Download the appropriate installer
		On the next page, click the link "No thanks, just start my download"
    Run the installation package
		On the "Choose Setup Type" dialog, choose "Typical"
		Accept the option to run the MySQL Configurator
        In the Configurator, accept all defaults until you reach the settings
		for Accounts and Roles.
			Set Root Account Password
				MySQL Root Password: root
				Repeat Password: root
			MySQL User Accounts
				Add User
				Username: student
				Password: student
				Use the defaults for the other fields
		For the remaining configuration options, accept all defaults.
		
     After MySQL is installed and running, restore the ticketmanor database:
        Using a command prompt shell, cd to MySQL's `bin` directory
			On Windows: C:\Program Files\MySQL\MySQL Server x.x\bin
        Enter the following command:
            mysql -u root --password=root
        Enter the following MySQL commands:
            create database ticketmanor;
            quit;
        Type into the command line (all on one line):
            mysql -u root --password=root -f ticketmanor < INSTALL_DIR\crs1906\ticketmanor.sql
        
    Note: on a Windows system, the MySQL service starts automatically when 
	Windows starts. If you prefer to start MySQL manually, go to the Windows 
	Control Panel > Administrative Tools > double-click Services > 
	R-click MySQLxx > Properties > Startup type > Manual
    
    If you set the service to use manual startup, you can start and stop the 
    MySQL service from the Services applet by right-clicking MySQLxx
    
	Install MySQL Workbench (Optional)
		The class exercises do not require you to interact directly with MySQL; 
		however, you can optionally install the MySQL Workbench GUI from
		https://dev.mysql.com/downloads/workbench/


Test a class project
    Open a command prompt as administrator and execute the following commands:
		python -m pip install --upgrade pip
        set "PATH=INSTALL_DIR\crs1906\scripts;%PATH%"
        pip install pytest pytest-cov pylint mypy certifi mysql-connector-python
        cd INSTALL_DIR\crs1906\exercises\solution_ex01_inheritance
        python -m venv venv
        venv\Scripts\activate
		pip install setuptools 
        ticketmanor
    Note: the "python setup.py develop" may take several minutes to run because 
    it downloads and installs all dependencies of the TicketManor application. 
    Note: ticketmanor.bat is in INSTALL_DIR\crs1906\scripts.
    
    Wait for the command prompt to display the message "serving on 
    http://0.0.0.0:6543"
    If Windows Firewall displays a security alert, select Allow Access.
    Start a web browser (preferably Chrome or Firefox) and navigate to 
    http://localhost:6543/static/#/home
    Select Concerts.
    In the search box, enter "Berlin Philharmonic" and select Search.
    Confirm that the page displays four search results.
    In the command prompt, press <Ctrl><C> to stop the TicketManor server.
	Deactive the virtual environment by entering the command:
		deactivate
    
    Start PyCharm.
    Select File | Open | INSTALL_DIR/crs1906/exercises/solution_ex08_multiprocessing
    Set the project's Python interpreter by selecting  File | Settings | Project: solution_ex08_multiprocessing | Project Interpreter
    If a Python 3.13 interpreter is already selected, click OK. Otherwise, do 
    the following steps:
        Click "Add interpreter" to the right of the Project Interpreter dropdown.
		Select "Add Local Interpreter"
		Select "System Interpreter"
        Navigate to your Python 3.13 installation directory
        Select python.exe
		Click OK
		Click OK again
    In the project view, expand the pi_monte_carlo folder, then right-click pi.py
    and select "Run 'pi'"
		If you don't see "Run 'pi'" in the menu, wait a minute and try again.
    Confirm that the pi.py script executes with no errors.


Running other hands-on exercises
    Other hands-on exercises should work as described in the exercise manual, 
    with the following modifications:
    
    For projects based on the TicketManor web application 
    (exercises 1.1, 2.1, 3.1, 3.2, 8.1, 8.2), first verify the Python version
	is 3.13:
		python -V
	Next, run  the following commands before opening a project in PyCharm:
        cd INSTALL_DIR\crs1906\exercises\ex0n...
        python -m venv venv
        venv\Scripts\activate
		pip install certifi
        python setup.py develop
		ticketmanor
    After all dependencies are downloaded and installed:
        Open the project in PyCharm.
        Select File | Settings | Project: ... | Project Interpreter
        Click the "gear" icon to the right of the Project Interpreter dropdown.
        Select Add
        Navigate to the exercise directory's venv\Scripts folder.
        Select python.exe
    
    Some of the exercise steps in Exercises 8.1 and 8.2 refer to other 
    TicketManor deployments. Simply skip those steps.
	
	For the bonus section of Exercise 8.2, you need to install Python 3.14
	with the optional free-threaded binaries. Download the Python 3.14 
	installer from https://www.python.org/downloads. During the installation,
	be sure to select "Download free-threaded binaries" as shown on slide 8-17.
	
	You can run the Appendix A exercise that builds a C extension in the 
	Windows Subsystem for Linux (WSL) without installing additional software. 
	However, if you want to build the extension as a Windows DLL instead of a 
	Linux shared object file, you'll need the Microsoft Visual C++ compiler, 
	which requires you to install Visual Studio. The minimum installation will 
	require about 4GB of disk space.
	To install Visual Studio:
		1. Go to https://visualstudio.microsoft.com/downloads and download the 
		   installer for the Community Edition of Visual Studio. 
		2. Run the installer and select workloads "Python Development" and 
		   "Desktop Development with C++".
		3. After the installation is complete, you can run the Appendix A 
		   exercise as described in the exercise manual. You don't need to 
		   start Visual Studio.

    
Links to download software distributions:
    Python
        https://www.python.org/downloads
    PyCharm
        https://www.jetbrains.com/pycharm/download/
    ActiveTcl
        https://platform.activestate.com/ActiveState/ActiveTcl-8.6
    MySQL Community Server
        http://dev.mysql.com/downloads/mysql/
