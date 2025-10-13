from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('business.opportunities'))
    return render_template('index.html', user=current_user)

@bp.route('/dashboard')
@login_required
def dashboard():
    return "Dashboard - Em construção"
