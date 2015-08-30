"""
Script to register a Pyramid-based web app running on the CherryPy web server
as a Windows service.

You can register the service with the system by running:
    python pyramidsvc.py install

Start the service through the normal service snap-in for the 
Microsoft Management Console or by running:
    python pyramidsvc.py start

If you want your service to start automatically you can run:
    python pyramidsvc.py update --start=auto

From http://pyramid-cookbook.readthedocs.org/en/latest/deployment/windows.html

CherryPy: http://www.cherrypy.org/
pip install cherrypy
"""

# Uncomment the next import line to get print to show up or see early 
# exceptions.
# If there are errors, then run
#     python -m win32traceutil
# to see the output.
#import win32traceutil
import win32serviceutil

PORT_TO_BIND = 80
CONFIG_FILE = 'production.ini'
SERVER_NAME = 'www.pyramid.example'

SERVICE_NAME = "PyramidWebService"
SERVICE_DISPLAY_NAME = "Pyramid Web Service"
SERVICE_DESCRIPTION = """This will be displayed as a description \
of the serivice in the Services snap-in for the Microsoft \
Management Console."""

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