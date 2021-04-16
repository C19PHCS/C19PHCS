from flask import Flask
from mysql.connector import connection, cursor
from config import config

class Person():
    def __init__(self, data):
        self.medicare_number = data[0]

def main():
    database_config = config["database"]
    cnx = connection.MySQLConnection(user=database_config["username"], password=database_config["password"],
                                     host=database_config["host"],
                                     database=database_config["name"])
    cursor = cnx.cursor()
    query = ("SELECT * FROM test")
    cursor.execute(query)

    for data in cursor:
        print(data)

    cursor.close()
    cnx.close()

    app = Flask(__name__)
    app.config["DEBUG"] = True


    @app.route('/', methods=['GET'])
    def home():
        return "asdfasdfasdfasdf"

    return app

app = main()

if __name__ == "__main__":
    app.run()
