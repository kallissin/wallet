from flask import Flask
from app.configs import env_configs, database, migration, auth
from app import routes
from app.controllers import commands


def create_app():
    app = Flask(__name__)
    env_configs.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    auth.init_app(app)
    routes.init_app(app)
    commands.init_app(app)
    return app
