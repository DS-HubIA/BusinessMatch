from app import create_app
from app.models import User, Opportunity, Interest
app = create_app()
with app.app_context():
    user = User.query.filter_by(email='tech@empresa.com').first()
    print(f'Usuário: {user.name}')
    print(f'User ID: {user.id}')
    
    # Verificar todas as oportunidades
    all_opps = Opportunity.query.all()
    print(f'Todas oportunidades: {len(all_opps)}')
    for opp in all_opps:
        print(f'  - ID: {opp.id}, User: {opp.user_id}, Business: {opp.business_id}')
    
    # Verificar a query da API
    from sqlalchemy.orm import joinedload
    
    seen_opportunities = Interest.query.filter(Interest.user_id == user.id).subquery()
    opportunities = Opportunity.query.filter(
        Opportunity.active == True,
        Opportunity.user_id != user.id,
        ~Opportunity.id.in_(seen_opportunities)
    ).all()
    
    print(f'Oportunidades para API: {len(opportunities)}')
