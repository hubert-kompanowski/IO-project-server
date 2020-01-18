from unittest import TestCase
from server_src.operations import *
from server_src.database_operations import *


class TestCheckUser(TestCase):

    def test_check_user(self):

        req = {'name': 'TEST',
               'surname': 'TEST',
               'login': 'TEST',
               'password': 'TEST',
               'birth_date': '1998-12-12',
               'email': 'TEST@TEST.com'}

        cnx = data_base_connection()
        info = add_new_user(cnx, req)

        cnx = data_base_connection()
        resp = execute_query("Select * from klient where login like 'TEST';", cnx)

        cnx.commit()
        cnx.close()



        if len(resp) != 0 and info.startswith('Added user'):
            cnx = data_base_connection()


            req = {'login':'TEST',
                   'password':'TEST'}

            id = check_user(cnx, req)



            cnx = data_base_connection()
            query = "Delete from klient where login like 'TEST';"
            with cnx.cursor() as cursor:
                cursor.execute(query)
            cnx.commit()
            cnx.close()

            if id == 0:
                self.fail('Login failed')
        else:
            cnx = data_base_connection()
            query = "Delete from klient where login like 'TEST';"
            with cnx.cursor() as cursor:
                cursor.execute(query)
            cnx.commit()
            cnx.close()
            self.fail('Failed due to adding user')

