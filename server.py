import argparse
import sys
import json
import jwt
import cgi

from model import dbmanipulate
from http.server import HTTPServer, BaseHTTPRequestHandler
from view.userservice import user
from view.response import Response
from auth.login_required import is_authenticated,response
from config.redis_connection import RedisService

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 120


class Server(BaseHTTPRequestHandler):

    # def _set_headers(self):
    #     self.send_response(200)
    #     self.send_header("Content-type", "json")
    #     self.end_headers()

    def _html(self, message=None):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        # content = f"<html><body><h1>{message}</h1></body></html>"
        content = '''<html><body> <form enctype ="multipart/form-data" action ="/api/profile" method = "post"> 
        <p>File: <input type = "file" name = "upfile" /></p> <p><input type = "submit" value = "Upload" /></p>
         </form> </body></html>'''
        return content  # NOTE: must return a bytes object!

    def do_GET(self):
        # self._set_headers()

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

        elif self.path == '/upload':

            # with open('templates/profileupload.html', 'r') as f:
            #     html_string_register = f.read()

            Response(self).html_response(status=200,data=self._html())

        elif self.path == '/listing':
            obj = user
            catch, respon, res = obj.listing_notes(self)
            response_data = {'success': True, "data": [],
                             "message": "This is listing Of is_pinned{}{}{}".format(catch, respon, res)}
            Response(self).jsonResponse(status=404, data=response_data)


        else:
            # response_data = {'success': False, "data": [], "message": "URL Invalid"}
            # Response(self).jsonResponse(status=404, data=response_data)
            with open('templates/error.html', 'r') as f:
                html_string_register = f.read()
                # self.wfile.write(self._html(html_string_register))

    @is_authenticated
    def do_POST(self):

        if self.path == '/register':
            obj = user
            obj.register_user(self)

        elif self.path == '/login':
            obj = user
            obj.login_user(self)

        elif self.path == '/forgot':
            obj = user
            obj.forgot_password(self)

        elif '/reset' in self.path:
            try:
                from urllib.parse import urlparse, parse_qs
                query_components = parse_qs(urlparse(self.path).query)
                token = query_components["token"][0]
                print(token)
                token = jwt.decode(token, "secret", algorithms='HS256')
                key = token["email_id"]
                obj = user
                obj.update_confirmation(self, key)
            except json.decoder.JSONDecodeError:
                response_data = {'success': False, "data": [], "message": "Json decode Error raised"}
                Response(self).jsonResponse(status=404, data=response_data)

            except jwt.exceptions.DecodeError:
                response_data = {'success': False, "data": [], "message": "JWT decode error raised"}
                Response(self).jsonResponse(status=404, data=response_data)

        elif self.path == '/api/note/insert':
            obj = user
            # catch = self.headers['token']
            # flag = obj.authenticate_user(self, catch)
            print('--->here')
            obj = user
            obj.insert_note(self)
            #
            # response_data = {'success': False, "data": [], "message": "User Should have to register"}
            # Response(self).jsonResponse(status=404, data=response_data)


        elif self.path == '/api/profile':

            import cgi, os

            print(self.headers)

            token = self.headers['token']
            payload = jwt.decode(token, "secret", algorithms='HS256')
            print(payload)
            id = payload['id']

            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")

            if ctype == 'multipart/form-data':
                form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST',
                                                                                      'CONTENT_TYPE': self.headers[
                                                                                          'Content-Type'], })

                filename = form['upfile'].filename
                data = form['upfile'].file.read()

                open("./media/%s" % filename, "wb").write(data)

                profile_data={
                    'profile_path':f'./media/{filename}',
                    'id':id
                }
                from model.dbmanipulate import DbManaged
                obj=DbManaged()
                obj.update_profile(profile_data)

        else:
            response_data = {'success': False, "data": [], "message": "URL Invalid"}
            Response(self).jsonResponse(status=404, data=response_data)

    @is_authenticated
    def do_PUT(self):
        if self.path == '/api/note/update':
            obj = user
            catch = self.headers['token']
            flag = obj.authenticate_user(self, catch)
            if flag:
                obj = user
                obj.update_note(self)
            else:
                response_data = {'success': False, "data": [], "message": "User Should have to register"}
                Response(self).jsonResponse(status=404, data=response_data)

    @is_authenticated
    def do_DELETE(self):
        if self.path == '/api/note/delete':
            obj = user
            catch = self.headers['token']
            flag = obj.authenticate_user(self, catch)
            if flag:
                obj = user
                obj.delete_note(self)
            else:
                response_data = {'success': False, "data": [], "message": "User Should have to register"}
                Response(self).jsonResponse(status=404, data=response_data)


def run(server_class=HTTPServer, handler_class=Server, addr="localhost", port=8888):
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
