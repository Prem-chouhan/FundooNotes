import unittest

import sys

# from view.registration.registration import register

sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/view/')
from registration import registration


class MyTestCase(unittest.TestCase):

    def test_register(self):
        with pytest.raises(FileNotFoundError):
            obj = rg.insert_user(self)
            obj.register_user()

    # def test_login(self):
    #     obj.login()


if __name__ == '__main__':
    unittest.main()
