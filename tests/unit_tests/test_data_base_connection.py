from unittest import TestCase
from server_src.operations import *


class TestDataBaseConnection(TestCase):
    def test_data_base_connection(self):
        cnx = data_base_connection()

        if cnx.closed != 0:
            self.fail()
