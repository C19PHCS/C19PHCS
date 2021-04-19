from dotenv import load_dotenv, dotenv_values
from mysql.connector import connection, cursor
from config import config

class connClass:
    cnx = None
    cursor = None
    config = None

    def __init__(self):
        self.connect()

    def connected(self):
        ret = True
        if self.cnx is None or self.config is None:
            load_dotenv()
            self.config = dotenv_values("../env/backend.env")
            ret = False
        elif not self.cnx.is_connected():
            ret = False

        return ret


    def connect(self):
        if not self.connected():
            try:
                self.cnx = connection.MySQLConnection(
                    user=self.config["NAME"],
                    password=self.config["PASSWORD"],
                    host=self.config["HOST"],
                    database=self.config["NAME"],
                )
            except Exception as e:
                print(e)
                return False

            self.cursor = self.cnx.cursor(buffered=True, dictionary=True)
        return True

conn = connClass()

# def get_conn():
#     database_config = config["database"]
#     conn = connection.MySQLConnection(user=database_config["username"], password=database_config["password"],
#                                         host=database_config["host"],
#                                         database=database_config["name"])
#     return conn
