from app import create_app, db
from app.models import User, Business, Opportunity, Interest
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    print("🎯 CRIANDO INTERESSES DE TESTE...")
    
    # Buscar usuários
    user1 = User.query.filter_by(email='tech@empresa.com').first()  # Tech Solutions
    user2 = User.query.filter_by(email='consultoria@empresa.com').first()  # Consultoria Excel
    user3 = User.query.filter_by(email='servicos@empresa.com').first()  # Serviços Rápidos
    
    # Buscar oportunidades
    opp1 = Opportunity.query.filter_by(user_id=user1.id).first()  # Oportunidade do Tech
    opp2 = Opportunity.query.filter_by(user_id=user2.id).first()  # Oportunidade da Consultoria
    opp3 = Opportunity.query.filter_by(user_id=user3.id).first()  # Oportunidade dos Serviços
    
    # Criar interesses (likes)
    # User2 (Consultoria) dá like na oportunidade do User1 (Tech)
    interest1 = Interest(
        user_id=user2.id,
        opportunity_id=opp1.id,
        interested=True
    )
    
    # User3 (Serviços) dá like na oportunidade do User1 (Tech)  
    interest2 = Interest(
        user_id=user3.id,
        opportunity_id=opp1.id,
        interested=True
    )
    
    # User1 (Tech) dá like na oportunidade do User3 (Serviços)
    interest3 = Interest(
        user_id=user1.id, 
        opportunity_id=opp3.id,
        interested=True
    )
    
    db.session.add(interest1)
    db.session.add(interest2) 
    db.session.add(interest3)
    db.session.commit()
    
    print("✅ INTERESSES CRIADOS:")
    print(f"   - {user2.name} → gostou de '{opp1.title}'")
    print(f"   - {user3.name} → gostou de '{opp1.title}'") 
    print(f"   - {user1.name} → gostou de '{opp3.title}'")
    print("")
    print("🔍 AGORA TESTE:")
    print(f"   👤 Login como {user1.name} ({user1.email})")
    print("   💼 Vá em 'Interesses' - deve ver 2 interesses")
    print("   🤝 Vá em 'Matches' - deve ver 1 match (com {user3.name})")
