from app import create_app
from app.static_config import configure_static
import os

app = create_app()

# Configurar arquivos estáticos apenas em produção
if os.environ.get('FLASK_ENV') == 'production':
    configure_static(app)

if __name__ == '__main__':
    # Em produção, usar gunicorn. Este arquivo é apenas para desenvolvimento.
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000)), 
        debug=debug_mode
    )
