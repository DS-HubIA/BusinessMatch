from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import User, Business, Opportunity, Match

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        # 🔥 NOVO: Se não tem negócio cadastrado, vai para cadastro obrigatório
        if not current_user.has_business:
            return redirect(url_for('business.create_business'))
        return render_template('dashboard.html')  # CORRIGIDO: vai para dashboard
    return render_template('index.html')

@main_bp.route('/opportunities')
@login_required
def opportunities():
    """TELA PRINCIPAL - Sistema de swipe"""
    # 🔥 NOVO: Verificar se usuário tem negócio cadastrado
    if not current_user.has_business:
        return redirect(url_for('business.create_business'))
    return render_template('opportunities.html')

@main_bp.route('/profile')
@login_required 
def profile():
    """Perfil do usuário"""
    # 🔥 NOVO: Verificar se usuário tem negócio cadastrado
    if not current_user.has_business:
        return redirect(url_for('business.create_business'))
        
    user_businesses = Business.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', businesses=user_businesses)

@main_bp.route('/test-mobile')
def test_mobile():
    return render_template('test_mobile.html')
from flask import render_template

@main_bp.route('/debug-opportunities')
def debug_opportunities():
    return render_template('debug_opportunities.html')
from flask import render_template

@main_bp.route('/debug-opportunities')
