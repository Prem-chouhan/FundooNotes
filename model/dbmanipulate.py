import re
from email.mime.text import MIMEText
from config.connection import DbConnect
import os
from config.connection import con

my_db = con


class DbManaged:

    def __init__(self):
        pass

    def insert_user(self, email, password):
        """Insert Query is fired Here and registration is done"""
        sql = "INSERT INTO user(email,password) VALUES (%s, %s)"
        val = (email, password)
        my_db.queryExecute(sql, val)

    def read_email(self, email=None, id=None):
        id = None
        """Select Query is fired Here and email address is present or not is shown """
        sql = "SELECT email,id FROM user where email = '" + email + "'"
        result = my_db.queryfetch(sql)
        print(result)
        email, id = result[0]
        print(email, id)
        if id is not None:
            return id, email
        else:
            return None

    def email_validate(self, email):
        """Here email validation is done"""
        if re.match(f"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        return False

    def update_password(self, data, key):
        """Here password is updated with update query"""
        sql = "UPDATE user SET password = '" + data['password'] + "' WHERE email = '" + key + "' "
        my_db.query(sql)

    def query_insert(self, data):
        """
        Insert Query Fired
        Fields of table:param data:
        no:return:
        """
        print("inside insert query")
        sql = "INSERT INTO notes(tittle,description,color,is_pinned,is_archived,is_trashed,user_id) VALUES (%s,%s,%s," \
              "%s,%s,%s, %s) "
        val = (
        data['tittle'], data['description'], data['color'], data['is_pinned'], data['is_archived'], data['is_trashed'],
        data['user_id'])
        my_db.queryExecute(sql, val)

    def query_update(self, data):
        """
        Update query is fired
        key where to delete:param data:
        no:return:
        """
        sql = "UPDATE notes SET tittle = '" + data['tittle'] + "' WHERE id = '" + data['id'] + "' "
        my_db.query(sql)

    def query_delete(self, data):
        """
        Delete query is fired
        id :param data:
        no:return:
        """
        sql = "DELETE FROM notes WHERE id = '" + data['id'] + "'"
        my_db.query(sql)

    def update_profile(self, data):
        """
        Update query is fired
        key where to delete:param data:
        no:return:
        """
        # print(, type(data['user_id']))
        profile_path = data['profile_path']
        id=data['id']
        print(id)
        sql = "INSERT INTO profile(profile_path,user_id) VALUES (%s, %s)"
        val = (profile_path, id)
        my_db.queryExecute(sql, val)



    def validate_file_extension(self, data):
        import os
        ext = os.path.splitext(data['profile_path'])[1]  # [0] returns path+filename
        valid_extensions = ['.jpg']
        if not ext.lower() in valid_extensions:
            print("Unsupported file extension.")
        else:
            return True
            # raise ValidationError(u'Unsupported file extension.')

    def list_remainders(self):
        sql = "select * from notes where is_pinned = 1"
        catch = my_db.queryfetch(sql)
        return catch

    def list_archives(self):
        sql = "select * from notes where is_trashed = 1"
        catch = my_db.queryfetch(sql)
        return catch

    def list_trash(self):
        sql = "select * from notes where is_archived = 1"
        catch = my_db.queryfetch(sql)
        return catch

    def validate_file_size(self, data):
        filesize = len(data['profile_path'])
        if filesize > 10485760:
            print("The maximum file size that can be uploaded is 10MB")
        else:
            return True
