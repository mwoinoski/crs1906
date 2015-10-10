"""
Script to register a Pyramid-based web app running on the CherryPy web server
as a Windows service. See http://www.cherrypy.org/
    pip install cherrypy

Requires PyWin32. To install in a virtual env, you need to run easy_install
(not pip) and point directly to the PyWin32 installer:
    easy_install C:\\Users\\user\\Downloads\\pywin32-219.win-amd64-py3.4.exe
Ignore the SyntaxError mapi/demos/mapisend.py. It won't affect the install.

You can register the service with the system by running:
    python pyramidsvc.py install

Start the service through the normal service snap-in for the 
Microsoft Management Console or by running:
    python pyramidsvc.py start

If you want your service to start automatically you can run:
    python pyramidsvc.py --startup=auto update

From http://pyramid-cookbook.readthedocs.org/en/latest/deployment/windows.html
"""

# Uncomment the next import line to get print to show up or see early 
# exceptions.
# If there are errors, then run
#     python -m win32traceutil
# to see the output.
#import win32traceutil
import win32serviceutil

PORT_TO_BIND = 80
CONFIG_FILE = 'development.ini'
SERVER_NAME = 'www.ticketmanor'

SERVICE_NAME = "TicketManor"
SERVICE_DISPLAY_NAME = "TicketManor Web App"
SERVICE_DESCRIPTION = "TicketManor Web App demo for Python course 1906"

class PyWebService(win32serviceutil.ServiceFramework):
    """Python Web Service."""

    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME
    _svc_deps_ = None        # sequence of service names on which this depends
    _svc_description_ = SERVICE_DESCRIPTION

    def SvcDoRun(self):
        from cherrypy import wsgiserver
        from pyramid.paster import get_app
        import os, sys

        path = os.path.dirname(os.path.abspath(__file__))

        os.chdir(path)

        app = get_app(CONFIG_FILE)

        self.server = wsgiserver.CherryPyWSGIServer(
                ('0.0.0.0', PORT_TO_BIND), app,
                server_name=SERVER_NAME)

        self.server.start()


    def SvcStop(self):
        self.server.stop()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PyWebService)
