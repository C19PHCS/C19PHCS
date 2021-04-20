from flask import Flask, request, jsonify
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

# 1-7. create/edit/delete
app.route('/general/<table>/<action>/', methods=['GET', 'POST'])(perform_action)

# 8 and 9. store or get survey
app.route("/survey/<string:action>/", methods=["POST"])(survey)

# 10. get messages within time period
app.route("/messages/", methods=["GET"])(messages)

# 11. People at address
app.route("/people-at-address/", methods=["GET"])(people_at_address)

# 12. get all facility details
app.route("/facilities/", methods=["GET"])(facilities)

# 13. list of all regions
app.route('/region/info/', methods=['GET'])(get_all_regions)

# 14. list of people who got the result of the test on a specific date
app.route('/test-results-on-date/', methods=['POST'])(get_all_test_results_on_specific_date)

# 15- list of workers in specific facility
app.route('/workers-at-facility/<int:facilityID>/', methods=['GET'])(get_all_workers_at_facility)

# 16. all positive workers at a facility
app.route('/workers-positive-test/', methods=['POST'])(get_workers_positive_at_facility)

# 17. report for each region
app.route('/region/report/', methods=['GET'])(get_region_reports)

# set alert for a given region
app.route('/set-region-alert/', methods=['POST'])(set_alert_for_region)

# Get current date
app.route('/get_date/', methods=['GET'])(get_date)
    
# Increment date in db
app.route('/increment_date/', methods=['GET'])(increment_date)


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
