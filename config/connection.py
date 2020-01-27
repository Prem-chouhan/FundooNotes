import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

from model import dbmanipulate
from .singleton import singleton


@singleton
class DbConnect:

    def __init__(self, **kwargs):
        self.connection = self.connect(**kwargs)

    def connect(self, **kwargs):
        mydb = mysql.connector.connect(
            host=kwargs["host"],
            port=kwargs["port"],
            user=kwargs["user"],
            passwd=kwargs["passwd"],
            database=kwargs["database"],

        )

        return mydb

    def queryExecute(self, sql, val):
        self.mycursor = self.connection.cursor()
        self.mycursor.execute(sql, val)
        self.connection.commit()

    def query(self, sql):
        self.mycursor = self.connection.cursor()
        self.mycursor.execute(sql)
        self.connection.commit()

    def queryfetch(self, sql):
        self.mycursor = self.connection.cursor()
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()

    def disconnect(self):
        self.connection.close()


con = DbConnect(host=os.getenv("HOST"),
                port=os.getenv("PORT"),
                user=os.getenv("USER_db"),
                passwd=os.getenv("PASSWD"),
                database=os.getenv("DATABASE"))
