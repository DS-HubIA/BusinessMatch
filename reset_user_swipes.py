from app import create_app, db
from app.models import User, Swipe

app = create_app()

with app.app_context():
    # Encontrar usuário por email
    user_email = "tech@empresa.com"
    user = User.query.filter_by(email=user_email).first()
    
    if user:
        print(f"Resetando swipes do usuário: {user.entrepreneur_name} ({user.email})")
        
        # Deletar todos os swipes do usuário
        swipes_deleted = Swipe.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        
        print(f"Swipes deletados: {swipes_deleted}")
        print("Usuário agora pode ver todas as oportunidades novamente!")
    else:
        print(f"Usuário {user_email} não encontrado")

    # Mostrar estatísticas
    total_users = User.query.count()
    total_swipes = Swipe.query.count()
    
    print(f"\n--- ESTATÍSTICAS ---")
    print(f"Total de usuários: {total_users}")
    print(f"Total de swipes no sistema: {total_swipes}")
