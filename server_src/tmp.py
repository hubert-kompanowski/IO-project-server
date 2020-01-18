from server_src.database_operations import *

cnx = data_base_connection()

query = f"select grupa_id from grupa where nazwa_grupy='{'test'}' order by data_zalozenia_grupy desc;"

resp = execute_query(query, cnx)
group_id = resp[0][0]

print(group_id)