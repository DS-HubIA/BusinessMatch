from app import create_app, db
from app.models import User, Business, Opportunity, Interest, Match
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    print("🔄 RECRIANDO BANCO COMPLETO...")
    
    # Drop e create todas as tabelas
    db.drop_all()
    db.create_all()
    
    print("✅ Estrutura do banco criada com novas colunas!")
    
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
    print("✅ 3 usuários de teste criados")
    
    # Criar negócios de exemplo com NOVA estrutura
    businesses_data = [
        {
            'name': 'Desenvolvimento Software Inovação',
            'entrepreneur_name': 'Carlos Silva',
            'description': 'Desenvolvimento de sistemas web e mobile customizados com tecnologias modernas',
            'business_sector': 'Tecnologia',
            'business_category': 'Software',
            'sells_products': 'Sistemas web, aplicativos mobile, ERP customizado',
            'sells_services': 'Consultoria em TI, desenvolvimento customizado, suporte técnico',
            'buys_products': 'Servidores, equipamentos de TI, notebooks',
            'buys_services': 'Design gráfico, marketing digital, contabilidade',
            'city': 'São Paulo',
            'state': 'SP',
            'tags': 'software,tecnologia,desenvolvimento,inovacao',
            'user': created_users[0]
        },
        {
            'name': 'Consultoria Empresarial Pro',
            'entrepreneur_name': 'Ana Santos', 
            'description': 'Consultoria especializada em gestão empresarial e processos organizacionais',
            'business_sector': 'Serviços',
            'business_category': 'Consultoria',
            'sells_services': 'Consultoria em gestão, treinamentos corporativos, planejamento estratégico',
            'buys_products': 'Material de escritório, equipamentos, mobiliário',
            'buys_services': 'TI, contabilidade, limpeza, marketing',
            'city': 'Rio de Janeiro',
            'state': 'RJ',
            'tags': 'consultoria,gestao,empresarial,estrategia',
            'user': created_users[1]
        },
        {
            'name': 'Serviços Integrados MEI',
            'entrepreneur_name': 'Roberto Lima',
            'description': 'Serviços gerais e manutenção para empresas e residências',
            'business_sector': 'Serviços',
            'business_category': 'Manutenção',
            'sells_services': 'Limpeza predial, manutenção elétrica, pintura, pequenos reparos',
            'buys_products': 'Material de limpeza, ferramentas, tintas, lâmpadas',
            'buys_services': 'Transporte, contabilidade, assessoria jurídica',
            'city': 'Belo Horizonte',
            'state': 'MG',
            'tags': 'servicos,manutencao,limpeza,reparos',
            'user': created_users[2]
        }
    ]
    
    for biz_data in businesses_data:
        business = Business(
            name=biz_data['name'],
            entrepreneur_name=biz_data['entrepreneur_name'],
            description=biz_data['description'],
            business_sector=biz_data['business_sector'],
            business_category=biz_data['business_category'],
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
    print("✅ 3 negócios de exemplo criados com nova estrutura")
    
    # Criar oportunidades automaticamente
    businesses = Business.query.all()
    opportunities_count = 0
    
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
            opportunities_count += 1
        
        # Oportunidade de DEMANDA
        if business.buys_products or business.buys_services:
            demand_opp = Opportunity(
                title=f"Demanda: {business.name}",
                description=f"Procuro: {business.buys_products or ''} {business.buys_services or ''}".strip(),
                business_id=business.id, 
                user_id=business.user_id
            )
            db.session.add(demand_opp)
            opportunities_count += 1
    
    db.session.commit()
    print(f"✅ {opportunities_count} oportunidades criadas automaticamente")
    
    # Criar alguns interesses de teste
    opportunities = Opportunity.query.all()
    if len(opportunities) >= 2:
        # User2 dá like na oportunidade do User1
        interest1 = Interest(
            user_id=created_users[1].id,
            opportunity_id=opportunities[0].id,
            interested=True
        )
        db.session.add(interest1)
        
        # User3 dá like na oportunidade do User1
        interest2 = Interest(
            user_id=created_users[2].id,
            opportunity_id=opportunities[0].id,
            interested=True
        )
        db.session.add(interest2)
        
        db.session.commit()
        print("✅ 2 interesses de teste criados")
    
    print("\\n🎉 BANCO RECRIADO COM SUCESSO!")
    print("📊 RESUMO:")
    print(f"   👥 {User.query.count()} usuários")
    print(f"   🏢 {Business.query.count()} negócios") 
    print(f"   💼 {Opportunity.query.count()} oportunidades")
    print(f"   ❤️ {Interest.query.count()} interesses")
    
    print("\\n🔑 LOGINS PARA TESTE:")
    for user in created_users:
        print(f"   📧 {user.email} | 🔑 123456")
    
    print("\\n🚀 AGORA TESTE:")
    print("   1. Login com qualquer usuário acima")
    print("   2. Vá em 'Perfil' - deve ver negócios")
    print("   3. Cadastre novo negócio - formulário completo")
    print("   4. Explore oportunidades - sistema de swipe")
    print("   5. Verifique matches e interesses")
