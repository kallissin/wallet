from flask import request, jsonify, current_app
from http import HTTPStatus
from werkzeug.exceptions import NotFound
from app.exceptions.exc import InvalidKeyError, InvalidValueError, RequiredKeyError
from app.models.order_model import OrderModel
from app.models.customer_model import CustomerModel
from app.models.order_product_model import OrderProductModel
from app.models.product_model import ProductModel
import requests


def calculate_total_amount(order):
    value_per_item = 0
    for item in order.itens:
        value_per_item += item.value * item.qty
    setattr(order, 'total', value_per_item)
    return order


def create_order():
    data = request.get_json()
    try:
        OrderModel.validate_key_and_value(data)
        OrderModel.validate_required_key(data)
        customer = CustomerModel.query.filter_by(cpf=data['cpf']).first_or_404()
        order = OrderModel(customer_id=customer.customer_id)

        current_app.db.session.add(order)
        current_app.db.session.commit()

        return jsonify(order), HTTPStatus.CREATED
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except RequiredKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except NotFound:
        return jsonify({"message": "customer not found"}), HTTPStatus.NOT_FOUND


def get_all_orders():
    list_orders = OrderModel.query.order_by(OrderModel.order_id).all()
    return jsonify([{
        "order_id": order.order_id,
        "sold_at": order.sold_at,
        "customer": order.customer,
        "total": order.total,
        "itens": [{
            "register_id": item.register_id,
            "product": item.product.name,
            "value": item.value,
            "qty": item.qty
        } for item in order.itens],
        "cashback_id": order.cashback_id
    } for order in list_orders])


def get_order_by_id(order_id):
    try:
        order = OrderModel.query.filter_by(order_id=order_id).first_or_404()
        return jsonify({
            "order_id": order.order_id,
            "sold_at": order.sold_at,
            "customer": order.customer,
            "total": order.total,
            "itens": [{
                "register_id": item.register_id,
                "product": item.product.name,
                "value": item.value,
                "qty": item.qty
            } for item in order.itens],
            "cashback_id": order.cashback_id})
    except NotFound:
        return jsonify({"message": "order not found"}), HTTPStatus.NOT_FOUND


def insert_item(order_id):
    data = request.get_json()

    try:
        OrderProductModel.validate_key_and_value(data)
        OrderProductModel.validate_required_key(data)
        product_name = data.pop('name')
        product = ProductModel.query.filter_by(name=product_name).first_or_404()
        item = OrderProductModel(product=product, **data)
    except NotFound:
        return jsonify({"message": "product not found"}), HTTPStatus.NOT_FOUND
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except RequiredKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    order = OrderModel.query.filter_by(order_id=order_id).first_or_404()
    existing_item = False

    for item_order in order.itens:
        if product_name == item_order.product.name:
            existing_item = True

    if existing_item:
        return jsonify({"message": "Item already exists"}), HTTPStatus.CONFLICT

    order.itens.append(item)
    order = calculate_total_amount(order)
    current_app.db.session.add(order)
    current_app.db.session.commit()

    return jsonify([{
        "item_id": item.register_id,
        "product": {
            "product_id": item.product.product_id,
            "name": item.product.name,
            "category": item.product.category.name
        },
        "value": item.value,
        "qty": item.qty
    } for item in order.itens]), HTTPStatus.CREATED


def get_item_by_id(item_id):
    try:
        item = OrderProductModel.query.filter_by(register_id=item_id).first_or_404()
        return jsonify({
            "item_id": item.register_id,
            "product": {
                "product_id": item.product.product_id,
                "name": item.product.name,
                "category": {
                    "category_id": item.product.category.category_id,
                    "name": item.product.category.name
                }
            },
            "value": item.value,
            "qty": item.qty
        }), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "item not found"}), HTTPStatus.NOT_FOUND


def get_all_itens():
    list_itens = OrderProductModel.query.order_by(OrderProductModel.register_id).all()
    return jsonify([{
        "item_id": item.register_id,
        "product": {
            "product_id": item.product.product_id,
            "name": item.product.name,
            "category": item.product.category.name
        },
        "value": item.value,
        "qty": item.qty
    } for item in list_itens]), HTTPStatus.OK


def get_item_by_order_id(order_id):
    try:
        order = OrderModel.query.filter_by(order_id=order_id).first_or_404()
        return jsonify([{
            "item_id": item.register_id,
            "product": {
                "product_id": item.product.product_id,
                "name": item.product.name,
                "category": item.product.category.name
            },
            "value": item.value,
            "qty": item.qty
        } for item in order.itens])
    except NotFound:
        return jsonify({"message": "order not found"}), HTTPStatus.NOT_FOUND


def delete_order(order_id):
    try:
        order = OrderModel.query.filter_by(order_id=order_id).first_or_404()
        if order.cashback_id:
            requests.delete(f"https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback/{order.cashback_id}")
        current_app.db.session.delete(order)
        current_app.db.session.commit()
        return jsonify(""), HTTPStatus.NO_CONTENT
    except NotFound:
        return jsonify({"message": "order not found"}), HTTPStatus.NOT_FOUND


def delete_item(item_id):
    try:
        item = OrderProductModel.query.filter_by(register_id=item_id).first_or_404()
        order = OrderModel.query.filter_by(order_id=item.order_id).first_or_404()
        current_app.db.session.delete(item)
        current_app.db.session.commit()
        order = calculate_total_amount(order)
        current_app.db.session.add(order)
        current_app.db.session.commit()
        return jsonify(""), HTTPStatus.NO_CONTENT
    except NotFound:
        return jsonify({"message": "item not found"}), HTTPStatus.NOT_FOUND


# TODO: implementar a função com as exceções
def update_item(item_id):
    data = request.get_json()

    try:
        item = OrderProductModel.query.filter_by(register_id=item_id).first_or_404()
    except NotFound:
        return jsonify({"message": "item not found"}), HTTPStatus.NOT_FOUND

    try:
        OrderProductModel.validate_key_and_value(data)
        OrderProductModel.validate_required_key(data)
        product_name = data.pop('name')
        product = ProductModel.query.filter_by(name=product_name).first_or_404()
        setattr(item, 'product', product)
        for key, value in data.items():
            setattr(item, key, value)
        order = OrderModel.query.filter_by(order_id=item.order_id).first_or_404()
        order = calculate_total_amount(order)
        current_app.db.session.add(order)
        current_app.db.session.commit()
        return jsonify({
            "item_id": item.register_id,
            "product": {
                "product_id": item.product.product_id,
                "name": item.product.name,
                "category": {
                    "category_id": item.product.category.category_id,
                    "name": item.product.category.name
                }
            },
            "value": item.value,
            "qty": item.qty
        }), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "product not found"}), HTTPStatus.NOT_FOUND
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except RequiredKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
