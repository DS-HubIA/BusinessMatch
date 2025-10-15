from app import create_app, db
from app.models import User, Business, Opportunity

app = create_app()

with app.app_context():
    print("Recriando banco com estrutura 100% correta")
    
    db.drop_all()
    db.create_all()
    
    user1 = User(
        name="Tech Empresa",
        email="tech@empresa.com",
        phone="11999999999",
        company="Tech Solutions",
        company_size="media",
        password="123456"
    )
    db.session.add(user1)
    db.session.flush()
    
    business1 = Business(
        name="Tech Solutions",
        entrepreneur_name="Tech Empresa",
        cnpj="11.111.111/0001-11",
        description="Empresa de tecnologia",
        business_sector="Tecnologia",
        business_category="Software",
        sells_services="Desenvolvimento",
        user_id=user1.id
    )
    db.session.add(business1)
    user1.has_business = True
    
    user2 = User(
        name="Consultoria Pro",
        email="consultoria@empresa.com",
        phone="11988888888",
        company="Consultoria Pro",
        company_size="pequena",
        password="123456"
    )
    db.session.add(user2)
    db.session.flush()
    
    business2 = Business(
        name="Consultoria Empresarial",
        entrepreneur_name="Consultoria Pro",
        cnpj="22.222.222/0001-22",
        description="Consultoria especializada",
        business_sector="Consultoria",
        business_category="Serviços",
        sells_services="Consultoria",
        user_id=user2.id
    )
    db.session.add(business2)
    user2.has_business = True
    
    opp = Opportunity(
        title="Parceria em Consultoria",
        description="Buscamos parceiros para projetos",
        business_id=business2.id,
        user_id=user2.id,
        active=True
    )
    db.session.add(opp)
    
    db.session.commit()
    
    print("DADOS CRIADOS")
    print(f"Usuários: {User.query.count()}")
    print(f"Oportunidades: {Opportunity.query.count()}")
