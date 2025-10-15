from app import create_app
app = create_app()
with app.app_context():
    from app.models import User
    user = User.query.filter_by(email='tech@empresa.com').first()
    
    with app.test_client() as client:
        client.post('/login', data={'email': 'tech@empresa.com', 'password': '123456'})
        response = client.get('/api/opportunities')
        print(f'Status: {response.status}')
        print(f'Content-Type: {response.content_type}')
        print(f'Dados brutos: {response.get_data()}')
