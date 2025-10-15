from app import create_app
from app.models import User, Opportunity, Interest

app = create_app()

with app.app_context():
    print('🔍 DIAGNÓSTICO DA QUERY:')
    
    # 1. Verificar usuário
    user = User.query.filter_by(email='tech@empresa.com').first()
    print(f'1. Usuário: {user.email if user else "NÃO ENCONTRADO"}')
    
    # 2. Verificar oportunidades totais
    total_opps = Opportunity.query.count()
    print(f'2. Oportunidades totais: {total_opps}')
    
    # 3. Verificar interesses do usuário
    user_interests = Interest.query.filter_by(user_id=user.id).count() if user else 0
    print(f'3. Interesses do usuário: {user_interests}')
    
    # 4. Testar a query completa
    if user:
        from sqlalchemy.orm import joinedload
        
        print('4. Executando query da API...')
        try:
            opportunities = Opportunity.query\
                .filter(Opportunity.user_id != user.id)\
                .filter(Opportunity.active == True)\
                .join(Opportunity.business)\
                .options(joinedload(Opportunity.business))\
                .limit(5)\
                .all()
            
            print(f'   ✅ Query executada - {len(opportunities)} oportunidades')
            for opp in opportunities:
                print(f'      - {opp.business.name}')
                
        except Exception as e:
            print(f'   ❌ Erro na query: {e}')
