import unittest

import sys
from FunDooapp.view.registration.registration import register

sys.path.insert(0, '/home/admin-1/PycharmProjects/FunDooapp/view/registration')


class MyTestCase(unittest.TestCase):

    def test_register(self):
        with pytest.raises(FileNotFoundError):
            obj = rg.registration(self)
        register()

    # def test_login(self):
    #     obj.login()


if __name__ == '__main__':
    unittest.main()
