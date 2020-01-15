import json
import sys

sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/microservices/')

from nameko.web.handlers import http
# from microservices import registration
from login import *
from nameko.rpc import rpc, RpcProxy


class headers():

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "json")
        self.end_headers()


class HttpService(object):
    name = "test"

    @http('GET', '/test')
    # @rpc
    def get_method(self, request):
        with open('templates/login.html', 'r') as f:
            html_string_login = f.read()
            self.wfile.write(self._html(html_string_login))
        # obj = HttpServices
        # catch = obj.login(self)
        print("yugcdbc")
        login123 = RpcProxy('login')
        self.login.login()
        print(catch)
        # third = int(request.args.get('third', 1))
        return json.dumps({'value': catch})
