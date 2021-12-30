from flask import jsonify, request, current_app
from app.exceptions.exc import InvalidValueError, InvalidKeyError, RequiredKeyError
from app.models.user_model import UserModel
from flask_jwt_extended import create_access_token
import datetime
from werkzeug.exceptions import NotFound
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def create_user():
    data = request.get_json()
    try:
        UserModel.validate_key(data)
        UserModel.validate_value(data)
        UserModel.validate_required_key(data)

        user = UserModel(**data)

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return jsonify(user), HTTPStatus.CREATED
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except RequiredKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            constraint = str(err.args).split('_')[1]
            if constraint == 'username':    
                return jsonify({"message": "username already exists"}), HTTPStatus.CONFLICT
            if constraint == 'email':
                return jsonify({"message": "email already exists"}), HTTPStatus.CONFLICT


def get_all_user():
    users_list = UserModel.query.order_by(UserModel.user_id).all()
    return jsonify(users_list), HTTPStatus.OK


def get_user_by_id(user_id):
    try:
        user = UserModel.query.filter_by(user_id=user_id).first_or_404()
        return jsonify(user), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "user not found"}), HTTPStatus.NOT_FOUND


def update_user(user_id):
    data = request.get_json()

    if 'role' in data:
        return jsonify({"message": "Unauthorized to update role"}), 401

    try:
        user = UserModel.query.filter_by(user_id=user_id).first_or_404()

        for key, value in data.items():
            setattr(user, key, value)

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return jsonify(user), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "user not found"}), HTTPStatus.NOT_FOUND
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            constraint = str(err.args).split('_')[1]
            if constraint == 'username':    
                return jsonify({"message": "username already exists"}), HTTPStatus.CONFLICT
            if constraint == 'email':
                return jsonify({"message": "email already exists"}), HTTPStatus.CONFLICT


def delete_user(user_id):

    user = UserModel.query.filter_by(id=user_id).first_or_404()
    current_app.db.session.delete(user)
    current_app.db.session.commit()

    return jsonify(""), HTTPStatus.NO_CONTENT

# TODO: user/session criar uma função para visualizar o perfil do usuário que fez a requisição


def login():
    data = request.get_json()
    password = data.pop('password')
    try:
        user: UserModel = UserModel.query.filter_by(username=data['username']).first_or_404()

        if user.check_password(password):
            return jsonify({"token": create_access_token(user, fresh=datetime.timedelta(minutes=2))})
        else:
            return jsonify({"message": "password incorrect"}), HTTPStatus.UNAUTHORIZED
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND
