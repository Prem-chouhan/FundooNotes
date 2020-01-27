import os, \
    sys, \
    jwt, \
    cgi, \
    smtplib, \
    base64

from datetime import datetime, timedelta
from config.redis_connection import RedisService
from view.response import Response
from model.dbmanipulate import DbManaged
from view.utils import response
from vendor.smtp import smtp

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 100000000

object = DbManaged()


class user:

    def register_user(self):
        """
        Here Registration of the user is done and it will check if the customers email is existing in database or not if present response is sent
        and if not present registration is done
        no return type:return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        response_data = {'success': True, "data": [], "message": ""}
        form_keys = list(form.keys())
        if len(form_keys) < 3:
            response_data.update({'success': False, "data": [], "message": " some values are missing"})
            Response(self).jsonResponse(status=404, data=response_data)
        data = {}
        data['email'] = form['email'].value
        data['password'] = form['password'].value
        email = data['email']
        password = data['password']
        id = object.read_email(email)
        present = object.email_validate(email)
        print(id)
        if not present:
            response_data.update(
                {"message": "Email Format is Invalid please Re-enter Email", "success": False})
            Response(self).jsonResponse(status=202, data=response_data)
        else:
            if id is not None:
                object.insert_user(email, password)
                response_data.update({"success": True, "data": [], "message": "Registration Done Successfully"})
                Response(self).jsonResponse(status=202, data=response_data)
            else:
                response_data.update({"message": "Email Already Exists", "success": False})
                Response(self).jsonResponse(status=202, data=response_data)

    def login_user(self):
        """
        Here User can login and if The username already exists then it will give response or else
        it will give response of Login done successfully
        no return :return:
        """
        object = DbManaged()
        # global jwt_token
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        form_keys = list(form.keys())

        if 'email' and 'password' in form_keys:
            data = {}
            data['email'] = form['email'].value
            data['password'] = form['password'].value
            email = data['email']
            id, email = object.read_email(email=email)
            print(id, '--------->id')

            if id:
                payload = {
                    'id': id,
                    'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }

                encoded_token = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')

                redis_obj = RedisService()
                # id_key = id[0]
                redis_obj.set(id, encoded_token)
                print(redis_obj.get(id), '------------->r.get')

                res = response(success=True, message="Login Successfully", data=[{
                    "token": encoded_token
                }])

            Response(self).jsonResponse(status=200, data=res)
        else:
            Response(self).jsonResponse(status=400, data=response(message="credentials are missing"))

    def forgot_password(self):
        """
        Here if User Forgot Password so can change password and here If want to reset he have to give email and then
        link will be sent to email and with that link the password will be reset
        no return :return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        response_data = {'success': True, "data": [], "message": ""}
        data = {}
        data['email'] = form['email'].value
        data = data['email']
        present = object.read_email(data)
        if not present:
            response_data.update({"success": False, "message": "Wrong Credentials"})
            Response(self).jsonResponse(status=202, data=response_data)
        else:
            encoded = jwt.encode({"email_id": data}, 'secret', algorithm='HS256').decode("utf-8")
            message = f"http://127.0.0.1:8888/reset/?token={encoded}"
            # email_id = data['email']
            obj = smtp()
            obj.smtp(data, message)
            response_data.update({"success": True, "message": "Successfully sent mail"})
            Response(self).jsonResponse(status=202, data=response_data)

    def update_confirmation(self, key):
        """
        here password will be updated and response will be show password updated
        Successfully
        no return:return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['password'] = form['password'].value
        object.update_password(data, key)
        response_data = {'success': False, "data": [], "message": "Password Updated Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def insert_note(self):
        """
        Here record is inserted in table and response is shown
        :return:
        """
        print(self.headers['token'], '---->token')
        token = self.headers['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        print(payload)
        id = payload['id']
        print(id, '------>id')
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['tittle'] = form['tittle'].value
        data['description'] = form['description'].value
        data['color'] = form['color'].value
        data['is_pinned'] = form['is_pinned'].value
        data['is_archived'] = form['is_archived'].value
        data['is_trashed'] = form['is_trashed'].value
        data['user_id'] = id
        object.query_insert(data)
        response_data = {'success': True, "data": [], "message": "Inserted Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def update_note(self):
        """
        Here record is Updated in table and response is shown
        no return:return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['id'] = form['id'].value
        data['tittle'] = form['tittle'].value
        object.query_update(data)
        response_data = {'success': True, "data": [], "message": "Updated Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def delete_note(self):
        """
        Here record is Deleted in table and response is shown
        no return:return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['id'] = form['id'].value
        object.query_delete(data)
        response_data = {'success': True, "data": [], "message": "Deleted Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def read_note(self):
        """
        Here record is Read in table and response is shown
        no return:return:
        """
        object = DbManaged()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['tablename'] = form['tablename'].value
        print(data)
        object.query_read(data)
        response_data = {'success': True, "data": [], "message": "Read Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def create_note(self):
        """
         Here  creation of  table is done and response is shown
        no return:return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': "POST",
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['tablename'] = form['tablename'].value
        object.query_create(data)
        response_data = {'success': True, "data": [], "message": "created table Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    # def authenticate_user(self, catch):
    #     """
    #     this function is used to decode and check whether the user is authorized user or not
    #     :param catch:
    #     True:return:
    #     """
    #     try:
    #         jwt_decode = jwt.decode(catch, "secret", algorithms='HS256')
    #         data = jwt_decode['username']
    #         obj = DbManaged()
    #         flag = obj.read_email(data)
    #         return flag
    #     except jwt.ExpiredSignatureError:
    #         # return 'Signature expired. Please log in again.'
    #         response_data = {'success': False, "data": [], "message": "Signature expired. Please log in again."}
    #         Response(self).jsonResponse(status=404, data=response_data)
    #
    #     except jwt.DecodeError:
    #         # return "Wrong Token"
    #         response_data = {'success': False, "data": [], "message": "Wrong Token"}
    #         Response(self).jsonResponse(status=404, data=response_data)
    #
    #     except jwt.InvalidTokenError:
    #         # return 'Invalid token. Please log in again.'
    #         response_data = {'success': False, "data": [], "message": "Invalid token. Please log in again."}
    #         Response(self).jsonResponse(status=404, data=response_data)

    def updateProfile(self):
        object = DbManaged()
        print(self.headers['token'], '---->token')
        token = self.headers['token']
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        print(payload)
        id = payload['id']
        print(id, '------>id')
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        # pdb.set_trace()
        data['profile_path'] = form['profile_path'].value
        data['user_id'] = id
        key = data['user_id']
        # image = base64.b64encode(data['path'])
        # valid_image = image.decode("utf-8")
        flag = object.validate_file_extension(data)
        check = object.validate_file_size(data)
        # valid_image = image.decode("utf-8")
        # sql = "INSERT INTO Picture(path) VALUES (%s)"
        # val = (data['path'])
        # # obj = db_connection()
        # my_db_obj.queryExecute(sql, val)
        object.update_profile(data, key)
        # print(flag)
        # print(check)
        if flag and check:
            response_data = {'success': True, "data": [], "message": "Profile Updated Successfully"}
            Response(self).jsonResponse(status=404, data=response_data)
        else:
            response_data = {'success': True, "data": [], "message": "Unsupported file extension"}
            Response(self).jsonResponse(status=404, data=response_data)

    def listing_notes(self):
        reaminders = object.list_remainders()
        archive = object.list_archives()
        trash = object.list_trash()
        return reaminders, archive, trash
