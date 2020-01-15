import os, \
    sys, \
    jwt, \
    cgi, \
    smtplib, \
    base64

from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# from ..model.query import DbManaged

# sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/model')
# sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/view')
from view.response import Response
from model.query import DbManaged
# from view import registration
import pdb

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 120


object = DbManaged()

class registration:

    def register(self):
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
        data['confirm_password'] = form['confirm_password'].value
        success = object.email_address_exists(data)
        present = object.email_validate(form['email'].value)
        if not present:
            response_data.update(
                {"message": "Email Format is Invalid please Re-enter Email", "success": False})
            Response(self).jsonResponse(status=202, data=response_data)
        else:
            if success:
                object.registration(data)
                response_data.update({"success": True, "data": [], "message": "Registration Done Successfully"})
                Response(self).jsonResponse(status=202, data=response_data)
            else:
                response_data.update({"message": "Email Already Exists", "success": False})
                Response(self).jsonResponse(status=202, data=response_data)

    def login(self):
        """
        Here User can login and if The username already exists then it will give response or else
        it will give response of Login done successfully
        no return :return:
        """
        object = DbManaged()
        global jwt_token
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        response_data = {'success': True, "data": [], "message": ""}
        form_keys = list(form.keys())

        if len(form_keys) < 2:
            response_data.update({'success': False, "data": [], "message": " some values are missing"})
            Response(self).jsonResponse(status=404, data=response_data)
        data = {}
        data['username'] = form['username'].value
        data['password'] = form['password'].value
        success = object.username_exists(data)
        if success:
            object.login_user(data)
            username = data['username']
            payload = {
                'username': username,
                'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
            }
            encoded_token = jwt.encode(payload, 'secret', 'HS256').decode('utf-8')
            response_data.update(
                {'success': True, "data": [], "message": "Login Done Successfully Generated Token",
                 'token': encoded_token})
            # response_data.update({"message": "Login done successfully"})
            Response(self).jsonResponse(status=202, data=response_data)
            return encoded_token

        else:
            response_data.update({"message": "Username already exists", "success": False})
            Response(self).jsonResponse(status=202, data=response_data)

        # except KeyError:
        #     pass

    def forgot_password(self):
        """
        Here if User Forgot Password so can change password and here If want to reset he have to give email and then
        link will be sent to email and with that link the password will be reset
        no return :return:
        """
        global object
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        response_data = {'success': True, "data": [], "message": ""}
        data = {}
        data['email'] = form['email'].value
        present = object.email_address_exists(data)
        if present:
            response_data.update({"success": False, "message": "Wrong Credentials"})
            Response(self).jsonResponse(status=202, data=response_data)
        else:
            email = data['email']
            encoded = jwt.encode({"email_id": email}, 'secret', algorithm='HS256').decode("utf-8")
            message = f"http://127.0.0.1:8888/reset/?token={encoded}"
            object.smtp(email, message)
            response_data.update({"success": True, "message": "Successfully sent mail"})
            Response(self).jsonResponse(status=202, data=response_data)

    def store(self, key):
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

    def insert(self):
        """
        Here record is inserted in table and response is shown
        :return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        print("hcduhc")
        data['tittle'] = form['tittle'].value
        data['description'] = form['description'].value
        data['color'] = form['color'].value
        data['isPinned'] = form['isPinned'].value
        data['isArchive'] = form['isArchive'].value
        data['isTrash'] = form['isTrash'].value
        print(data)
        object.query_insert(data)
        response_data = {'success': True, "data": [], "message": "Inserted Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def update(self):
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
        # print(data)
        object.query_update(data)
        response_data = {'success': True, "data": [], "message": "Updated Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def delete(self):
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

    def read(self):
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
        # my_db_obj = DbManaged()
        data = {}
        data['tablename'] = form['tablename'].value
        print(data)
        object.query_read(data)
        response_data = {'success': True, "data": [], "message": "Read Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def create(self):
        """
         Here  creation of  table is done and response is shown
        no return:return:
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        data['tablename'] = form['tablename'].value
        # print(data)
        object.query_create(data)
        response_data = {'success': True, "data": [], "message": "created table Successfully"}
        Response(self).jsonResponse(status=404, data=response_data)

    def auth(self, catch):
        """
        this function is used to decode and check whether the user is authorized user or not
        :param catch:
        True:return:
        """
        try:
            print("chdshc")
            jwt_decode = jwt.decode(catch, JWT_SECRET, JWT_ALGORITHM)
            data = jwt_decode['username']
            # print(jwt_decode,"jndcjnjc")
            success = object.username_exists(data)
            # print(success)
            return success
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.DecodeError:
            return "Wrong Token"
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def updateProfile(self):
        object = DbManaged()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        data = {}
        # pdb.set_trace()
        data['path'] = form['path'].value
        data['id'] = form['id'].value
        # image = base64.b64encode(data['path'])
        # valid_image = image.decode("utf-8")
        flag = object.validate_file_extension(data)
        check = object.validate_file_size(data)
        # valid_image = image.decode("utf-8")
        # sql = "INSERT INTO Picture(path) VALUES (%s)"
        # val = (data['path'])
        # # obj = db_connection()
        # my_db_obj.queryExecute(sql, val)
        object.update_profile(data)
        # print(flag)
        # print(check)
        if flag and check:
            response_data = {'success': True, "data": [], "message": "Profile Updated Successfully"}
            Response(self).jsonResponse(status=404, data=response_data)
        else:
            response_data = {'success': True, "data": [], "message": "Unsupported file extension"}
            Response(self).jsonResponse(status=404, data=response_data)

    def list(self):
        catch = object.list_notes()
        respon = object.list_note()
        res = object.list_not()
        return catch, respon, res
