from flask import Blueprint

bp = Blueprint('business', __name__)

@bp.route('/opportunities')
def opportunities():
    return "Oportunidades - Em construção"
