from app import create_app, db
from app.models import User
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    print("Corrigindo senhas dos usuários...")
    
    users = User.query.all()
    for user in users:
        if user.password == '123456':  # Se a senha está em texto puro
            print(f"Corrigindo senha para {user.email}")
            user.password = bcrypt.generate_password_hash('123456').decode('utf-8')
        elif len(user.password) < 20:  # Se não parece ser um hash
            print(f"Re-hasheando senha para {user.email}")
            user.password = bcrypt.generate_password_hash('123456').decode('utf-8')
    
    db.session.commit()
    print("✅ Senhas corrigidas")
    
    # Verificar
    user = User.query.filter_by(email='tech@empresa.com').first()
    if user and bcrypt.check_password_hash(user.password, '123456'):
        print("✅ Login deve funcionar agora")
    else:
        print("❌ Problema persistente")
