from mysql.connector import connection, cursor
from config import config

def get_conn():
    database_config = config["database"]
    conn = connection.MySQLConnection(user=database_config["username"], password=database_config["password"],
                                        host=database_config["host"],
                                        database=database_config["name"])
    return conn