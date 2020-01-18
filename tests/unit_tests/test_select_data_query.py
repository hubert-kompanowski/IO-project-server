from unittest import TestCase
from server_src.operations import *


class TestSelectDataQuery(TestCase):

    def test_select_data_query(self):
        list_of_data = ['A', 'B', 'C']
        tab_name = 'ABC'
        where_field = 'D'
        where_value = 'E'
        query = select_data_query(list_of_data, tab_name, where_field, where_value)

        expected_query = ("SELECT A, B, C FROM ABC WHERE D = 'E';")

        self.assertEqual(query, expected_query)
