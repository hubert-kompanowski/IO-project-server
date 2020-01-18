import unittest
from server_src.database_operations import *


class MyTestCase(unittest.TestCase):

    def test_group_add(self):
        req = {
            'group_name': 'test',
            'group_description': 'test',
            'group_members': ["Hubix", "alicja"]
        }

        cnx = data_base_connection()
        info = group_add(cnx, req)

        cnx = data_base_connection()
        resp = execute_query("Select * from grupa where nazwa_grupy like 'test';", cnx)

        cnx.commit()
        cnx.close()

        cnx = data_base_connection()

        query = f"SELECT grupa_id FROM grupa WHERE nazwa_grupy='test';"
        resp = execute_query(query, cnx)
        group_id = resp[0][0]

        query = f"Delete from grupa_klient where grupa_id='{group_id}';"
        with cnx.cursor() as cursor:
            cursor.execute(query)

        query = "Delete from grupa where nazwa_grupy like 'test';"
        with cnx.cursor() as cursor:
            cursor.execute(query)
        cnx.commit()
        cnx.close()

        if len(resp) == 0:
            self.fail('len(resp) == 0')

        self.assertTrue(info == 'Added')


if __name__ == '__main__':
    unittest.main()
