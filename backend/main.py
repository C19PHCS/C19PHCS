from flask import Flask, request, jsonify
from general_functions import perform_action


def main():
    app = Flask(__name__)
    app.config["DEBUG"] = True


    @app.route('/', methods=['GET'])
    def home():
        return "hello world"

    @app.route('/<table>/<action>', methods=['POST'])
    def actions(table, action):
        data = request.get_json()
        return jsonify(perform_action(action, table, data))

    return app

app = main()

if __name__ == "__main__":
    app.run()
