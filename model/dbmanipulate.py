import sys
import re
from email.mime.multipart import MIMEMultipart
import smtplib
import socket
from email.mime.text import MIMEText
from configration.connection import db_connection
from email.mime.multipart import MIMEMultipart
import os

my_db = db_connection()


class DbManaged:

    def __init__(self):
        pass

    def registration(self, data):
        """Insert Query is fired Here and registration is done"""
        sql = "INSERT INTO Registration(email,password,confirm_password) VALUES (%s, %s, %s)"
        val = (data['email'], data['password'], data['confirm_password'])
        my_db.queryExecute(sql, val)

    # def login_user(self, data):
    #     """Insert Query is fired Here and Login is done"""
    #     sql = "INSERT INTO Login(username,password) VALUES (%s, %s)"
    #     val = (data['username'], data['password'])
    #     my_db.queryExecute(sql, val)

    def email_address_exists(self, data):
        """Select Query is fired Here and email address is present or not is shown """
        sql = "SELECT email FROM user where email = '" + data['email'] + "'"
        my_result = my_db.queryfetch(sql)
        if my_result:
            return False
        else:
            return True

    def username_exists(self, data):
        """Select Query is fired Here and username is present or not is shown """
        sql = "SELECT username FROM Login where username = '" + data['username'] + "'"
        my_result = my_db.queryfetch(sql)
        if my_result:
            return False
        else:
            return True

    def email_validate(self, email):
        """Here email validation is done"""
        if re.match(f"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        return False

    def check_password(self, data):
        """Password is check if the user old password is present in database or not"""
        sql = "SELECT password FROM Login where password = '" + data['password'] + "'"
        my_result = my_db.queryfetch(sql)
        if my_result:
            return True
        else:
            return False

    def update_password(self, data, key):
        """Here password is updated with update query"""
        sql = "UPDATE Registration SET password = '" + data['password'] + "' WHERE email = '" + key + "' "
        my_db.query(sql)

    def smtp(self, emailid, message):
        """
        Here message of reset link is sent to user
        email:param emailid:
        link message:param message:
        no :return:
        """
        import smtplib
        s = smtplib.SMTP(os.getenv("SMTP_EXCHANGE_SERVER"), os.getenv("SMTP_EXCHANGE_PORT"))
        s.starttls()
        s.login(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), os.getenv("SMTP_EXCHANGE_USER_PASSWORD"))
        msg = MIMEText(message)
        s.sendmail(os.getenv("SMTP_EXCHANGE_USER_LOGIN"), emailid, msg.as_string())
        s.quit()

    def query_insert(self, data):
        """
        Insert Query Fired
        Fields of table:param data:
        no:return:
        """
        sql = "INSERT INTO crud(tittle,description,color,isPinned,isArchive,isTrash) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (data['tittle'], data['description'], data['color'], data['isPinned'], data['isArchive'], data['isTrash'])
        my_db.queryExecute(sql, val)

    def query_update(self, data):
        """
        Update query is fired
        key where to delete:param data:
        no:return:
        """
        sql = "UPDATE crud SET tittle = '" + data['tittle'] + "' WHERE id = '" + data['id'] + "' "
        my_db.query(sql)

    def query_delete(self, data):
        """
        Delete query is fired
        id :param data:
        no:return:
        """
        sql = "DELETE FROM crud WHERE id = '" + data['id'] + "'"
        my_db.query(sql)

    # def query_read(self, data):
    #     print(data['tablename'])
    #     sql = "select * from " + data['tablename'] + ""
    #     self.mycursor.execute(sql)
    #     print(self.mycursor.fetchall())
    #
    # def query_create(self, data):
    #     key = data['tablename']
    #     print(key)
    #     sql = "CREATE TABLE " + key + "(id int NOT NULL AUTO_INCREMENT,LastName varchar(255) NOT NULL,FirstName " \
    #                                   "varchar(255),Age int,PRIMARY KEY (id)) "
    #     self.mycursor.execute(sql)
    #     self.mydb.commit()

    def update_profile(self, data):
        """
        Update query is fired
        key where to delete:param data:
        no:return:
        """
        sql = "UPDATE Picture SET path = '" + data['path'] + "' WHERE id = '" + data['id'] + "' "
        my_db.query(sql)

    def validate_file_extension(self, data):
        import os
        ext = os.path.splitext(data['path'])[1]  # [0] returns path+filename
        valid_extensions = ['.jpg']
        if not ext.lower() in valid_extensions:
            print("Unsupported file extension.")
        else:
            return True
            # raise ValidationError(u'Unsupported file extension.')

    def list_notes(self):
        sql = "select * from crud where isPinned = 1"
        catch = my_db.queryfetch(sql)
        return catch

    def list_note(self):
        sql = "select * from crud where isTrash = 1"
        catch = my_db.queryfetch(sql)
        return catch

    def list_not(self):
        sql = "select * from crud where isArchive = 1"
        catch = my_db.queryfetch(sql)
        return catch

    def validate_file_size(self, data):
        filesize = len(data['path'])
        if filesize > 10485760:
            print("The maximum file size that can be uploaded is 10MB")
        else:
            return True
