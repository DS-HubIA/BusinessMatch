import os
from app import db
from app.models import User
from flask_bcrypt import Bcrypt

def setup_database(app):
    """Configura o database automaticamente se as tabelas não existirem"""
    with app.app_context():
        try:
            # Verificar se a tabela user existe
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'user' not in tables:
                print("🔧 Criando tabelas do banco de dados...")
                db.create_all()
                
                # Criar admin padrão
                bcrypt = Bcrypt(app)
                hashed_password = bcrypt.generate_password_hash('Sebrae@2025').decode('utf-8')
                
                admin_user = User(
                    name='Diego M Smorigo',
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
                print("✅ Database configurado automaticamente!")
            else:
                print("✅ Database já está configurado")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no setup do database: {e}")
            return False
