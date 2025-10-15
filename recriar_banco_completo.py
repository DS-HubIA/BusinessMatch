from app import create_app, db
from app.models import User, Business, Opportunity
from datetime import datetime

app = create_app()

with app.app_context():
    print("🗑️  Limpando banco...")
    db.drop_all()
    db.create_all()
    
    print("👥 Criando usuários...")
    
    # Usuário principal (tech@empresa.com)
    user1 = User(
        email='tech@empresa.com',
        entrepreneur_name='Tech Empresa',
        phone='11999999999', 
        company_size='media',
        password_hash='123456'
    )
    db.session.add(user1)
    db.session.flush()  # Para obter o ID
    
    # Negócio do usuário principal
    business1 = Business(
        name='Tech Solutions',
        entrepreneur_name='Tech Empresa',
        cnpj='11.111.111/0001-11',
        description='Empresa de tecnologia especializada em desenvolvimento',
        business_sector='Tecnologia',
        business_category='Software',
        sells_services='Desenvolvimento web e mobile',
        user_id=user1.id
    )
    db.session.add(business1)
    
    # Outros usuários (para ter oportunidades)
    users_data = [
        {'email': 'consultoria@empresa.com', 'name': 'Consultoria Pro', 'sector': 'Consultoria'},
        {'email': 'marketing@empresa.com', 'name': 'Marketing Digital', 'sector': 'Marketing'},
        {'email': 'design@empresa.com', 'name': 'Design Studio', 'sector': 'Design'}
    ]
    
    for data in users_data:
        user = User(
            email=data['email'],
            entrepreneur_name=data['name'],
            phone='11988888888',
            company_size='pequena', 
            password_hash='123456'
        )
        db.session.add(user)
        db.session.flush()
        
        business = Business(
            name=data['name'],
            entrepreneur_name=data['name'],
            cnpj='22.222.222/0001-22',
            description=f'Descrição do {data["name"]}',
            business_sector=data['sector'],
            business_category='Serviços',
            user_id=user.id
        )
        db.session.add(business)
        db.session.flush()
        
        # Criar oportunidades para esses usuários
        opp = Opportunity(
            description=f'Oportunidade de {data["sector"].lower()} com {data["name"]}',
            business_id=business.id,
            user_id=user.id,
            active=True,
            tags=f'{data["sector"].lower()},servicos,parceria'
        )
        db.session.add(opp)
    
    db.session.commit()
    
    print("✅ BANCO RECRIADO COM:")
    print(f"   - {User.query.count()} usuários")
    print(f"   - {Business.query.count()} negócios") 
    print(f"   - {Opportunity.query.count()} oportunidades")
    
    # Verificar se o usuário principal existe
    user_tech = User.query.filter_by(email='tech@empresa.com').first()
    print(f"   - tech@empresa.com: {'✅ ENCONTRADO' if user_tech else '❌ NÃO ENCONTRADO'}")
