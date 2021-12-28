from flask import Blueprint
from .users_blueprints import bp as bp_user
from .customers_blueprint import bp as bp_customer


bp = Blueprint('api_bp', __name__, url_prefix='/api')

bp.register_blueprint(bp_user)
bp.register_blueprint(bp_customer)
