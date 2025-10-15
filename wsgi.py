from app import create_app
import os

# Configurar ambiente para produção
os.environ['FLASK_ENV'] = 'production'

app = create_app()

if __name__ == "__main__":
    app.run()
