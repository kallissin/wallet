from flask import Blueprint

from app.controllers.products_controller import create_product, get_all_products

bp = Blueprint('product', __name__, url_prefix='/product')

bp.post('')(create_product)
bp.get('')(get_all_products)
