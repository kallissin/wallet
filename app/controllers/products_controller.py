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
