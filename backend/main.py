from flask import Flask, request, jsonify
from mysql.connector import connection, cursor
from flask_cors import CORS


from config import config
from general_functions import *
from database import conn

database_config = config["database"]

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def home():
    return "hello world"


@app.route('/general/<table>/<action>', methods=['GET', 'POST'])
def actions(table, action):
    return perform_action(action, table, request.get_json())


# 8 and 9. store or get survey
@app.route("/survey/<string:action>/", methods=["POST"])
def survey(action):
    conn.connect()
    if action == "store":
        required = [
            "medicare",
            "dateOfBirth",
            "time",
            "temperature",
            "symptoms",
        ]

        data = request.get_json()

        if any(x not in data for x in required):
            return {"response": "fail", "reason": f"Expected keys: {str(required)}"}

        query = "SELECT * FROM "
        conn.cursor.execute(query)
        return jsonify(conn.cursor.fetchall()) if conn.cursor is not None else {"response": "failed", "reason": "query failed"}
    elif action == "get":
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
            f"AND date > '{data['date']}' "
        )

        conn.cursor.execute(query)
        return jsonify(conn.cursor.fetchall()) if conn.cursor is not None else {"response": "failed", "reason": "query failed"}


# 10. get messages within time period
@app.route("/messages/", methods=["GET"])
def messages():
    conn.connect()

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
    # conn.cursor.execute(query)
    return {"response": "success"}


# 11. People at address
@app.route("/people-at-address/", methods=["GET"])
def people_at_address():
    conn.connect()

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

    conn.cursor.execute(query)
    return jsonify(conn.cursor.fetchall()) if conn.cursor is not None else {"response": "failed", "reason": "query failed"}


# 12. get all facility details
@app.route("/facilities/", methods=["GET"])
def facilities():
    conn.connect()
    query = "SELECT * FROM publicHealthCenter"
    conn.cursor.execute(query)
    increment_date()
    return jsonify(conn.cursor.fetchall()) if conn.cursor is not None else {"response": "failed", "reason": "query failed"}


@app.route('/region/info', methods=['GET'])
def get_all_regions():
    return jsonify(get_regions())


@app.route('/region/report', methods=['GET'])
def get_region_reports():
    return jsonify(get_all_region_reports())


@app.route('/test-results-on-date', methods=['GET'])
def get_all_test_results_on_specific_date():
    data = request.get_json()
    return jsonify(get_test_result_on_date(data))


@app.route('/workers-at-facility', methods=['GET'])
def get_all_workers_at_facility():
    data = request.get_json()
    return jsonify(get_workers_at_facility(data))


@app.route('/workers-positive-test', methods=['GET'])
def get_workers_positive_at_facility():
    data = request.get_json()
    return jsonify(get_workers_positive_test_at_facility(data))


@app.route('/set-region-alert', methods=['POST'])
def set_alert_for_region():
    data = request.get_json()
    return jsonify(set_region_alert(data))


def on_starting(server):
    print("Starting up, connecting to DB")
    conn.connect()
    print("Connection to DB failed")


def on_exit(server):
    conn.cursor.close()
    conn.cnx.close()


if __name__ == "__main__":
    conn.connect()
    app.run()
