"""
http_server.py - Demonstration of Template Method design pattern from Chapter 2

This module uses the standard http.server modules to implement a simple
HTTP server. Run it, then test it with curl or Postman:
curl -X GET "http://localhost:7777/adduser?name=Homer&job=Chaos"
curl -X POST --data "name=Homer&job=Chaos" http://localhost:7777/adduser
"""

import sys
import re
import json
import socket

from http.server import HTTPServer, BaseHTTPRequestHandler

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'


# TODO: note definition of HttpRequestProcessor class
class HttpRequestProcessor(BaseHTTPRequestHandler):
    """Handle HTTP requests"""

    def get_request_line(self):
        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
        elif not self.raw_requestline:
            self.close_connection = 1

    # TODO: note the definition of the template method handle_one_request()
    def handle_one_request(self):
        """Handle a single HTTP request."""
        print('handle_one_request() called')
        try:
            # Generic setup
            self.get_request_line()
            if self.parse_request():
                if self.command in ('GET', 'POST'):
                    # A real HTTP server would also handle PUT, DELETE, etc.

                    # TODO: note call of generic get_request_data()
                    request_data = self.get_request_data()

                    # TODO: note call of do_get() and do_post() template
                    # methods defined in subclass
                    if self.command == 'GET':
                        resp, status = self.do_get(request_data)

                    elif self.command == 'POST':
                        resp, status = self.do_post(request_data)

                    # TODO: note call of generic return_response()
                    self.return_response(resp, status)

                else:
                    self.send_error(501, "Unsupported method (%r)" %
                                    self.command)
                    return
                # actually send the response if not already done.
                self.wfile.flush()
        except socket.timeout as e:
            # a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return

    # TODO: note the definition of get_request_data()
    def get_request_data(self):
        if self.command == 'GET':
            # Get the search params from the GET URL path
            match = re.search(r"\?(.*)", self.path)
            params = match.group(1) if match and match.group(1) else None
            request_data = self.get_cgi_data(params)
        elif self.command == 'POST':
            # Get the data from the body of the POST request
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)
            request_data = self.get_cgi_data(post_body.decode('utf-8'))
        return request_data

    def get_cgi_data(self, string):
        return {} if not string \
            else dict([name_value.split('=') for name_value in string.split('&')])

    # TODO: note the definition of return_response()
    def return_response(self, response_data, status):
        # Write the response
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # Convert the response data to JSON
        response_body = json.dumps(response_data)
        self.wfile.write(response_body.encode('utf-8'))


# TODO: note the definition of AddUserFormProcessor, a subclass of
# HttpRequestProcessor
class AddUserFormProcessor(HttpRequestProcessor):

    # TODO: note the definition of do_get()
    def do_get(self, request_data):
        """Handle GET request"""
        name = request_data['name']
        job = request_data['job']
        # Now use the GET params to add the user
        print('do_get() called with name = {}, job = {}'.format(name, job))
        # For this demo, we'll just echo the request data
        get_response = dict(request_data)
        return get_response, 200  # OK

    # TODO: note the definition of do_post()
    def do_post(self, request_data):
        """Handle POST request"""
        name = request_data['name']
        job = request_data['job']
        # Now use the POST params to add the user.
        print('do_post() called with name = {}, job = {}'.format(name, job))
        # For this demo, we'll just echo the request data
        post_response = dict(request_data)
        return post_response, 201  # Created


host = 'localhost'
http_port = 7777

if __name__ == "__main__":
    if len(sys.argv) > 1:
        http_port = int(sys.argv[1])
    server_address = (host, http_port)  # listen on localhost
    httpd = HTTPServer(server_address, AddUserFormProcessor)

    print("Server Started - {}:{}".format(host, http_port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server Stopped - {}:{}".format(host, http_port))

# def do_GET(self):  # called by BaseHTTPRequestHandler.handle_one_request
