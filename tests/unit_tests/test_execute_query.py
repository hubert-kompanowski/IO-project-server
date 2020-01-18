from unittest import TestCase
from server_src.operations import *


class TestExecuteQuery(TestCase):

    def test_execute_query(self):
        query = "SELECT now()"
        cnx = data_base_connection()

        resp = execute_query(query, cnx)

        resp_type = str(type(resp[0][0])).strip()

        expected_type = "<class 'datetime.datetime'>"

        self.assertEqual(resp_type, expected_type)
