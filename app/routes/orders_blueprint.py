from flask import Blueprint

from app.controllers.orders_controller import create_order, delete_item, delete_order, get_all_orders, get_item_by_order_id, get_order_by_id, insert_item

bp = Blueprint('order_bp', __name__, url_prefix='order')

bp.post('')(create_order)
bp.get('')(get_all_orders)
bp.get('/<int:order_id>')(get_order_by_id)
bp.post('/<int:order_id>/item')(insert_item)
bp.get('/<int:order_id>/item')(get_item_by_order_id)
bp.delete('/<int:order_id>')(delete_order)
bp.delete('/item/<int:item_id>')(delete_item)
