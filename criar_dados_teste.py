from app import create_app
from app.models import User, Business, Opportunity
from datetime import datetime

app = create_app()

with app.app_context():
    # Encontrar todos os usuários exceto o atual
    current_user = User.query.filter_by(email='tech@empresa.com').first()
    other_users = User.query.filter(User.id != current_user.id).all()
    
    opportunities_count = 0
    
    for user in other_users:
        if user.businesses:
            business = user.businesses[0]
            
            # Criar oportunidade baseada no negócio
            opp = Opportunity(
                description=f"Oportunidade de parceria com {business.name} - {business.business_sector}",
                business_id=business.id,
                user_id=user.id,
                active=True,
                created_at=datetime.utcnow()
            )
            
            # Adicionar tags baseadas no setor
            if 'tech' in business.business_sector.lower():
                opp.tags = 'tecnologia,inovacao,startup'
            elif 'consultoria' in business.business_sector.lower():
                opp.tags = 'consultoria,servicos,negocios'
            else:
                opp.tags = 'parceria,colaboracao,negocios'
                
            from app import db
            db.session.add(opp)
            opportunities_count += 1
    
    if opportunities_count > 0:
        db.session.commit()
        print(f"✅ {opportunities_count} oportunidades de teste criadas")
    else:
        print("ℹ️  Criando usuários de teste...")
        
        # Criar usuário de teste se não existir
        new_user = User(
            email='parceiro@empresa.com',
            entrepreneur_name='João Parceiro',
            phone='11999999999',
            company_size='media',
            password_hash='teste123'
        )
        db.session.add(new_user)
        db.session.commit()
        
        # Criar negócio
        business = Business(
            name='Tech Solutions Parceira',
            entrepreneur_name='João Parceiro',
            cnpj='12.345.678/0001-99',
            description='Empresa de tecnologia buscando parcerias',
            business_sector='Tecnologia',
            business_category='Software',
            sells_products='Sistemas ERP',
            sells_services='Desenvolvimento customizado',
            user_id=new_user.id
        )
        db.session.add(business)
        db.session.commit()
        
        # Criar oportunidade
        opp = Opportunity(
            description='Buscamos parceiros para desenvolvimento conjunto',
            business_id=business.id,
            user_id=new_user.id,
            active=True,
            tags='tecnologia,parceria,desenvolvimento'
        )
        db.session.add(opp)
        db.session.commit()
        print("✅ Usuário e oportunidade de teste criados")
