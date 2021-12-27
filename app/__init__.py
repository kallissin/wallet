from flask import Flask
from app.configs import env_configs, database


def create_app():
    app = Flask(__name__)
    env_configs.init_app(app)
    database.init_app(app)

    return app
