from app import create_app, db
from app.models import User, Business, Opportunity, Interest, Match
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    print("🔄 RECRIANDO BANCO COMPLETO COM NOVA ESTRUTURA...")
    
    # Drop e create todas as tabelas
    db.drop_all()
    db.create_all()
    
    print("✅ Estrutura do banco criada com todas as colunas novas!")
    
    # Criar usuários de teste
    users_data = [
        {
            'name': 'Tech Solutions', 
            'email': 'tech@empresa.com',
            'phone': '11999990001',
            'company': 'Tech Solutions LTDA',
            'company_size': 'ME',
            'password': '123456',
            'has_business': True  # Já tem negócio cadastrado
        },
        {
            'name': 'Consultoria Excel',
            'email': 'consultoria@empresa.com', 
            'phone': '11999990002',
            'company': 'Consultoria Excelência',
            'company_size': 'EPP',
            'password': '123456',
            'has_business': True  # Já tem negócio cadastrado
        },
        {
            'name': 'Novo Usuário',
            'email': 'novo@empresa.com',
            'phone': '11999990003', 
            'company': 'Nova Empresa MEI',
            'company_size': 'MEI',
            'password': '123456',
            'has_business': False  # Ainda não tem negócio - vai para cadastro obrigatório
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
            password=hashed_pw,
            has_business=user_data['has_business']  # 🔥 NOVO CAMPO
        )
        db.session.add(user)
        created_users.append(user)
    
    db.session.commit()
    print("✅ 3 usuários de teste criados")
    
    # Criar negócios de exemplo com CNPJ
    businesses_data = [
        {
            'name': 'Desenvolvimento Software Inovação',
            'entrepreneur_name': 'Carlos Silva',
            'cnpj': '12.345.678/0001-90',  # 🔥 NOVO: CNPJ
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
            'cnpj': '98.765.432/0001-10',  # 🔥 NOVO: CNPJ
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
        }
    ]
    
    for biz_data in businesses_data:
        business = Business(
            name=biz_data['name'],
            entrepreneur_name=biz_data['entrepreneur_name'],
            cnpj=biz_data['cnpj'],  # 🔥 NOVO: CNPJ
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
    print("✅ 2 negócios de exemplo criados com CNPJ")
    
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
        
        db.session.commit()
        print("✅ Interesses de teste criados")
    
    print("\\n🎉 BANCO RECRIADO COM SUCESSO!")
    print("📊 RESUMO:")
    print(f"   👥 {User.query.count()} usuários")
    print(f"   🏢 {Business.query.count()} negócios com CNPJ") 
    print(f"   💼 {Opportunity.query.count()} oportunidades")
    print(f"   ❤️ {Interest.query.count()} interesses")
    
    print("\\n🔑 LOGINS PARA TESTE:")
    for user in created_users:
        business_status = "✅ Com negócio" if user.has_business else "📝 Precisa cadastrar"
        print(f"   📧 {user.email} | 🔑 123456 | {business_status}")
    
    print("\\n🚀 AGORA TESTE OS DOIS FLUXOS:")
    print("   1. Login com tech@empresa.com - Vai direto para oportunidades (já tem negócio)")
    print("   2. Login com novo@empresa.com - Vai para cadastro obrigatório de negócio")
    print("   3. Teste validação de CNPJ no formulário")
    print("   4. Após cadastro, navegação é liberada")
