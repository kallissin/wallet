from flask import Blueprint

from app.controllers.orders_controller import create_order

bp = Blueprint('order_bp', __name__, url_prefix='order')

bp.post('')(create_order)
