from flask import request, jsonify, current_app
from flask_jwt_extended.view_decorators import jwt_required
from werkzeug.exceptions import NotFound
from app.exceptions.exc import InvalidKeyError, InvalidValueError, RequiredKeyError
from app.models.category_model import CategoryModel
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation, NotNullViolation
from app.utils.permission import permission_role


@permission_role(('admin',))
@jwt_required()
def create_category():
    data = request.get_json()
    try:
        CategoryModel.validate_key_and_value(data)
        CategoryModel.validate_required_key(data)

        category = CategoryModel(**data)

        current_app.db.session.add(category)
        current_app.db.session.commit()

        return jsonify(category), HTTPStatus.CREATED
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except RequiredKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            return jsonify({"message": "name already exists"}), HTTPStatus.CONFLICT


@jwt_required()
def get_all_categories():

    list_categories = CategoryModel.query.order_by(CategoryModel.category_id).all()

    return jsonify(list_categories), HTTPStatus.OK


@jwt_required()
def get_category_by_id(category_id):
    try:
        category = CategoryModel.query.filter_by(category_id=category_id).first_or_404()
        return jsonify(category), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "category not found"}), HTTPStatus.NOT_FOUND


@permission_role(('admin',))
@jwt_required()
def update_category(category_id):
    data = request.get_json()
    try:
        CategoryModel.validate_key_and_value(data)
        category = CategoryModel.query.filter_by(category_id=category_id).first_or_404()

        for key, value in data.items():
            setattr(category, key, value)

        current_app.db.session.add(category)
        current_app.db.session.commit()

        return jsonify(category), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "category not found"}), HTTPStatus.NOT_FOUND
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            return jsonify({"message": "name already exists"}), HTTPStatus.CONFLICT


@permission_role(('admin',))
@jwt_required()
def delete_category(category_id):
    try:
        category = CategoryModel.query.filter_by(category_id=category_id).first_or_404()
        current_app.db.session.delete(category)
        current_app.db.session.commit()
        return jsonify(""), HTTPStatus.NO_CONTENT
    except NotFound:
        return jsonify({"message": "category not found"}), HTTPStatus.NOT_FOUND
    except IntegrityError as err:
        if isinstance(err.orig, NotNullViolation):
            return jsonify({"message": "there are products registered with this category"}), HTTPStatus.CONFLICT
