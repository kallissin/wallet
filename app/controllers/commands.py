import click
from flask.cli import AppGroup
from flask import Flask, current_app
from app.models.user_model import UserModel
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def commands(app: Flask):
    cli = AppGroup('admin')

    @cli.command('create')
    @click.argument('name')
    @click.argument('email')
    @click.argument('username')
    @click.argument('password')
    def create(name, email, username, password):
        data = {
            'name': name,
            'email': email,
            'username': username,
            'password': password
        }

        try:
            UserModel.validate_key_and_value(data)
            UserModel.validate_required_key(data)

            user = UserModel(**data)
            user.role = 'admin'
            current_app.db.session.add(user)
            current_app.db.session.commit()

            return print("user created with successfull")
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                constraint = str(err.args).split('_')[1]
                if constraint == 'username':
                    return print("username already exists")
                if constraint == 'email':
                    return print("email already exists")
    app.cli.add_command(cli)


def init_app(app: Flask):
    commands(app)
