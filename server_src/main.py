# [START gae_python37_cloudsql_psql]

from flask import Flask
from flask import request

try:
    from server_src.operations import *
except ModuleNotFoundError or FileNotFoundError:
    from operations import *

try:
    from server_src.database_operations import *
except ModuleNotFoundError or FileNotFoundError:
    from database_operations import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def main():
    # return(request.json)

    cnx = data_base_connection()

    req = request.json

    if 'command' in req:

        command = req['command']
        if command == 'add_new_user':
            return add_new_user(cnx, req)

        if command == 'check_user':
            return check_user(cnx, req)

        if command == 'new_outgo':
            return new_outgo(cnx, req)

        if command == 'new_income':
            return new_income(cnx, req)

        if command == 'show_all':
            return show_all(cnx, req)

        if command == 'group_add':
            return group_add(cnx, req)

        if command == 'new_group_payment':
            return new_group_payment(cnx, req)

        if command == "show_balance":
            return show_balance(cnx, req)

        if command == "get_groups":
            return get_groups(cnx, req)

        if command == "show_history":
            return show_history(cnx, req)

        if command == "user_exist":
            return user_exist(cnx, req)


        else:
            return "not found command\n"

    else:
        return "command key not in request\n"


# [END gae_python37_cloudsql_psql]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
