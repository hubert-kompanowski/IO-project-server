import binascii
import hashlib
import os

import psycopg2

db_fields = {'klient': ["imie, nazwisko, login, email, haslo, data_urodzenia",
                        "'{}', '{}', '{}', '{}', '{}', '{}'"],

             'wydatek_osobisty': ["klient_id, kategoria, kwota, opis",
                                  "'{}', '{}', '{}', '{}'"],

             'przychod_osobisty': ["klient_id, kategoria, kwota, opis",
                                   "'{}', '{}', '{}', '{}'"],

             }


def insert_data_query(data: list, tab_name: str) -> str:
    """ Creates SQL query to insert some data to database.

    Args:
        data:       List of data to insert
        tab_name:   Type of data set

    Returns:
        Query string
    """

    query = ""
    if tab_name == 'klient':
        query = "INSERT INTO " + tab_name + " (" + db_fields[tab_name][0] + ") "
        query += "VALUES (" + db_fields[tab_name][1] + ");"
        query = query.format(data[0], data[1], data[2], data[3], data[4], data[5])
    elif tab_name == 'wydatek_osobisty':
        if data[3] is not None:
            query = "INSERT INTO " + tab_name + " (" + db_fields[tab_name][0] + ") "
            query += "VALUES (" + db_fields[tab_name][1] + ");"
            query = query.format(data[0], data[1], data[2], data[3])
        else:
            query = "INSERT INTO " + tab_name + " (" + "klient_id, kategoria, kwota" + ") "
            query += "VALUES (" + "'{}', '{}', '{}'" + ");"
            query = query.format(data[0], data[1], data[2])

    elif tab_name == 'przychod_osobisty':
        if data[3] is not None:
            query = "INSERT INTO " + tab_name + " (" + db_fields[tab_name][0] + ") "
            query += "VALUES (" + db_fields[tab_name][1] + ");"
            query = query.format(data[0], data[1], data[2], data[3])
        else:
            query = "INSERT INTO " + tab_name + " (" + "klient_id, kategoria, kwota" + ") "
            query += "VALUES (" + "'{}', '{}', '{}'" + ");"
            query = query.format(data[0], data[1], data[2])

    return query


def select_data_query(list_of_data, tab_name, where_field, where_value):
    """ Create SQL query to select some data.

    Args:
        list_of_data:   List of data
        tab_name:       Name of SQL table
        where_field:    Field to identify selection
        where_value:    Value of field to identify selection

    Returns:
        Query string
    """

    query = "SELECT "
    first = True
    for i in list_of_data:
        if first:
            query += i
            first = False
        else:
            query += ", " + i
    query += " FROM " + tab_name + " WHERE " + where_field + " = '{}';".format(where_value)
    return query


def data_base_connection():
    """ Create database connection.

    Returns:
        Database handler
    """
    cnx = psycopg2.connect('postgres://ejghyueefenfne:'
                           '8fa6d202f1c8f8e9ab99335a6843e2b68d66f2c409a81842681dff76e4dcc2d9@'
                           'ec2-54-246-121-32.eu-west-1.compute.amazonaws.com:5432/d98v78i1nijesv')
    return cnx


def execute_query(query, cnx):
    """ Send query to SQL database server and execute it.

    Args:
        query:  Query to execute
        cnx:    Database handler

    Returns:
        Response from SQL server
    """

    with cnx.cursor() as cursor:
        cursor.execute(query)
        resp = cursor.fetchall()
        return resp


def hash_password(password: str) -> str:
    """ Hash a password for storing

    Args:
        password:   Password to hash

    Returns:
        Hashed password
    """

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """ Verify a stored password against one provided by user

    Args:
        stored_password:    Password from database
        provided_password:  Password from user input

    Returns:
        bool: True if password is correct, False otherwise.
    """
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password,
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
