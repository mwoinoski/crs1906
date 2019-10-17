"""
Trivial view to handle browser's request for /favicon.ico
"""
import os
from pyramid.response import FileResponse


def favicon_view(request):
    here = os.path.dirname(__file__)
    icon = os.path.join(here, '..', 'html', 'favicon.ico')
    return FileResponse(icon, request=request)


# class FavIconView:
#     """View Callable for returning /html/favicon.ico"""
# 
#     def __init__(self, request):
#         self._request = request
# 
#     # URLs are mapped to route names in __init__.py with Configurator.add_route()
# 
#     # Pyramid calls this method for a request like this:
#     # http://localhost:6543/favicon.ico
#     def favicon_view(self, request):
#         here = os.path.dirname(__file__)
#         icon = os.path.join(here, '..', 'html', 'favicon.ico')
#         return FileResponse(icon, request=request)
