from app import create_app, db
from app.models import Business  # 🔧 IMPORTAR OS MODELS

app = create_app()

with app.app_context():
    print("🔄 Atualizando banco com novas colunas...")
    
    try:
        # Para SQLite, precisamos recriar as tabelas
        # Em produção (PostgreSQL) usaríamos migrations
        
        # Backup dos dados existentes
        businesses = Business.query.all()
        backup_data = []
        
        for biz in businesses:
            backup_data.append({
                'id': biz.id,
                'name': biz.name,
                'description': biz.description,
                'business_type': biz.business_type,
                'category': biz.category,
                'tags': biz.tags,
                'location': biz.location,
                'user_id': biz.user_id,
                'created_at': biz.created_at
            })
        
        # Recriar tabelas
        db.drop_all()
        db.create_all()
        
        # Restaurar dados com novas colunas
        for data in backup_data:
            business = Business(
                id=data['id'],
                name=data['name'],
                entrepreneur_name=data['name'],  # Usar nome da empresa como fallback
                description=data['description'],
                business_type=data['business_type'],
                category=data['category'],
                tags=data['tags'],
                location=data['location'],
                city="São Paulo",  # Default
                state="SP",       # Default
                user_id=data['user_id'],
                created_at=data['created_at']
            )
            db.session.add(business)
        
        db.session.commit()
        print("✅ Banco atualizado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar banco: {e}")
        db.session.rollback()
