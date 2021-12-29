from flask import jsonify, request, current_app
from app.exceptions.exc import InvalidValueError, InvalidKeyError, RequiredKeyError
from app.models.user_model import UserModel
from flask_jwt_extended import create_access_token
import datetime
from werkzeug.exceptions import NotFound
from http import HTTPStatus


def create_user():
    data = request.get_json()
    try:
        UserModel.validate_data(data)
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


def get_all_user():
    users_list = UserModel.query.order_by(UserModel.user_id).all()
    return jsonify(users_list), HTTPStatus.OK


def get_user_by_id(user_id):
    user = UserModel.query.filter_by(id=user_id).first_or_404()
    return jsonify(user), HTTPStatus.OK


def update_user(user_id):
    data = request.get_json()

    if 'role' in data:
        return jsonify({"message": "Unauthorized to update role"}), 401

    user = UserModel.query.filter_by(id=user_id).first_or_404()

    for key, value in data.items():
        setattr(user, key, value)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify(user), HTTPStatus.OK


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
