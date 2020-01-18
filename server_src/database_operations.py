import json

try:
    from server_src.operations import *
except ModuleNotFoundError or FileNotFoundError:
    from operations import *


def show_all(cnx, req):
    """ Showing all transactions for specified user

    Args:
        cnx: Database handler
        req: Incoming request, should contain 'id' key

    Returns:
        String like json object which contains all incomes and outgoings
    """
    if 'id' in req:
        query = select_data_query(['wydatek_osobisty_id', 'data_dodania', 'kategoria', 'kwota', 'opis'],
                                  'wydatek_osobisty', 'klient_id', req['id'])

        resp = execute_query(query, cnx)

        result = {'outgo': []}
        for r in resp:
            result['outgo'].append({'id': str(r[0]),
                                    'data': str(r[1])[0:16],
                                    'category': str(r[2]),
                                    'cost': str(r[3]),
                                    'description': str(r[4])})

        result['income'] = []
        query = select_data_query(['przychod_osobisty_id', 'data_dodania', 'kategoria', 'kwota', 'opis'],
                                  'przychod_osobisty', 'klient_id', req['id'])

        resp = execute_query(query, cnx)

        for r in resp:
            result['income'].append({'id': str(r[0]),
                                     'data': str(r[1])[0:16],
                                     'category': str(r[2]),
                                     'cost': str(r[3]),
                                     'description': str(r[4])})

        cnx.commit()
        cnx.close()

        summary = 0
        for k, v in result.items():
            if k == 'outgo':
                for i in v:
                    summary -= int(i['cost'])
            elif k == 'income':
                for i in v:
                    summary += int(i['cost'])

        result['summary'] = summary

        return json.dumps(result)
    else:
        return "bad arguments in request\n"


def new_income(cnx, req):
    """ Add new income

    Args:
        cnx: Database handler
        req: Incoming request, should contain 'id' key

    Returns:
        "Added" statement if an income was added
    """
    if 'id' in req \
            and 'category' in req \
            and 'cost' in req:

        if 'description' in req:
            des = req['description']
        else:
            des = None

        query = insert_data_query([req['id'], req['category'], req['cost'], des],
                                  'przychod_osobisty')
        with cnx.cursor() as cursor:
            cursor.execute(query)
        cnx.commit()
        cnx.close()
        return 'Added'

    else:
        return "bad arguments in request\n"


def new_outgo(cnx, req):
    """ Add new outgoing

    Args:
        cnx: Database handler
        req: Incoming request, should contain 'id' key

    Returns:
        "Added" statement if an income was added
    """
    if 'id' in req \
            and 'category' in req \
            and 'cost' in req:

        if 'description' in req:
            des = req['description']
        else:
            des = None

        query = insert_data_query([req['id'], req['category'], req['cost'], des],
                                  'wydatek_osobisty')
        with cnx.cursor() as cursor:
            cursor.execute(query)
        cnx.commit()
        cnx.close()
        return 'Added'

    else:
        return "bad arguments in request\n"


def check_user(cnx, req):
    """ Check if login and password are in database

    Args:
        cnx: Database handler
        req: Incoming request, should contain 'login' and 'password' key

    Returns:
        Id of logged user or 0
    """
    if 'login' in req and 'password' in req:

        query = select_data_query(['klient_id', 'login', 'haslo'], 'klient', 'login', req['login'])
        resp = execute_query(query, cnx)
        if len(resp) == 0:
            return "0"

        login = resp[0][1].strip()
        password = resp[0][2].strip()

        cnx.commit()
        cnx.close()

        if login == req['login'] and verify_password(password, (req['password'].encode('utf-8'))):
            return str(resp[0][0])
        else:
            return "0"

    else:
        return "bad arguments in request\n"


def add_new_user(cnx, req):
    """ Adding new user to database

    Args:
        cnx: Database handler
        req: Incoming request, should contain 'login', 'password', 'name', 'email',
             'birth_date' and 'surname' keys

    Returns:
        Statement like: "Added user: klient_id=<id>"
    """
    if 'name' in req \
            and 'login' in req \
            and 'email' in req \
            and 'password' in req \
            and 'birth_date' in req \
            and 'surname' in req:

        query = select_data_query(['login'], "klient", 'login', req['login'])
        resp = execute_query(query, cnx)
        if len(resp) != 0:
            login_check = resp[0][0].strip()
            if login_check == req['login']:
                return "User with this login already exists"

        query = select_data_query(['email'], "klient", 'email', req['email'])
        resp = execute_query(query, cnx)
        if len(resp) != 0:
            email_check = resp[0][0].strip()
            if email_check == req['email']:
                return "User with this email already exists"

        query = insert_data_query([req['name'], req['surname'], req['login'], req['email'],
                                   hash_password(req['password']), req['birth_date']], 'klient')
        with cnx.cursor() as cursor:
            cursor.execute(query)

        query = select_data_query(['klient_id', 'login'], "klient", 'login', req['login'])
        resp = execute_query(query, cnx)
        id_check = resp[0][0]
        login_check = resp[0][1].strip()
        result = "Added user: klient_id=" + str(id_check) + " login=" + req['login']

        cnx.commit()
        cnx.close()

        if req['login'] != login_check:
            return 'Error in adding klient'
        return result

    else:
        return "bad arguments in request\n"


def group_add(cnx, req):
    """ Add new group

    Args:
        cnx: Database handler
        req: Incoming request, should contain 'group_name' key

    Returns:
        "Added" statement
    """
    if 'group_name' in req:
        if 'group_members' not in req:
            return "'group_members' not in request"

        group_name = req['group_name']
        if 'group_description' in req:
            group_description = "'" + req['group_description'] + "'"
        else:
            group_description = 'NULL'

        if 'group_reset_date' in req:
            group_reset_date = "'" + req['group_reset_date'] + "'"
        else:
            group_reset_date = 'NULL'

        query = "INSERT INTO grupa (nazwa_grupy, opis_grupy, data_resetu_bilansu_grupy) "
        query += "VALUES ('{}', {}, {})".format(group_name, group_description, group_reset_date) + ';'

        with cnx.cursor() as cursor:
            cursor.execute(query)

        cnx.commit()
        cnx.close()

        cnx = data_base_connection()

        query = f"select grupa_id from grupa where nazwa_grupy='{group_name}' order by data_zalozenia_grupy desc;"

        resp = execute_query(query, cnx)
        group_id = resp[0][0]

        member_id = {}
        for name in req['group_members']:
            query = f"SELECT klient_id, login FROM klient WHERE login = '{name}';"
            resp = execute_query(query, cnx)
            member_id[resp[0][1]] = resp[0][0]

        for login, id in member_id.items():
            query = f"INSERT INTO grupa_klient (klient_id, grupa_id) VALUES ({id}, {group_id});"
            with cnx.cursor() as cursor:
                cursor.execute(query)

        cnx.commit()
        cnx.close()

        return "Added"

    else:
        return "group_name not in request"


def new_group_payment(cnx, req):
    """ Add new group payment

    Args:
        cnx: Database handler
        req: Incoming request, should contain ''quota', 'category', 'description', 'person_pay'

    Returns:
        "Added" statement or failed statement
    """

    if 'quota' in req and 'category' in req and 'description' in req and 'person_pay' in req and 'group_id' in req:
        quota = req['quota']
        category = req['category']
        description = req['description']
        person_pay = req['person_pay']
        group_id = req['group_id']

        query = f"SELECT klient_id, login FROM klient WHERE login = '{person_pay}';"
        resp = execute_query(query, cnx)
        person_pay_id = resp[0][0]

        query = f"INSERT INTO grupa_wydatki (placacy_id, grupa_id, kategoria, kwota, opis) " \
                f"VALUES ('{person_pay_id}', '{group_id}', '{category}', '{quota}', '{description}')"

        with cnx.cursor() as cursor:
            cursor.execute(query)
        cnx.commit()
        cnx.close()
        return "Added"

    else:
        return "Failed because of lack of information"


def get_groups(cnx, req):
    """ Get all users group

    Args:
        cnx: Database handler
        req: Incoming request, should contain 'login' key

    Returns:
        Json object with list of groups
    """
    if 'login' in req:

        login = req['login']

        query = f"SELECT klient_id, login FROM klient WHERE login = '{login}';"
        resp = execute_query(query, cnx)
        user_id = resp[0][0]

        query = f"SELECT grupa_id FROM grupa_klient WHERE klient_id = '{user_id}';"
        resp = execute_query(query, cnx)

        out = []
        for gr in resp[0]:
            query = f"SELECT nazwa_grupy FROM grupa WHERE grupa_id = '{gr}';"
            resp = execute_query(query, cnx)

            out.append(resp[0][0])

        return json.dumps({'groups': out})

    else:
        return '"login" not in reqest'


def show_balance(cnx, req):
    """ Show group balance

    Args:
        cnx: Database handler
        req: Incoming request, should contain 'login' and 'group_id' key

    Returns:
        Json object with group balance
    """
    if 'login' in req:
        if 'group_id' not in req:
            return 'group_id not in request'

        id = req['group_id']

        login = req['login']

        query = f"SELECT nazwa_grupy FROM grupa WHERE grupa_id={id};"
        resp = execute_query(query, cnx)
        group_name = resp[0][0]

        query = f"SELECT placacy_id, kwota FROM grupa_wydatki WHERE grupa_id={id};"
        resp = execute_query(query, cnx)

        bal = {}
        for k_id, quota in resp:
            query = f"SELECT login FROM klient WHERE klient_id = '{k_id}';"
            resp = execute_query(query, cnx)
            log = resp[0][0]

            if log in bal:
                bal[log].append(quota)
            else:
                bal[log] = [quota]

        members_number = len(bal)

        wisza = sum(bal[login]) / members_number

        out = []

        for l in bal:
            if l != login:
                out.append([l, round(100 * (wisza - sum(bal[l]))) / 100])

        data = {"group_name": group_name,
                "balance": out}

        return json.dumps(data)

    else:
        return "'login' not in request"


def show_history(cnx, req):
    """ Showing groups payment history

    Args:
        cnx: Database handler
        req: Incoming request, should contain 'login' key

    Returns:
        Json object with history list
    """
    if 'login' in req:
        if 'group_id' not in req:
            return 'group_id not in request'

        id = req['group_id']
        query = f"SELECT placacy_id, kategoria, kwota FROM grupa_wydatki WHERE grupa_id={id};"
        resp = execute_query(query, cnx)

        out = []
        for user_id, category, quota in resp:
            query = f"SELECT login FROM klient WHERE klient_id = '{user_id}';"
            resp = execute_query(query, cnx)
            user_login = resp[0][0]

            out.append([user_login, category, quota])

        return json.dumps({'history': out})

    else:
        return "'login' not in request"


def user_exist(cnx, req):
    """ Check if user with this login exists

    Args:
        cnx: Database handler
        req: Incoming request, should contain 'login' key

    Returns:
        "YES or "NO" strings
    """
    if 'login' in req:

        login = req['login']
        query = f"SELECT login FROM klient WHERE login = '{login}';"
        resp = execute_query(query, cnx)

        if len(resp) == 0:
            return "NO"

        log = resp[0][0]

        if log == login:
            return "YES"
        else:
            return "NO"

    else:
        return "'login' not in request"
