import mysql.connector
import sys
import os
from dotenv     import load_dotenv

load_dotenv()
sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/model')
from query import *

class db_connection:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if db_connection.__instance is None:
            db_connection()
        return db_connection.__instance

    def __init__(self):
        if db_connection.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            db_connection.__instance = self

        self.mydb = mysql.connector.connect(
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            user=os.getenv("USER_db"),
            passwd=os.getenv("PASSWD"),
            database=os.getenv("DATABASE"),

        )

    def queryExecute(self, sql, val):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def query(self, sql):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(sql)
        self.mydb.commit()

    def queryfetch(self, sql):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def debugger(self):
        pass

    def disconnect(self):
        self.mydb.close()
        pass

    def __del__(self):
        pass
