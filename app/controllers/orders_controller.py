from flask import request, jsonify, current_app
from http import HTTPStatus
from app.models.order_model import OrderModel
from app.models.customer_model import CustomerModel


def create_order():
    data = request.get_json()

    customer = CustomerModel.query.filter_by(cpf=data['cpf']).first_or_404()
    order = OrderModel(customer_id=customer.id)

    current_app.db.session.add(order)
    current_app.db.session.commit()

    return jsonify(order), HTTPStatus.CREATED


def get_all_orders():
    list_orders = OrderModel.query.order_by(OrderModel.id).all()

    return jsonify(list_orders)


def get_order_by_id(order_id):
    order = OrderModel.query.filter_by(id=order_id).first_or_404()

    return jsonify(order)
