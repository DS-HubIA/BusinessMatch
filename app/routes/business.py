from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Business, Opportunity, Interest, Match, User
from app.security import limiter, sanitize_input, validate_cnpj, API_LIMITS, BUSINESS_LIMITS
from datetime import datetime

business_bp = Blueprint('business', __name__, url_prefix='/business')

@business_bp.route('/api/opportunities')
@login_required
def api_opportunities():
    """API para listar oportunidades (exclui admins automaticamente)"""
    try:
        # Oportunidades já vistas pelo usuário
        seen_opportunities = db.session.query(Interest.opportunity_id).filter(
            Interest.user_id == current_user.id
        ).subquery()

        # ✅ FILTRO CRÍTICO: Excluir oportunidades de usuários admin
        opportunities = Opportunity.query.filter(
            ~Opportunity.id.in_(seen_opportunities),
            ~Opportunity.user_id.in_(
                db.session.query(User.id).filter(User.is_admin == True)
            )
        ).all()

        if opportunities:
            opportunity_list = []
            for opp in opportunities:
                business = Business.query.get(opp.business_id)
                if business:
                    opportunity_data = {
                        'id': opp.id,
                        'title': sanitize_input(opp.title),
                        'description': sanitize_input(opp.description),
                        'type': opp.type,
                        'business_name': sanitize_input(business.name),
                        'business_description': sanitize_input(business.description),
                        'business_cnpj': business.cnpj,
                        'business_phone': business.phone,
                        'business_email': business.email,
                        'user_id': opp.user_id
                    }
                    opportunity_list.append(opportunity_data)
            
            return jsonify(opportunity_list)
        else:
            return jsonify([])

    except Exception as e:
        print(f"Erro API oportunidades: {e}")
        return jsonify([]), 500

# Manter o resto do código igual...
def matches():

@business_bp.route('/matches')
@login_required
def matches():
    if not current_user.has_business:
        return redirect(url_for('business.create_business'))
        
    try:
        user_matches = Match.query.filter(
            (Match.user1_id == current_user.id) | (Match.user2_id == current_user.id)
        ).all()
        
        matches_data = []
        for match in user_matches:
            other_user_id = match.user2_id if match.user1_id == current_user.id else match.user1_id
            other_user = User.query.get(other_user_id)
            opportunity = Opportunity.query.get(match.opportunity_id)
            business = Business.query.get(opportunity.business_id) if opportunity else None
            
            matches_data.append({
                'match_id': match.id,
                'other_user_name': sanitize_input(other_user.name) if other_user else 'Usuário',
                'other_user_phone': other_user.phone if other_user else '',
                'other_user_email': other_user.email if other_user else '',
                'opportunity_title': sanitize_input(opportunity.title) if opportunity else 'Oportunidade',
                'business_name': sanitize_input(business.name) if business else 'Negócio',
                'match_date': match.created_at.strftime('%d/%m/%Y') if match.created_at else 'Data não disponível'
            })
        
        return render_template('matches.html', matches=matches_data)
        
    except Exception as e:
        print(f"Erro ao carregar matches: {e}")
        flash('Erro ao carregar matches.', 'danger')
        return render_template('matches.html', matches=[])
