from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Business, Match

bp = Blueprint('business', __name__)

@bp.route('/opportunities')
@login_required
def opportunities():
    # Buscar oportunidades que não são do usuário atual
    opportunities = Business.query.filter(
        Business.user_id != current_user.id,
        Business.is_active == True
    ).all()
    return render_template('opportunities.html', opportunities=opportunities)

@bp.route('/api/opportunities')
@login_required
def api_opportunities():
    opportunities = Business.query.filter(
        Business.user_id != current_user.id,
        Business.is_active == True
    ).all()
    
    result = []
    for opp in opportunities:
        result.append({
            'id': opp.id,
            'title': opp.title,
            'description': opp.description,
            'type': opp.business_type,
            'category': opp.category
        })
    
    return jsonify(result)

@bp.route('/swipe/<int:business_id>/<action>')
@login_required
def swipe(business_id, action):
    business = Business.query.get_or_404(business_id)
    
    if action == 'like':
        # Criar match
        match = Match(user_id=current_user.id, business_id=business_id)
        db.session.add(match)
        db.session.commit()
        
        return jsonify({
            'status': 'success', 
            'message': 'Match realizado!',
            'match': True
        })
    
    elif action == 'dislike':
        return jsonify({
            'status': 'success',
            'message': 'Oportunidade descartada', 
            'match': False
        })
    
    return jsonify({'status': 'error', 'message': 'Ação inválida'})

@bp.route('/matches')
@login_required
def matches():
    user_matches = Match.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).join(Business).all()
    return render_template('matches.html', matches=user_matches)
