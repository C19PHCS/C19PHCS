from mysql.connector import connection, cursor
from os import getenv
from dotenv import load_dotenv, dotenv_values

import flask


class Person():
    def __init__(self, data):
        self.medicare_number = data[0]

def main():
    load_dotenv()
    config = dotenv_values(".env")
    cnx = connection.MySQLConnection(user=config["NAME"], password=config["PASSWORD"],
                                     host=config["HOST"],
                                     database=config["NAME"])
    cursor = cnx.cursor()
    query = ("SELECT * FROM person")
    cursor.execute(query)

    for data in cursor:
        person = Person(data)
        print(person.medicare_number)

    cursor.close()
    cnx.close()

    app = flask.Flask(__name__)
    app.config["DEBUG"] = True


    @app.route('/', methods=['GET'])
    def home():
        return "asdfasdfasdfasdf"

    app.run()

if __name__ == "__main__":
    main()
