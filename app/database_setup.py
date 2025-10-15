from app.models import User
from flask_bcrypt import Bcrypt

def setup_database(app, db):  # ✅ RECEBER db COMO PARÂMETRO
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
                
                # Criar múltiplos admins - SEM BUSINESS para não aparecer nos matches
                bcrypt = Bcrypt(app)
                hashed_password = bcrypt.generate_password_hash('Sebrae@2025').decode('utf-8')
                
                admins = [
                    User(
                        name='Diego SEBRAE - ADMIN',
                        email='diegos@sebraesp.com.br',
                        phone='(11) 99999-9999',
                        company='SEBRAE-SP',
                        company_size='EPP',
                        password=hashed_password,
                        terms_accepted=True,
                        is_admin=True,
                        has_business=False  # ✅ CRÍTICO: Admin NÃO tem negócio
                    ),
                    User(
                        name='Admin 2 SEBRAE',
                        email='admin2@sebrae.com',
                        phone='(11) 88888-8888',
                        company='SEBRAE Nacional',
                        company_size='EPP',
                        password=hashed_password,
                        terms_accepted=True,
                        is_admin=True,
                        has_business=False
                    ),
                    User(
                        name='Admin 3 SEBRAE',
                        email='admin3@sebrae.com',
                        phone='(11) 77777-7777',
                        company='SEBRAE Regional',
                        company_size='EPP',
                        password=hashed_password,
                        terms_accepted=True,
                        is_admin=True,
                        has_business=False
                    )
                ]
                
                for admin in admins:
                    existing_admin = User.query.filter_by(email=admin.email).first()
                    if not existing_admin:
                        db.session.add(admin)
                        print(f"✅ Admin criado: {admin.email}")
                    else:
                        print(f"✅ Admin já existe: {admin.email}")
                
                db.session.commit()
                print("✅ Database configurado automaticamente!")
                print("✅ Admins criados SEM business - não aparecerão nos matches")
            else:
                print("✅ Database já está configurado")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no setup do database: {e}")
            return False
