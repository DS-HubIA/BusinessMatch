from app import create_app, db
from app.models import User, Business, Opportunity, Interest, Match
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    # Limpar dados antigos
    Match.query.delete()
    Interest.query.delete()
    Opportunity.query.delete()
    Business.query.delete()
    User.query.delete()
    
    # Criar usuários reais
    users = [
        {
            'name': 'Tech Solutions', 
            'email': 'tech@empresa.com',
            'phone': '11999990001',
            'company': 'Tech Solutions LTDA',
            'company_size': 'ME',
            'password': '123456'
        },
        {
            'name': 'Consultoria Excel',
            'email': 'consultoria@empresa.com', 
            'phone': '11999990002',
            'company': 'Consultoria Excelência',
            'company_size': 'EPP',
            'password': '123456'
        },
        {
            'name': 'Serviços Rápidos',
            'email': 'servicos@empresa.com',
            'phone': '11999990003', 
            'company': 'Serviços Rápidos MEI',
            'company_size': 'MEI',
            'password': '123456'
        }
    ]
    
    created_users = []
    for user_data in users:
        hashed_pw = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user = User(
            name=user_data['name'],
            email=user_data['email'],
            phone=user_data['phone'],
            company=user_data['company'],
            company_size=user_data['company_size'],
            password=hashed_pw
        )
        db.session.add(user)
        created_users.append(user)
    
    db.session.commit()
    
    # Criar negócios reais
    businesses = [
        {'name': 'Desenvolvimento Software', 'type': 'Tecnologia', 'user': created_users[0], 'desc': 'Desenvolvimento de sistemas web e mobile customizados'},
        {'name': 'Consultoria Empresarial', 'type': 'Consultoria', 'user': created_users[1], 'desc': 'Consultoria em gestão e processos empresariais'},
        {'name': 'Serviços Gerais', 'type': 'Serviços', 'user': created_users[2], 'desc': 'Serviços de limpeza e manutenção predial'}
    ]
    
    created_businesses = []
    for biz_data in businesses:
        business = Business(
            name=biz_data['name'],
            description=biz_data['desc'],
            business_type=biz_data['type'],
            category=biz_data['type'],
            location="São Paulo, SP",
            user_id=biz_data['user'].id
        )
        db.session.add(business)
        created_businesses.append(business)
    
    db.session.commit()
    
    # Criar oportunidades reais
    opportunities = [
        {'title': 'Preciso de Desenvolvedor', 'business': created_businesses[1], 'desc': 'Busco desenvolvedor para projeto de e-commerce'},
        {'title': 'Consultoria em TI', 'business': created_businesses[0], 'desc': 'Ofereço consultoria em transformação digital'},
        {'title': 'Serviços de Limpeza', 'business': created_businesses[2], 'desc': 'Ofereço serviços de limpeza para empresas'}
    ]
    
    for opp_data in opportunities:
        opportunity = Opportunity(
            title=opp_data['title'],
            description=opp_data['desc'],
            business_id=opp_data['business'].id,
            user_id=opp_data['business'].user_id
        )
        db.session.add(opportunity)
    
    db.session.commit()
    
    print("🎉 DADOS REAIS CRIADOS!")
    print("👥 Usuários:")
    for user in created_users:
        print(f"   - {user.name} ({user.email}) - Senha: 123456")
    
    print("🏢 Negócios criados com oportunidades reais")
    print("💡 AGORA: Teste o sistema com lógica real de matching!")
