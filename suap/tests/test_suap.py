import os
import sys
import unittest

from suap import Suap

from . import config

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSuap(unittest.TestCase):
    def setUp(self) -> None:
        self.suap_session = Suap(config.USERNAME, config.PASSWORD)

    def test_login(self) -> None:
        self.assertTrue(self.suap_session)

    def test_login_error(self) -> None:
        with self.assertRaises(ValueError):
            Suap("username", "password")

    def test_get_personal_data(self) -> None:
        personal_data = self.suap_session.get_personal_data()
        self.assertEqual(len(personal_data), 7)

if __name__ == "__main__":
    unittest.main()
