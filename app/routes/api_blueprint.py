from flask import Blueprint
from .users_blueprints import bp as bp_user


bp = Blueprint('api_bp', __name__, url_prefix='/api')

bp.register_blueprint(bp_user)
