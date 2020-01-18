from unittest import TestCase
from server_src.operations import *
from server_src.database_operations import *


class TestShowAll(TestCase):

    def test_show_all(self):

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

            req = {'login': 'TEST',
                   'password': 'TEST'}

            id = check_user(cnx, req)

            req = {'id': str(id),
                   'category': 'ABC',
                   'cost': '50'}

            cnx = data_base_connection()
            info = new_outgo(cnx, req)

            cnx = data_base_connection()
            resp = execute_query("Select * from wydatek_osobisty where klient_id = '" + id + "';", cnx)

            req = {'id': str(id),
                   'category': 'ABC',
                   'cost': '50'}

            cnx = data_base_connection()
            info2 = new_income(cnx, req)

            cnx = data_base_connection()
            resp2 = execute_query("Select * from wydatek_osobisty where klient_id = '" + id + "';", cnx)

            if len(resp) == 0 or info != 'Added'  or len(resp2) == 0 or info2 != 'Added':
                self.fail('Added outgo failed')
            else:

                req = {"command": "show_all", "id": str(id)}
                cnx = data_base_connection()


                resp = json.loads(show_all(cnx, req))


                if len(resp['outgo']) ==0 or len(resp['income']) ==0 or int(resp['summary']) != 0:
                    self.fail('Show all failed')

            if id == 0:
                self.fail('Login failed')

            cnx = data_base_connection()
            query = "Delete from klient where login like 'TEST';"
            with cnx.cursor() as cursor:
                cursor.execute(query)
            cnx.commit()
            cnx.close()

            cnx = data_base_connection()
            query = "Delete from wydatek_osobisty where klient_id = '" + id + "';"
            with cnx.cursor() as cursor:
                cursor.execute(query)
            cnx.commit()
            cnx.close()

            cnx = data_base_connection()
            query = "Delete from przychod_osobisty where klient_id = '" + id + "';"
            with cnx.cursor() as cursor:
                cursor.execute(query)
            cnx.commit()
            cnx.close()

        else:
            cnx = data_base_connection()
            query = "Delete from klient where login like 'TEST';"
            with cnx.cursor() as cursor:
                cursor.execute(query)
            cnx.commit()
            cnx.close()

            cnx = data_base_connection()
            query = "Delete from wydatek_osobisty where kategoria = 'ABC';"
            with cnx.cursor() as cursor:
                cursor.execute(query)
            cnx.commit()
            cnx.close()

            cnx = data_base_connection()
            query = "Delete from przychod_osobisty where kategoria = 'ABC';"
            with cnx.cursor() as cursor:
                cursor.execute(query)
            cnx.commit()
            cnx.close()

            self.fail('Failed due to adding user')


