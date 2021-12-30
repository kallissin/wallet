from flask import request, jsonify, current_app
from app.exceptions.exc import InvalidKeyError, InvalidValueError, RequiredKeyError
from app.models.category_model import CategoryModel
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


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


def get_all_categories():

    list_categories = CategoryModel.query.order_by(CategoryModel.id).all()

    return jsonify(list_categories), HTTPStatus.OK


def get_category_by_id(category_id):
    category = CategoryModel.query.filter_by(id=category_id).first_or_404()

    return jsonify(category), HTTPStatus.OK


def update_category(category_id):
    data = request.get_json()

    category = CategoryModel.query.filter_by(id=category_id).first_or_404()

    for key, value in data.items():
        setattr(category, key, value)

    current_app.db.session.add(category)
    current_app.db.session.commit()

    return jsonify(category), HTTPStatus.OK


def delete_category(category_id):

    category = CategoryModel.query.filter_by(id=category_id).first_or_404()

    current_app.db.session.delete(category)
    current_app.db.session.commit()

    return jsonify(""), HTTPStatus.NO_CONTENT
