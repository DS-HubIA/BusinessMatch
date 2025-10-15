from app import create_app
import json
app = create_app()
with app.app_context():
    from app.models import User
    user = User.query.filter_by(email='tech@empresa.com').first()
    
    with app.test_client() as client:
        client.post('/login', data={'email': 'tech@empresa.com', 'password': '123456'})
        response = client.get('/api/opportunities')
        print(f'API Status: {response.status_code}')
        data = response.get_json()
        print(f'Tipo: {type(data)}')
        print(f'Keys: {list(data.keys()) if data else "VAZIO"}')
        print(f'Dados completos:')
        print(json.dumps(data, indent=2, ensure_ascii=False))
