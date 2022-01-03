from flask import Blueprint
from .users_blueprints import bp as bp_user
from .customers_blueprint import bp as bp_customer
from .categories_blueprint import bp as bp_category
from .products_blueprint import bp as bp_product
from .orders_blueprint import bp as bp_order
from .cashback_blueprint import bp as bp_cashback

bp = Blueprint('api_bp', __name__, url_prefix='/api')

bp.register_blueprint(bp_user)
bp.register_blueprint(bp_customer)
bp.register_blueprint(bp_category)
bp.register_blueprint(bp_product)
bp.register_blueprint(bp_order)
bp.register_blueprint(bp_cashback)
