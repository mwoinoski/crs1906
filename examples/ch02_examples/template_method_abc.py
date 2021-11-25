"""
template_method.py - demo Template Method design pattern from Chapter 2
"""

import re
from abc import ABCMeta, abstractmethod

RESPONSE_TEMPLATE = """\
<html>
    <head><title>{}</title></head>
    <body>
        <h3>{}</h3>
    </body>
</html>
"""

class HttpRequestProcessor(metaclass=ABCMeta):
    def service_request(self, request):
        # Generic: parse request data
        request_data = self.parse_request(request)

        # App-specific: process request data
        if request['method'] == 'GET':
            # Call subclass do_get() method
            response_data = self.do_get(request_data)

        elif request['method'] == "POST":
            # Call subclass do_post() method
            response_data = self.do_post(request_data)

        else:
            raise NotImplementedError(
                    f"HTTP method {request.method} not implemented")

        # Generic: prepare HTML response
        self.return_response(response_data)

    def parse_request(self, request):
        if request['method'] == "GET":
            return self.decode_get_params(request['url'])
        elif request['method'] == "POST":
            return self.decode_post_params(request['body'])
        else:
            raise NotImplementedError(
                    f"HTTP method {request.method} not implemented")

    @abstractmethod
    def do_get(self, request):
        pass

    @abstractmethod
    def do_post(self, request):
        pass

    def return_response(self, resp_data):
        response = RESPONSE_TEMPLATE.format(
            "Success" if resp_data and resp_data['status'] < 400 else "Error",
            resp_data['message'] if resp_data else '')
        print(response)

    def decode_get_params(self, request_data):
        params = re.search(r"\?(.*)", request_data).group(1)
        return self.get_cgi_data(params)

    def decode_post_params(self, request_data):
        return self.get_cgi_data(request_data)

    @staticmethod
    def get_cgi_data(string):
        return dict(name_value.split('=') for name_value in string.split('&'))


class AddUserFormProcessor(HttpRequestProcessor):
    def do_get(self, request_data):
        name = request_data['name']
        # get user data from database
        address = '123 Url Param St'  # fake it
        response_data = {
            'status': 200,  # OK
            'message': f"User '{name}' is at address '{address}'",
        }
        return response_data

    def do_post(self, request_data):
        name = request_data['name']
        address = request_data['address']
        # add user to database
        response_data = {
            'status': 201,  # Created
            'message': f"User '{name}' at address '{address}' added successfully",
        }
        return response_data

if __name__ == "__main__":
    http_processor = AddUserFormProcessor()
    get_request = {'method': 'GET',
                   'url': '/add_user?name=Gertie Get'}
    http_processor.service_request(get_request)

    get_request = {'method': 'POST',
                   'body': 'name=Peter Post&address=456 Request Body Blvd'}
    http_processor.service_request(get_request)
