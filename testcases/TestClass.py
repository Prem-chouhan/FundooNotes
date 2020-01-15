# import pytest

import sys
import pytest

# sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/view')
from registration import registration

# sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/configration')
from db_connection import db_connection

sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/model')
from query import DbManaged


class TestClass:

    def test_register(self):
        obj = registration()
        assert email == premchouhan@gmail.com
        with pytest.raises(NameError):
            obj.register(email, password, confirm_password)

    def test_login(self):
        obj = registration
        with pytest.raises(NameError):
            obj.login(username, password)

    def test_forgotpassword(self):
        obj = registration
        with pytest.raises(NameError):
            obj.forgot_password(email)

    def test_connect(self):
        obj = db_connection
        with pytest.raises(NameError):
            obj.queryExecute(sql, val)

    def test_query(self):
        obj = db_connection
        with pytest.raises(NameError):
            obj.query(sql)

    def test_queryfetch(self):
        obj = db_connection
        with pytest.raises(NameError):
            obj.queryfetch(sql)

    def test_store(self):
        obj = registration
        with pytest.raises(NameError):
            obj.store(password)

    def test_insert(self):
        obj = registration
        with pytest.raises(NameError):
            obj.insert(tittle, description, color, isPinned, isArchive, isTrash)

    def test_update(self):
        obj = registration
        with pytest.raises(NameError):
            obj.update(id, tittle)

    def test_delete(self):
        obj = registration
        with pytest.raises(NameError):
            obj.delete(personid)

    def test_read(self):
        obj = registration
        with pytest.raises(NameError):
            obj.read(tablename)

    def test_create(self):
        obj = registration
        with pytest.raises(NameError):
            obj.create(tablename)

    def test_auth(self):
        obj = registration
        with pytest.raises(NameError):
            obj.auth(catch)

    def test_list(self):
        obj = registration()
        obj.list()

    def test_registration(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.registration(data)

    def test_loginUer(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.login_user(data)

    def test_emailexist(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.email_address_exists(data)

    def test_userexist(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.username_exists(data)

    def test_emailval(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.email_validate(email)

    def test_checkpassword(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.check_password(data)

    def test_updatepass(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.update_password(data, key)

    def test_smtp(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.smtp(email, message)

    def test_queryinsert(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.query_insert(data)

    def test_queryupdate(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.query_update(data)

    def test_querydelete(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.query_delete(data)

    def test_updateprofile(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.update_profile(data)

    def test_validatefile(self):
        obj = DbManaged
        with pytest.raises(NameError):
            obj.validate_file_extension(data)

    def test_listnotes(self):
        obj = DbManaged()
        # with pytest.raises(NameError):
        obj.list_notes()

    def test_listnote(self):
        obj = DbManaged()
        # with pytest.raises(NameError):
        obj.list_note()

    def test_listnot(self):
        obj = DbManaged()
        # with pytest.raises(NameError):
        obj.list_not()

    def test_validatesize(self):
        obj = DbManaged()
        with pytest.raises(NameError):
            obj.validate_file_size(data)
