from flask import Blueprint

from app.controllers.orders_controller import create_order, get_all_orders

bp = Blueprint('order_bp', __name__, url_prefix='order')

bp.post('')(create_order)
bp.get('')(get_all_orders)
