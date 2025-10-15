from app import create_app
app = create_app()
with app.app_context():
    from app.models import User
    user = User.query.filter_by(email='tech@empresa.com').first()
    
    with app.test_client() as client:
        client.post('/login', data={'email': 'tech@empresa.com', 'password': '123456'})
        response = client.get('/api/opportunities')
        print(f'API Status: {response.status_code}')
        data = response.get_json()
        print(f'Dados retornados: {len(data) if data else 0}')
        if data:
            for opp in data:
                print(f"  - {opp.get('business_name', 'Sem nome')}")
