from flask import Blueprint

from app.controllers.products_controller import create_product

bp = Blueprint('product', __name__, url_prefix='/product')

bp.post('')(create_product)
