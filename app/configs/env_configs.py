from flask import Flask
from environs import Env
from os import getenv

env = Env()
env.read_env()


def init_app(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = bool(getenv("SQLALCHEMY_TRACK_MODIFICATIONS"))
    app.config['JSON_SORT_KEYS'] = bool(getenv("JSON_SORT_KEYS"))
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY')
