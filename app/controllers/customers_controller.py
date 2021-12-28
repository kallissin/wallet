from flask import request, jsonify, current_app
from app.models.customer_model import CustomerModel
from http import HTTPStatus


def create_customer():
    data = request.get_json()

    customer = CustomerModel(**data)

    current_app.db.session.add(customer)
    current_app.db.session.commit()

    return jsonify(customer), HTTPStatus.CREATED


def get_all_customer():
    customers_list = CustomerModel.query.order_by(CustomerModel.id).all()

    return jsonify(customers_list), HTTPStatus.OK
