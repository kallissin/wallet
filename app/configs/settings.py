import os

DATABASE = {
    "host": os.environ.get("DATABASE_HOST"),
    "user": os.environ.get("DATABASE_USER"),
    "password": os.environ.get("DATABASE_PASSWORD"),
    "name": os.environ.get("DATABASE_NAME")
}


SQLALCHEMY_URL = "mysql+pymysql://{user}:{password}@{host}/{name}".format(
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    name=DATABASE['name'],
)
