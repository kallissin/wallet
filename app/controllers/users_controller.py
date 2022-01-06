from flask import jsonify, request, current_app
from app.exceptions.exc import InvalidValueError, InvalidKeyError, RequiredKeyError
from app.models.user_model import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
from werkzeug.exceptions import NotFound
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from app.utils.permission import permission_role


def create_user():
    data = request.get_json()
    try:
        UserModel.validate_key_and_value(data)
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


@permission_role(('admin',))
@jwt_required()
def get_all_user():
    users_list = UserModel.query.order_by(UserModel.user_id).all()
    return jsonify(users_list), HTTPStatus.OK


@permission_role(('admin',))
@jwt_required()
def get_user_by_id(user_id):
    try:
        user = UserModel.query.filter_by(user_id=user_id).first_or_404()
        return jsonify(user), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "user not found"}), HTTPStatus.NOT_FOUND


# TODO: criar validação para atualizar os dados somente se for o mesmo id ou admin
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user = get_jwt_identity()

    if user['user_id'] != user_id:
        if user['role'] != 'admin':
            return jsonify({"message": "Unauthorized to update user"}), HTTPStatus.FORBIDDEN

    if 'role' in data:
        return jsonify({"message": "Unauthorized to update role"}), 403

    try:
        UserModel.validate_key_and_value(data)

        user = UserModel.query.filter_by(user_id=user_id).first_or_404()

        for key, value in data.items():
            setattr(user, key, value)

        current_app.db.session.add(user)
        current_app.db.session.commit()

        return jsonify(user), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "user not found"}), HTTPStatus.NOT_FOUND
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            constraint = str(err.args).split('_')[1]
            if constraint == 'username':    
                return jsonify({"message": "username already exists"}), HTTPStatus.CONFLICT
            if constraint == 'email':
                return jsonify({"message": "email already exists"}), HTTPStatus.CONFLICT


@permission_role(('admin',))
@jwt_required()
def delete_user(user_id):
    try:
        user = UserModel.query.filter_by(user_id=user_id).first_or_404()
        current_app.db.session.delete(user)
        current_app.db.session.commit()

        return jsonify(""), HTTPStatus.NO_CONTENT
    except NotFound:
        return jsonify({"message": "user not found"}), HTTPStatus.NOT_FOUND
# TODO: user/session criar uma função para visualizar o perfil do usuário que fez a requisição


def login():
    data = request.get_json()
    try:
        UserModel.validate_key_and_value(data)
        UserModel.validate_login(data)
        password = data.pop('password')

        user: UserModel = UserModel.query.filter_by(username=data['username']).first_or_404()

        if user.check_password(password):
            return jsonify({"token": create_access_token(user, fresh=datetime.timedelta(minutes=2))})
        else:
            return jsonify({"message": "password incorrect"}), HTTPStatus.UNAUTHORIZED
    except NotFound:
        return {"message": "user not found"}, HTTPStatus.NOT_FOUND
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except RequiredKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
