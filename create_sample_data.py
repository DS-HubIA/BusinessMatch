from app import create_app, db
from app.models import User, Business

def create_sample_data():
    app = create_app()
    with app.app_context():
        # Limpar dados existentes primeiro
        db.drop_all()
        db.create_all()
        
        # Criar usuário de exemplo
        user = User(
            name="João Silva",
            email="joao@empresa.com", 
            phone="11999999999",
            company="Tech Solutions Ltda"
        )
        user.set_password("123456")
        
        # Criar negócios de exemplo
        business1 = Business(
            title="Sistema de Gestão para Varejo",
            description="Solução completa para gestão de estoque, vendas e financeiro para redes de lojas.",
            business_type="OFERTA",
            category="Tecnologia",
            user_id=1
        )
        
        business2 = Business(
            title="Consultoria em Marketing Digital", 
            description="Serviços completos de marketing digital para pequenas e médias empresas.",
            business_type="OFERTA", 
            category="Marketing",
            user_id=1
        )
        
        business3 = Business(
            title="Busco Parceiro para Distribuição",
            description="Empresa busca parceiro para distribuição de produtos em todo território nacional.",
            business_type="DEMANDA",
            category="Logística", 
            user_id=1
        )
        
        db.session.add(user)
        db.session.add(business1)
        db.session.add(business2)
        db.session.add(business3)
        db.session.commit()
        print("✅ Dados de exemplo criados!")
        print("📧 Usuário: joao@empresa.com / Senha: 123456")

if __name__ == '__main__':
    create_sample_data()
