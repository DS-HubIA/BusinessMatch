from app import create_app, db
from app.models import User, Business, Opportunity
app = create_app()

with app.app_context():
    # Limpar oportunidades existentes
    Opportunity.query.delete()
    
    # Buscar todos os usuários exceto o principal
    main_user = User.query.filter_by(email='tech@empresa.com').first()
    other_users = User.query.filter(User.id != main_user.id).all()
    
    # Criar múltiplas oportunidades
    opportunities_data = [
        {"title": "Parceria Tech", "desc": "Buscamos desenvolvedores para projeto inovador", "sector": "Tecnologia"},
        {"title": "Consultoria Estratégica", "desc": "Oportunidade para consultores experientes", "sector": "Consultoria"},
        {"title": "Colaboração Marketing", "desc": "Procuramos parceiros em marketing digital", "sector": "Marketing"},
        {"title": "Desenvolvimento App", "desc": "Parceria para desenvolvimento de aplicativo", "sector": "Tecnologia"},
        {"title": "Expansão Comercial", "desc": "Buscamos representantes comerciais", "sector": "Vendas"},
        {"title": "Projeto Sustentabilidade", "desc": "Oportunidade em energias renováveis", "sector": "Sustentabilidade"},
        {"title": "Consultoria Financeira", "desc": "Precisamos de especialistas em finanças", "sector": "Consultoria"},
        {"title": "Parceria Logística", "desc": "Oportunidade em transporte e logística", "sector": "Logística"},
        {"title": "Desenvolvimento Web", "desc": "Procuramos desenvolvedores front-end", "sector": "Tecnologia"},
        {"title": "Consultoria Jurídica", "desc": "Buscamos advogados para parceria", "sector": "Consultoria"}
    ]
    
    created = 0
    for opp_data in opportunities_data:
        for user in other_users:
            if user.businesses:
                business = user.businesses[0]
                opp = Opportunity(
                    title=opp_data["title"],
                    description=opp_data["desc"],
                    business_id=business.id,
                    user_id=user.id,
                    active=True
                )
                db.session.add(opp)
                created += 1
    
    db.session.commit()
    print(f"✅ {created} oportunidades criadas")
