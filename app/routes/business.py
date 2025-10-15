from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Business, Opportunity, Match, Interest
from app.security import limiter, sanitize_input, validate_cnpj, API_LIMITS, BUSINESS_LIMITS
import unicodedata
import re

business_bp = Blueprint('business', __name__)

def normalize_text(text):
    """Normaliza texto: remove acentos, converte para minúsculas"""
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    return text.lower().strip()

def format_cnpj(cnpj):
    """Formata CNPJ para o padrão 00.000.000/0000-00"""
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    if len(cnpj) == 14:
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return cnpj

@business_bp.route('/business/create', methods=['GET', 'POST'])
@login_required
@limiter.limit(BUSINESS_LIMITS)  # 🔥 CORREÇÃO: String
def create_business():
    existing_business = Business.query.filter_by(user_id=current_user.id).first()
    
    if existing_business:
        flash('Você já tem um negócio cadastrado. Use a opção "Editar Negócio".', 'info')
        return redirect(url_for('business.edit_business'))
        
    if request.method == 'POST':
        try:
            # Sanitizar todos os inputs
            name = sanitize_input(request.form.get('name'))
            description = sanitize_input(request.form.get('description'))
            cnpj = sanitize_input(request.form.get('cnpj'))
            
            # Validar CNPJ
            if not validate_cnpj(cnpj):
                flash('CNPJ inválido!', 'danger')
                return render_template('create_business.html')
            
            # Formatar CNPJ
            cnpj_formatted = format_cnpj(cnpj)
            
            # Verificar se CNPJ já está cadastrado
            existing_cnpj = Business.query.filter_by(cnpj=cnpj_formatted).first()
            if existing_cnpj:
                flash('Este CNPJ já está cadastrado no sistema.', 'danger')
                return render_template('create_business.html')
            
            # Sanitizar demais campos
            business_sector = sanitize_input(request.form.get('business_sector'))
            business_category = sanitize_input(request.form.get('business_category'))
            city = sanitize_input(request.form.get('city'))
            state = sanitize_input(request.form.get('state'))
            sells_products = sanitize_input(request.form.get('sells_products'))
            sells_services = sanitize_input(request.form.get('sells_services'))
            buys_products = sanitize_input(request.form.get('buys_products'))
            buys_services = sanitize_input(request.form.get('buys_services'))
            
            location = f"{city}, {state}"
            tags = normalize_text(sanitize_input(request.form.get('tags', '')))
            
            # Criar negócio
            business = Business(
                name=name,
                entrepreneur_name=current_user.name,
                cnpj=cnpj_formatted,
                description=description,
                business_sector=business_sector,
                business_category=business_category,
                sells_products=sells_products,
                sells_services=sells_services,
                buys_products=buys_products,
                buys_services=buys_services,
                tags=tags,
                location=location,
                city=city,
                state=state,
                user_id=current_user.id
            )
            
            db.session.add(business)
            current_user.has_business = True
            db.session.commit()
            
            # Criar oportunidades automaticamente
            opportunities_created = []
            
            if sells_products or sells_services:
                offer_opp = Opportunity(
                    title=f"Oferta: {name}",
                    description=f"{sells_products or ''} {sells_services or ''}".strip(),
                    business_id=business.id,
                    user_id=current_user.id
                )
                db.session.add(offer_opp)
                opportunities_created.append("Oferta")
            
            if buys_products or buys_services:
                demand_opp = Opportunity(
                    title=f"Demanda: {name}",
                    description=f"Procuro: {buys_products or ''} {buys_services or ''}".strip(),
                    business_id=business.id,
                    user_id=current_user.id
                )
                db.session.add(demand_opp)
                opportunities_created.append("Demanda")
            
            db.session.commit()
            
            flash(f'Negócio cadastrado com sucesso! {len(opportunities_created)} oportunidade(s) criada(s).', 'success')
            return redirect(url_for('main.opportunities'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar negócio. Tente novamente.', 'danger')
            print(f"Erro criar negócio: {e}")
    
    return render_template('create_business.html')

@business_bp.route('/business/edit', methods=['GET', 'POST'])
@login_required
@limiter.limit(BUSINESS_LIMITS)  # 🔥 CORREÇÃO: String
def edit_business():
    business = Business.query.filter_by(user_id=current_user.id).first()
    
    if not business:
        flash('Você ainda não tem um negócio cadastrado.', 'warning')
        return redirect(url_for('business.create_business'))
    
    if request.method == 'POST':
        try:
            # Sanitizar todos os inputs
            business.name = sanitize_input(request.form.get('name'))
            business.description = sanitize_input(request.form.get('description'))
            business.business_sector = sanitize_input(request.form.get('business_sector'))
            business.business_category = sanitize_input(request.form.get('business_category'))
            business.city = sanitize_input(request.form.get('city'))
            business.state = sanitize_input(request.form.get('state'))
            business.sells_products = sanitize_input(request.form.get('sells_products'))
            business.sells_services = sanitize_input(request.form.get('sells_services'))
            business.buys_products = sanitize_input(request.form.get('buys_products'))
            business.buys_services = sanitize_input(request.form.get('buys_services'))
            
            business.location = f"{business.city}, {business.state}"
            business.tags = normalize_text(sanitize_input(request.form.get('tags', '')))
            
            db.session.commit()
            
            # Atualizar oportunidades existentes
            update_opportunities(business)
            
            flash('Negócio atualizado com sucesso!', 'success')
            return redirect(url_for('main.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar negócio. Tente novamente.', 'danger')
            print(f"Erro editar negócio: {e}")
    
    return render_template('edit_business.html', business=business)

def update_opportunities(business):
    """Atualiza oportunidades baseadas nos dados do negócio"""
    Opportunity.query.filter_by(business_id=business.id).delete()
    
    if business.sells_products or business.sells_services:
        offer_opp = Opportunity(
            title=f"Oferta: {business.name}",
            description=f"{business.sells_products or ''} {business.sells_services or ''}".strip(),
            business_id=business.id,
            user_id=business.user_id
        )
        db.session.add(offer_opp)
    
    if business.buys_products or business.buys_services:
        demand_opp = Opportunity(
            title=f"Demanda: {business.name}",
            description=f"Procuro: {business.buys_products or ''} {business.buys_services or ''}".strip(),
            business_id=business.id,
            user_id=business.user_id
        )
        db.session.add(demand_opp)
    
    db.session.commit()

@business_bp.route('/opportunities')
@login_required
def opportunities():
    if not current_user.has_business:
        return redirect(url_for('business.create_business'))
    return render_template('opportunities.html')

@business_bp.route('/api/opportunities')
@login_required
@limiter.limit(API_LIMITS)  # 🔥 CORREÇÃO: String
def api_opportunities():
    try:
        seen_opportunities = db.session.query(Interest.opportunity_id).filter(
            Interest.user_id == current_user.id
        )
        
        opportunities = Opportunity.query.filter(
            Opportunity.active == True,
            Opportunity.user_id != current_user.id,
            ~Opportunity.id.in_(seen_opportunities)
        ).all()
        
        if opportunities:
            opportunity_list = []
            for opp in opportunities:
                business = Business.query.get(opp.business_id)
                user = User.query.get(opp.user_id)
                
                opportunity_data = {
                    'id': opp.id,
                    'title': sanitize_input(opp.title),
                    'description': sanitize_input(opp.description),
                    'business_name': sanitize_input(business.name) if business else 'Negócio',
                    'business_type': sanitize_input(business.business_sector) if business else '',
                    'user_name': sanitize_input(user.name) if user else 'Usuário',
                    'user_phone': user.phone if user else '',
                    'user_company': sanitize_input(user.company) if user else '',
                    'user_id': user.id if user else None
                }
                opportunity_list.append(opportunity_data)
            
            return jsonify(opportunity_list)
        else:
            return jsonify({'empty': True})
    
    except Exception as e:
        print(f"Erro API oportunidades: {e}")
        return jsonify({'empty': True})

@business_bp.route('/api/swipe', methods=['POST'])
@login_required
@limiter.limit("100 per hour")  # 🔥 CORREÇÃO: String direta
def api_swipe():
    try:
        data = request.get_json()
        opportunity_id = data.get('opportunity_id')
        action = data.get('action')
        
        # Validar dados
        if not opportunity_id or action not in ['like', 'dislike']:
            return jsonify({'error': 'Dados inválidos'}), 400
        
        interest = Interest(
            user_id=current_user.id,
            opportunity_id=opportunity_id,
            interested=(action == 'like')
        )
        db.session.add(interest)
        
        match_created = False
        if action == 'like':
            opportunity = Opportunity.query.get(opportunity_id)
            if opportunity:
                mutual_like = Interest.query.filter(
                    Interest.user_id == opportunity.user_id,
                    Interest.interested == True,
                    Interest.opportunity_id.in_(
                        db.session.query(Opportunity.id).filter(
                            Opportunity.user_id == current_user.id
                        )
                    )
                ).first()
                
                if mutual_like:
                    match = Match(
                        user1_id=current_user.id,
                        user2_id=opportunity.user_id,
                        opportunity_id=opportunity_id
                    )
                    db.session.add(match)
                    match_created = True
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'match': match_created,
            'next_opportunity': True
        })
    
    except Exception as e:
        db.session.rollback()
        print(f"Erro API swipe: {e}")
        return jsonify({'error': 'Erro interno'}), 500

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
        print(f"Erro matches: {e}")
        return render_template('matches.html', matches=[])

@business_bp.route('/interests')
@login_required
def interests():
    if not current_user.has_business:
        return redirect(url_for('business.create_business'))
        
    try:
        user_opportunities = Opportunity.query.filter_by(user_id=current_user.id).all()
        interests_received = []
        
        for opp in user_opportunities:
            interests = Interest.query.filter(
                Interest.opportunity_id == opp.id, 
                Interest.interested == True,
                Interest.user_id != current_user.id
            ).all()
            
            for interest in interests:
                user = User.query.get(interest.user_id)
                if not user:
                    continue
                    
                business = Business.query.filter_by(user_id=user.id).first()
                
                existing_match = Match.query.filter(
                    ((Match.user1_id == current_user.id) & (Match.user2_id == user.id)) |
                    ((Match.user1_id == user.id) & (Match.user2_id == current_user.id))
                ).first()
                
                if not existing_match:
                    interests_received.append({
                        'opportunity_title': sanitize_input(opp.title),
                        'interested_user_name': sanitize_input(user.name),
                        'interested_user_phone': user.phone,
                        'interested_user_email': user.email,
                        'interested_business': sanitize_input(business.name) if business else 'Negócio',
                        'interest_date': interest.created_at.strftime('%d/%m/%Y %H:%M') if interest.created_at else 'Data não disponível'
                    })
        
        return render_template('interests.html', interests=interests_received)
    
    except Exception as e:
        print(f"Erro interests: {e}")
        return render_template('interests.html', interests=[])
