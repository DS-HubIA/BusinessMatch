from flask import Blueprint

bp = Blueprint('auth', __name__)

@bp.route('/login')
def login():
    return "Página de Login - Em construção"

@bp.route('/register')
def register():
    return "Página de Cadastro - Em construção"
