from flask import Blueprint

from app.controllers.orders_controller import create_order, get_all_orders, get_order_by_id

bp = Blueprint('order_bp', __name__, url_prefix='order')

bp.post('')(create_order)
bp.get('')(get_all_orders)
bp.get('/<int:order_id>')(get_order_by_id)
