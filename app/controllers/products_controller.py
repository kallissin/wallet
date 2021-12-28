from flask import request, jsonify, current_app
from http import HTTPStatus
from app.models.category_model import CategoryModel
from app.models.product_model import ProductModel


def create_product():
    data = request.get_json()
    category = data.pop('category')

    category = CategoryModel.query.filter_by(name=category).first_or_404()

    data['category_id'] = category.id

    product = ProductModel(**data)

    current_app.db.session.add(product)
    current_app.db.session.commit()

    return jsonify(product), HTTPStatus.CREATED


def get_all_products():
    list_products = ProductModel.query.order_by(ProductModel.id).all()

    return jsonify(list_products)


def get_product_by_id(product_id):
    product = ProductModel.query.filter_by(id=product_id).first_or_404()

    return jsonify(product)
