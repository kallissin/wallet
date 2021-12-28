from flask import request, jsonify, current_app
from app.models.category_model import CategoryModel
from http import HTTPStatus


def create_category():
    data = request.get_json()

    category = CategoryModel(**data)

    current_app.db.session.add(category)
    current_app.db.session.commit()

    return jsonify(category), HTTPStatus.CREATED


def get_all_categories():

    list_categories = CategoryModel.query.order_by(CategoryModel.id).all()

    return jsonify(list_categories)
