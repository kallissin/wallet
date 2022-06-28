import os

DATABASE = {
    "host": os.environ.get("DATABASE_HOST"),
    "user": os.environ.get("DATABASE_USER"),
    "password": os.environ.get("DATABASE_PASSWORD"),
    "name": os.environ.get("DATABASE_NAME")
}


ENV = os.environ.get("FLASK_ENV")

if ENV == "development":
    SQLALCHEMY_URL = "postgresql://{user}:{password}@{host}:5432?sslmode=disable".format(
        user=DATABASE['user'],
        password=DATABASE['password'],
        host=DATABASE['host'],
    )
else:
    SQLALCHEMY_URL = "postgres://{user}:{password}@{host}:5432/{name}".format(
        user=DATABASE['user'],
        password=DATABASE['password'],
        host=DATABASE['host'],
        name=DATABASE['name']
    )
