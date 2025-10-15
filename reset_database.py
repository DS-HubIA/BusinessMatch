from app import create_app, db
from app.models import User, Business, Opportunity, Interest, Match
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    print("🔄 Recriando banco do zero com nova estrutura...")
    
    # Drop e create todas as tabelas
    db.drop_all()
    db.create_all()
    
    print("✅ Banco recriado com sucesso!")
    
    # Criar usuários de teste
    users_data = [
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
    for user_data in users_data:
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
    print("✅ Usuários de teste criados")
    
    # Criar alguns negócios de exemplo
    businesses_data = [
        {
            'name': 'Desenvolvimento Software',
            'entrepreneur_name': 'Carlos Silva',
            'description': 'Desenvolvimento de sistemas web e mobile customizados',
            'business_type': 'Tecnologia',
            'category': 'Desenvolvimento de Software',
            'sells_products': 'Sistemas web, aplicativos mobile',
            'sells_services': 'Consultoria em TI, desenvolvimento customizado',
            'buys_products': 'Servidores, equipamentos de TI',
            'buys_services': 'Design gráfico, marketing digital',
            'city': 'São Paulo',
            'state': 'SP',
            'tags': 'software,tecnologia,desenvolvimento',
            'user': created_users[0]
        },
        {
            'name': 'Consultoria Empresarial',
            'entrepreneur_name': 'Ana Santos', 
            'description': 'Consultoria em gestão e processos empresariais',
            'business_type': 'Consultoria',
            'category': 'Consultoria Empresarial',
            'sells_services': 'Consultoria em gestão, treinamentos',
            'buys_products': 'Material de escritório, equipamentos',
            'buys_services': 'TI, contabilidade, limpeza',
            'city': 'Rio de Janeiro',
            'state': 'RJ',
            'tags': 'consultoria,gestão,empresarial',
            'user': created_users[1]
        }
    ]
    
    for biz_data in businesses_data:
        business = Business(
            name=biz_data['name'],
            entrepreneur_name=biz_data['entrepreneur_name'],
            description=biz_data['description'],
            business_type=biz_data['business_type'],
            category=biz_data['category'],
            sells_products=biz_data.get('sells_products', ''),
            sells_services=biz_data.get('sells_services', ''),
            buys_products=biz_data.get('buys_products', ''),
            buys_services=biz_data.get('buys_services', ''),
            city=biz_data['city'],
            state=biz_data['state'],
            location=f"{biz_data['city']}, {biz_data['state']}",
            tags=biz_data['tags'],
            user_id=biz_data['user'].id
        )
        db.session.add(business)
    
    db.session.commit()
    print("✅ Negócios de exemplo criados")
    
    # Criar oportunidades automaticamente
    businesses = Business.query.all()
    for business in businesses:
        # Oportunidade de OFERTA
        if business.sells_products or business.sells_services:
            offer_opp = Opportunity(
                title=f"Oferta: {business.name}",
                description=f"{business.sells_products or ''} {business.sells_services or ''}".strip(),
                business_id=business.id,
                user_id=business.user_id
            )
            db.session.add(offer_opp)
        
        # Oportunidade de DEMANDA
        if business.buys_products or business.buys_services:
            demand_opp = Opportunity(
                title=f"Demanda: {business.name}",
                description=f"Procuro: {business.buys_products or ''} {business.buys_services or ''}".strip(),
                business_id=business.id, 
                user_id=business.user_id
            )
            db.session.add(demand_opp)
    
    db.session.commit()
    print("✅ Oportunidades criadas automaticamente")
    
    print("\\n🎉 BANCO RECRIADO COM SUCESSO!")
    print("👥 Usuários:")
    for user in created_users:
        print(f"   - {user.name} ({user.email}) - Senha: 123456")
    
    print("🏢 Negócios criados com estrutura completa")
    print("💼 Oportunidades geradas automaticamente")
