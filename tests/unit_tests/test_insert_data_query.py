from unittest import TestCase
from server_src.operations import *


class TestInsertDataQuery(TestCase):

    def test_insert_data_query(self):
        data = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        tab_name = 'klient'
        query = insert_data_query(data, tab_name)
        expected_query = ("INSERT INTO klient (imie, nazwisko, login, email, haslo, data_urodzenia) "
                          "VALUES ('A', 'B', 'C', 'D', 'E', 'F');")

        self.assertEqual(query, expected_query)
