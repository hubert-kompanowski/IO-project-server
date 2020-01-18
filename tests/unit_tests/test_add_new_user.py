from unittest import TestCase
from server_src.operations import *
from server_src.database_operations import *


class TestAddNewUser(TestCase):

    def test_add_new_user(self):

        req = {'name': 'Adam',
               'surname': 'Kowalski',
               'login': 'AKowal',
               'password': 'kowal',
               'birth_date': '1998-12-12',
               'email': 'ad@kol.com'}

        cnx = data_base_connection()
        info = add_new_user(cnx, req)

        cnx = data_base_connection()
        resp = execute_query("Select * from klient where login like 'AKowal';", cnx)

        cnx.commit()
        cnx.close()

        cnx = data_base_connection()
        query = "Delete from klient where login like 'AKowal';"
        with cnx.cursor() as cursor:
            cursor.execute(query)
        cnx.commit()
        cnx.close()

        if len(resp) == 0:
            self.fail('len(resp) == 0')

        if info.startswith('Added user'):
            self.assertEqual(resp[0][3], req['login'], 'Dont equal')
        else:
            self.fail('Dont start with Added user')

