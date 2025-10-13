from app import create_app, db
from app.models import User, Business

def add_more_data():
    app = create_app()
    with app.app_context():
        # Criar mais negócios de exemplo
        businesses = [
            Business(
                title="Sistema ERP para Indústria",
                description="Solução completa de ERP para indústrias de médio porte com módulos personalizados.",
                business_type="OFERTA",
                category="Tecnologia",
                user_id=1
            ),
            Business(
                title="App Delivery Local",
                description="Plataforma de delivery para comércios locais com integração de pagamentos.",
                business_type="DEMANDA", 
                category="Tecnologia",
                user_id=1
            ),
            Business(
                title="Consultoria em Exportação",
                description="Consultoria especializada para empresas que desejam exportar seus produtos.",
                business_type="OFERTA",
                category="Consultoria",
                user_id=1
            ),
            Business(
                title="Busco Investidor para Startup",
                description="Startup de edtech busca investidor para expansão nacional.",
                business_type="DEMANDA",
                category="Investimento",
                user_id=1
            )
        ]
        
        for business in businesses:
            db.session.add(business)
        
        db.session.commit()
        print("✅ +4 oportunidades adicionadas!")

if __name__ == '__main__':
    add_more_data()
