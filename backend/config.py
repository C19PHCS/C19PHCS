import os

default = {
    "database": {
        "name": os.getenv("DATABASE_NAME", "comp353"),
        "username": os.getenv("DATABASE_USERNAME", "admin"),
        "password": os.getenv("DATABASE_PASSWORD", "admin"),
        "host": os.getenv("DATABASE_HOST", "mysqldb"),
        "port": int(os.getenv("DATABASE_PORT", "3306")),
    }
}

config = default
