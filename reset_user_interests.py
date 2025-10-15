from app import create_app, db
from app.models import User, Interest, Match

app = create_app()

with app.app_context():
    # Encontrar usuário por email
    user_email = "tech@empresa.com"
    user = User.query.filter_by(email=user_email).first()
    
    if user:
        print(f"Resetando histórico do usuário: {user.name} ({user.email})")
        
        # Deletar todos os interesses do usuário
        interests_deleted = Interest.query.filter_by(user_id=user.id).delete()
        
        # Deletar todos os matches do usuário
        matches_deleted = Match.query.filter(
            (Match.user1_id == user.id) | (Match.user2_id == user.id)
        ).delete()
        
        db.session.commit()
        
        print(f"Interesses deletados: {interests_deleted}")
        print(f"Matches deletados: {matches_deleted}")
        print("✅ Usuário resetado - pode ver todas as oportunidades novamente!")
    else:
        print(f"❌ Usuário {user_email} não encontrado")

    # Mostrar estatísticas
    total_users = User.query.count()
    total_interests = Interest.query.count()
    total_matches = Match.query.count()
    
    print(f"\n--- ESTATÍSTICAS ATUAIS ---")
    print(f"Total de usuários: {total_users}")
    print(f"Total de interesses: {total_interests}")
    print(f"Total de matches: {total_matches}")
