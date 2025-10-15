from whitenoise import WhiteNoise
import os

def configure_static(app):
    """Configurar servidor de arquivos estáticos para produção"""
    app.wsgi_app = WhiteNoise(
        app.wsgi_app, 
        root=os.path.join(os.path.dirname(__file__), 'static'),
        prefix='static/'
    )
    
    # Adicionar arquivos estáticos extras se necessário
    # app.wsgi_app.add_files('/path/to/static/files')
