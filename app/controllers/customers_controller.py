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


def get_customer_by_id(customer_id):
    customer = CustomerModel.query.filter_by(id=customer_id).first_or_404()

    return jsonify(customer), HTTPStatus.OK


def update_customer(customer_id):
    data = request.get_json()

    customer = CustomerModel.query.filter_by(id=customer_id).first_or_404()

    for key, value in data.items():
        setattr(customer, key, value)

    current_app.db.session.add(customer)
    current_app.db.session.commit()

    return jsonify(customer), HTTPStatus.OK
