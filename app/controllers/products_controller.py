from flask import request, jsonify, current_app
from http import HTTPStatus
from app.exceptions.exc import InvalidKeyError, InvalidValueError, RequiredKeyError
from app.models.category_model import CategoryModel
from app.models.product_model import ProductModel
from werkzeug.exceptions import NotFound
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from flask_jwt_extended import jwt_required


@jwt_required()
def create_product():
    try:
        data = request.get_json()

        ProductModel.validate_key_and_value(data)
        ProductModel.validate_required_key(data)

        category = data.pop('category')
        category = CategoryModel.query.filter_by(name=category).first_or_404()

        data['category_id'] = category.category_id

        product = ProductModel(**data)

        current_app.db.session.add(product)
        current_app.db.session.commit()

        return jsonify(product), HTTPStatus.CREATED
    except NotFound:
        return jsonify({"message": "category not found"}), HTTPStatus.NOT_FOUND
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
def get_all_products():
    list_products = ProductModel.query.order_by(ProductModel.product_id).all()
    return jsonify(list_products), HTTPStatus.OK


@jwt_required()
def get_product_by_id(product_id):
    try:
        product = ProductModel.query.filter_by(product_id=product_id).first_or_404()
        return jsonify(product), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "product not found"}), HTTPStatus.NOT_FOUND


@jwt_required()
def update_product(product_id):
    data = request.get_json()

    try:
        ProductModel.validate_key_and_value(data)
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST

    if 'category' in data:
        try:
            category = data.pop('category').lower()
            category = CategoryModel.query.filter_by(name=category).first_or_404()
            data['category_id'] = category.category_id
        except NotFound:
            return jsonify({"message": "category not found"}), HTTPStatus.NOT_FOUND

    try:
        product = ProductModel.query.filter_by(product_id=product_id).first_or_404()

        for key, value in data.items():
            setattr(product, key, value)

        current_app.db.session.add(product)
        current_app.db.session.commit()

        return jsonify(product), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "product not found"}), HTTPStatus.NOT_FOUND
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            return jsonify({"message": "name already exists"}), HTTPStatus.CONFLICT


@jwt_required()
def delete_product(product_id):
    try:
        product = ProductModel.query.filter_by(product_id=product_id).first_or_404()

        current_app.db.session.delete(product)
        current_app.db.session.commit()

        return jsonify(""), HTTPStatus.NO_CONTENT
    except NotFound:
        return jsonify({"message": "product not found"}), HTTPStatus.NOT_FOUND
