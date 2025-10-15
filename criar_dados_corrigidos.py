from app import create_app
from app.models import User, Business, Opportunity
from datetime import datetime

app = create_app()

with app.app_context():
    from app import db
    
    # Limpar dados existentes
    Opportunity.query.delete()
    Business.query.delete() 
    User.query.delete()
    db.session.commit()
    
    # Criar usuários de teste
    users_data = [
        {'email': 'tech@empresa.com', 'name': 'Tech Empresa', 'cnpj': '11.111.111/0001-11', 'sector': 'Tecnologia'},
        {'email': 'consultoria@empresa.com', 'name': 'Consultoria Pro', 'cnpj': '22.222.222/0001-22', 'sector': 'Consultoria'},
        {'email': 'parceiro@empresa.com', 'name': 'Parceiro Tech', 'cnpj': '33.333.333/0001-33', 'sector': 'Desenvolvimento'}
    ]
    
    for user_data in users_data:
        user = User(
            email=user_data['email'],
            entrepreneur_name=user_data['name'],
            phone='11999999999',
            company_size='media',
            password_hash='123456'
        )
        db.session.add(user)
        db.session.commit()
        
        business = Business(
            name=user_data['name'],
            entrepreneur_name=user_data['name'],
            cnpj=user_data['cnpj'],
            description=f'Descrição do negócio {user_data["name"]}',
            business_sector=user_data['sector'],
            business_category='Serviços',
            user_id=user.id
        )
        db.session.add(business)
        db.session.commit()
        
        # Criar oportunidades APENAS para outros usuários (não para tech@empresa.com)
        if user_data['email'] != 'tech@empresa.com':
            opp = Opportunity(
                description=f'Oportunidade de {user_data["sector"]} com {user_data["name"]}',
                business_id=business.id,
                user_id=user.id,
                active=True,
                tags=f'{user_data["sector"].lower()},parceria,negocios'
            )
            db.session.add(opp)
    
    db.session.commit()
    print("✅ Dados de teste criados corretamente")
    
    # Verificar
    opps = Opportunity.query.all()
    print(f"Oportunidades criadas: {len(opps)}")
    for opp in opps:
        print(f"  - {opp.description}")
