import argparse
import sys
import json
import jwt
import cgi

# sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/templates/')
# sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/view/')

# sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/model')
from model import query
from http.server import HTTPServer, BaseHTTPRequestHandler
from view.registration import registration
from view import response

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 120


class S(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "json")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()

        if self.path == '/register':
            with open('templates/register.html', 'r') as f:
                html_string_register = f.read()
                self.wfile.write(self._html(html_string_register))

        elif self.path == '/login':
            with open('templates/login.html', 'r') as f:
                html_string_login = f.read()
                self.wfile.write(self._html(html_string_login))

        elif self.path == '/forgot':
            with open('templates/forgot.html', 'r') as f:
                html_string_login = f.read()
                self.wfile.write(self._html(html_string_login))

        elif '/reset' in self.path:
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            token = query_components["token"][0]
            with open('templates/reset.html', 'r') as f:
                html_string_register = f.read()
                output = html_string_register.format(result=token)
                self.wfile.write(self._html(output))
        elif self.path == '/read':
            obj = registration
            obj.read(self)
        elif self.path == '/upload':
            with open('templates/profileupload.html', 'r') as f:
                html_string_register = f.read()
                self.wfile.write(self._html(html_string_register))

        elif self.path == '/listing':
            obj = registration
            catch, respon, res = obj.list(self)
            response_data = {'success': True, "data": [],
                             "message": "This is listing Of isPinned{}{}{}".format(catch, respon, res)}
            Response(self).jsonResponse(status=404, data=response_data)


        else:
            # response_data = {'success': False, "data": [], "message": "URL Invalid"}
            # Response(self).jsonResponse(status=404, data=response_data)
            with open('templates/error.html', 'r') as f:
                html_string_register = f.read()
                self.wfile.write(self._html(html_string_register))

    def do_HEAD(self):
        self._set_headers()
        pass

    def do_POST(self):

        if self.path == '/register':
            obj = registration
            obj.register(self)

        elif self.path == '/login':
            obj = registration
            obj.login(self)

        elif self.path == '/forgot':
            obj = registration
            obj.forgot_password(self)

        elif '/reset' in self.path:
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            token = query_components["token"][0]
            token = jwt.decode(token, "secret", algorithms='HS256')
            key = token["email_id"]
            print(key)
            obj = registration
            obj.store(self, key)

        elif self.path == '/insert':
            obj = registration
            print(self.headers['token'])
            catch = self.headers['token']
            flag = obj.auth(self, catch)
            if flag:
                obj = registration
                obj.insert(self)
            else:
                response_data = {'success': False, "data": [], "message": "User Should have to register"}
                Response(self).jsonResponse(status=404, data=response_data)

        elif self.path == '/create':
            obj = registration
            obj.create(self)

        elif self.path == '/profile':
            # self.send_response(200)
            # self.send_header("Content-type", "image/jpg")
            # self.send_header("Content-length", 20)
            # self.end_headers()
            # print(self.send_header)
            obj = registration
            obj.updateProfile(self)


        else:
            response_data = {'success': False, "data": [], "message": "URL Invalid"}
            Response(self).jsonResponse(status=404, data=response_data)

    def do_PUT(self):
        if self.path == '/update':
            obj = registration
            # print(self.headers['token'])
            catch = self.headers['token']
            flag = obj.auth(self, catch)
            if flag:
                obj = registration
                obj.update(self)
            else:
                response_data = {'success': False, "data": [], "message": "User Should have to register"}
                Response(self).jsonResponse(status=404, data=response_data)

    def do_DELETE(self):
        if self.path == '/delete':
            obj = registration
            print(self.headers['token'])
            catch = self.headers['token']
            flag = obj.auth(self, catch)
            if flag:
                obj = registration
                obj.delete(self)
            else:
                response_data = {'success': False, "data": [], "message": "User Should have to register"}
                Response(self).jsonResponse(status=404, data=response_data)


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8888):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8888,
        help="Specify the port on which the server listens",
    )
    args = parser.parse_args()
    run(addr=args.listen, port=args.port)
