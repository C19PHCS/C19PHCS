from flask import Flask, request, jsonify
from general_functions import *


def main():
    app = Flask(__name__)
    app.config["DEBUG"] = True


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

    return app

app = main()

if __name__ == "__main__":
    app.run()
