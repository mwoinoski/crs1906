r"""
urllib_wrapper defines functions for sending HTTP requests to a REST API.
This module's API is similar to the non-standard `requests` module but
is implemented using the standard `urllib` module, so it has no dependencies
on non-standard modules.
"""

import json as jsonlib
import urllib.request
import urllib.error
import base64


def get(url, headers = None, creds = None):
    """ Send a GET request """
    return send_request(url, headers, creds, method='GET')


def post(url, headers = None, json = None, creds = None):
    """ Send a POST request """
    return send_request(url, headers, json, creds, method='POST')


def put(url, headers = None, json = None, creds = None):
    """ Send a PUT request """
    return send_request(url, headers, json, creds, method='PUT')


def delete(url, headers = None, json = None, creds = None):
    """ Send a DELETE request """
    return send_request(url, headers, json, creds, method='DELETE')


def send_request(url, headers = None, json = None, creds = None, method='GET'):
    if not headers:
        headers = {}  # Python doesn't allow a dict as a default value for a parameter

    request_data = None
    if json:
        request_data = jsonlib.dumps(json).encode('utf-8')

    # Create a request object
    req = urllib.request.Request(url, headers=headers, data=request_data, method=method)

    # Add basic authentication if required
    if creds:
        credentials = f'{creds[0]}:{creds[1]}'
        encoded_creds = base64.b64encode(credentials.encode('ascii')).decode('ascii')
        req.add_header('Authorization', f'Basic {encoded_creds}')

    try:
        # Make the request
        with urllib.request.urlopen(req) as response:
            # Parse the JSON response
            response_body = response.read()
            if response_body:
                response_data = jsonlib.loads(response_body.decode())
            return HttpResponse(response.status, response_data)

    except urllib.error.HTTPError as e:
        return HttpResponse(e.code, f'HTTP error occurred: {e.code}')
    except urllib.error.URLError as e:
        return HttpResponse(500, f'Failed to reach the server: {e.reason}')


class HttpResponse:
    """ Mimic the response from a call to a function in the `requests` module """
    def __init__(self, status_code, data = None):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data
