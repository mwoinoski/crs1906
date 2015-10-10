import json

from pyramid.response import Response
from pyramid.view import notfound_view_config


# this is used as a global handler for any view callable method that
# returns status 404
@notfound_view_config()
def notfound(request):
    return Response(
        body=json.dumps({"message": "no resource found at path {}"
                        .format(request.url)}),
        status='404 Not Found',
        content_type='application/json')
