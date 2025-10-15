from app import create_app, db
from app.models import User, Business

app = create_app()

with app.app_context():
    print("🔄 Atualizando banco com campo CNPJ...")
    
    try:
        # Para desenvolvimento: recriar tabelas
        # Em produção usaríamos migrations
        
        # Backup dos dados existentes
        users = User.query.all()
        businesses = Business.query.all()
        
        user_backup = []
        for user in users:
            user_backup.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'phone': user.phone,
                'company': user.company,
                'company_size': user.company_size,
                'password': user.password,
                'has_business': user.has_business,
                'created_at': user.created_at
            })
        
        business_backup = []
        for biz in businesses:
            business_backup.append({
                'id': biz.id,
                'name': biz.name,
                'entrepreneur_name': biz.entrepreneur_name,
                'description': biz.description,
                'business_sector': biz.business_sector,
                'business_category': biz.business_category,
                'sells_products': biz.sells_products,
                'sells_services': biz.sells_services,
                'buys_products': biz.buys_products,
                'buys_services': biz.buys_services,
                'tags': biz.tags,
                'location': biz.location,
                'city': biz.city,
                'state': biz.state,
                'user_id': biz.user_id,
                'created_at': biz.created_at
            })
        
        # Recriar tabelas
        db.drop_all()
        db.create_all()
        
        # Restaurar usuários
        for user_data in user_backup:
            user = User(
                id=user_data['id'],
                name=user_data['name'],
                email=user_data['email'],
                phone=user_data['phone'],
                company=user_data['company'],
                company_size=user_data['company_size'],
                password=user_data['password'],
                has_business=user_data['has_business'],
                created_at=user_data['created_at']
            )
            db.session.add(user)
        
        db.session.commit()
        print("✅ Usuários restaurados")
        
        # Restaurar negócios com CNPJ fake (para desenvolvimento)
        cnpj_counter = 1
        for biz_data in business_backup:
            cnpj = f"{cnpj_counter:014d}"  # Gera CNPJ sequencial
            cnpj_formatted = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
            
            business = Business(
                id=biz_data['id'],
                name=biz_data['name'],
                entrepreneur_name=biz_data['entrepreneur_name'],
                cnpj=cnpj_formatted,
                description=biz_data['description'],
                business_sector=biz_data['business_sector'],
                business_category=biz_data['business_category'],
                sells_products=biz_data['sells_products'],
                sells_services=biz_data['sells_services'],
                buys_products=biz_data['buys_products'],
                buys_services=biz_data['buys_services'],
                tags=biz_data['tags'],
                location=biz_data['location'],
                city=biz_data['city'],
                state=biz_data['state'],
                user_id=biz_data['user_id'],
                created_at=biz_data['created_at']
            )
            db.session.add(business)
            cnpj_counter += 1
        
        db.session.commit()
        print("✅ Negócios restaurados com CNPJ")
        
        print("🎉 Banco atualizado com sucesso!")
        print(f"👥 {len(user_backup)} usuários")
        print(f"🏢 {len(business_backup)} negócios com CNPJ")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar banco: {e}")
        db.session.rollback()
