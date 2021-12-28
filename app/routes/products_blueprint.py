from flask import Blueprint

from app.controllers.products_controller import create_product, delete_product, get_all_products, get_product_by_id, update_product

bp = Blueprint('product', __name__, url_prefix='/product')

bp.post('')(create_product)
bp.get('')(get_all_products)
bp.get('<int:product_id>')(get_product_by_id)
bp.patch('<int:product_id>')(update_product)
bp.delete('<int:product_id>')(delete_product)
