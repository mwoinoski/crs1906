"""
http_server.py - Demonstration of Template Method design pattern from Chapter 2

This module uses the standard http.server modules to implement a simple REST server.
Run it, then test it with curl or Postman:
curl -i -X GET http://localhost:7777/user?email=mike@wxyz.me
curl -i -X POST -d @request.json -H 'Content-Type: application/json'  http://localhost:7777
"""

__author__ = 'Mike Woinoski (michaelw@articulatedesign.us.com)'

import sys
import re
import json

from http.server import HTTPServer, BaseHTTPRequestHandler


class MyRequestHandler(BaseHTTPRequestHandler):
    """Handle REST requests"""

    def do_GET(self):  # called by BaseHTTPRequestHandler.handle_one_request
        """Handle GET request"""
        # Get the search params from the GET URL path
        params = self.decode_get_params(self.path)

        # Now use the params to look up something
        response = dict(params)  # fake it

        # Write the response
        self.send_response(200)  # 200 == OK
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # Convert the response data to JSON
        response_body = json.dumps(params)
        self.wfile.write(response_body.encode('utf-8'))

    def do_POST(self):  # called by BaseHTTPRequestHandler.handle_one_request
        """Handle GET request"""
        # Get the data from the body of the POST request
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_data = json.loads(post_body.decode('utf-8'))

        # Now use the posted JSON data
        print("do_POST received: " + str(post_data))

        # Write the response
        self.send_response(201)  # 201 == Created
        self.end_headers()

    def decode_get_params(self, request_data):
        match = re.search(r"\?(.*)", request_data)
        params = match.group(1) if match and match.group(1) else None
        return self.get_cgi_data(params)

    def get_cgi_data(self, string):
        return {} if not string \
            else dict([name_value.split('=') for name_value in string.split('&')])


host = 'localhost'
http_port = 7777

if __name__ == "__main__":
    if len(sys.argv) > 1:
        http_port = int(sys.argv[1])
    server_address = (host, http_port)  # listen on localhost
    httpd = HTTPServer(server_address, MyRequestHandler)

    print("Server Started - {}:{}".format(host, http_port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server Stopped - {}:{}".format(host, http_port))
