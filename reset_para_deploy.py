import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    print("=== LIMPANDO BANCO PARA DEPLOY ===")
    
    # Deletar todos os usuários existentes
    User.query.delete()
    
    # Criar usuário admin real
    hashed_password = bcrypt.generate_password_hash('Sebrae@2025').decode('utf-8')
    
    admin_user = User(
        name='Diego Smorigo',
        email='diegos@sebraesp.com.br',
        phone='(11) 98737-8844',
        company='SEBRAE-SP',
        company_size='EPP',
        password=hashed_password,
        terms_accepted=True,
        is_admin=True,
        has_business=True
    )
    
    db.session.add(admin_user)
    db.session.commit()
    
    print("✅ Banco zerado com sucesso!")
    print("✅ Admin criado:")
    print(f"   Email: diegos@sebraesp.com.br")
    print(f"   Senha: a523R68@)")
    print(f"   Admin: Sim")
    
    # Verificar
    users = User.query.all()
    print(f"📊 Total de usuários no banco: {len(users)}")
