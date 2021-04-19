from dotenv import load_dotenv, dotenv_values
from flask import Flask, request, jsonify
from mysql.connector import connection, cursor
from flask_cors import CORS

from config import config
from general_functions import *

database_config = config["database"]
cnx = None
cursor = None

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app, resources={r'/*': {'origins': '*'}})


def action_create(request, **kwargs):
    pass


def action_delete(request, **kwargs):
    pass


def action_edit(request, **kwargs):
    pass


def action_display(request, **kwargs):
    cursor.execute(f"SELECT * FROM {kwargs['table']}")
    return cursor


actions = {
    "request_type": {
        "POST": {
            "create": action_create,
            "delete": action_delete,
            "edit": action_edit,
        },
        "GET": {
            "display": action_display,
        },
    },
}


@app.route("/<path:action>/<string:table>", methods=["GET", "POST"])
def endpoint_insert(action, table):
    ensure_db()

    res = None
    try:
        res = actions[request.method][action](request, table=table)
        return str(res.fetchall())
    except Exception as e:
        print(e)


# 8. store survey
@app.route("/survey/", methods=["GET", "POST"])
def survey():
    ensure_db()

    required = [
        "medicare",
        "dateOfBirth",
        "time",
        "temperature",
        "symptoms",
    ]

    if request.method == "POST":
        data = request.get_json()

        if any(x not in data for x in required):
            return {"response": "fail", "reason": f"Expected keys: {str(required)}"}

        query = "INSERT INTO surveys "
        # cursor.execute(query)
        return {"response": "success"}


# 9. symptom progress report
@app.route("/symptoms/", methods=["GET"])
def sypmtoms():
    ensure_db()

    required = [
        "medicareNumber",
        "date",
    ]

    data = request.get_json()

    if any(x not in data for x in required):
        return {"response": "fail", "reason": f"Expected keys: {str(required)}"}

    query = (
        f"SELECT * FROM followUpForm "
        f"WHERE medicareNumber = \"{data['medicareNumber']}\" "
        f"AND date >= '{data['date']}' "
    )
    # cursor.execute(query)
    return {"response": "success"}


# 10. get messages within time period
@app.route("/messages/", methods=["GET"])
def messages():
    ensure_db()

    required = [
        "startDateTime",
        "endDateTime",
    ]

    data = request.get_json()

    if any(x not in data for x in required):
        return {"response": "fail", "reason": f"Expected keys: {str(required)}"}

    query = (
        f"SELECT * FROM message "
        f"WHERE dateTime > \"{data['startDateTime']}\" "
        f"AND dateTime < \"{data['endDateTime']}\" "
    )
    # cursor.execute(query)
    return {"response": "success"}


# 11. People at address
@app.route("/people-at-address/", methods=["GET"])
def people_at_address():
    ensure_db()

    required = [
        "address",
        "city",
        "province",
        "postalCode",
        "country",
    ]

    data = request.get_json()

    if any(x not in data for x in required):
        return {"response": "fail", "reason": f"Expected keys: {str(required)}"}

    query = ("SELECT * FROM person WHERE ") + " AND ".join(
        [f"{key}='{data[key]}'" for key in required]
    )
    print(query)

    cursor.execute(query)
    return jsonify(cursor.fetchall()) if cursor is not None else {"response": "failed", "reason": "query failed"}


# 12. get all facility details
@app.route("/facilities/", methods=["GET"])
def facilities():
    ensure_db()
    query = "SELECT * FROM publicHealthCenter"
    print(get_date())
    cursor.execute(query)
    return jsonify(cursor.fetchall()) if cursor is not None else {"response": "failed", "reason": "query failed"}


@app.route('/', methods=['GET'])
def home():
    return "hello world"


@app.route('/region/info', methods=['GET'])
def get_all_regions():
    return jsonify(get_regions())


@app.route('/region/report', methods=['GET'])
def get_region_reports():
    return jsonify(get_all_region_reports())


@app.route('/test_results_on_date', methods=['GET'])
def get_all_test_results_on_specific_date():
    data = request.get_json()
    return jsonify(get_test_result_on_date(data))


@app.route('/workers_at_facility', methods=['GET'])
def get_all_workers_at_facility():
    data = request.get_json()
    return jsonify(get_workers_at_facility(data))


@app.route('/workers_positive_test', methods=['GET'])
def get_workers_positive_at_facility():
    data = request.get_json()
    return jsonify(get_workers_positive_test_at_facility(data))


@app.route('/set_region_alert', methods=['POST'])
def set_alert_for_region():
    data = request.get_json()
    return jsonify(set_region_alert(data))


@app.route('/general/<table>/<action>', methods=['POST'])
def actions(table, action):
    data = request.get_json()
    return jsonify(perform_action(action, table, data))


def ensure_db():
    global cnx, cursor

    if cnx is None:
        load_dotenv()
        # load environment details from gitignored file
        config = dotenv_values("../env/backend.env")

    if cnx is None or not cnx.is_connected():
        cnx = connection.MySQLConnection(
            user=config["NAME"],
            password=config["PASSWORD"],
            host=config["HOST"],
            database=config["NAME"],
        )
        cursor = cnx.cursor(buffered=True, dictionary=True)


def on_starting(server):
    print("Starting up, connecting to DB")
    ensure_db()
    print("Connection to DB failed")


def on_exit(server):
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    ensure_db()
    app.run()
