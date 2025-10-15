from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import get_config
from app.security import limiter
from app.middleware import security_headers
from app.csrf import init_csrf
from app.database_setup import setup_database  # ✅ NOVO: Setup automático

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=None):
    if config_class is None:
        config_class = get_config()
    
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ✅ SEGURANÇA: Ativar CSRF primeiro
    init_csrf(app)

    # Inicializar extensões com o app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # ✅ DATABASE: Setup automático (CRÍTICO)
    setup_database(app)
    
    # Inicializar rate limiting
    limiter.init_app(app)

    # Importar modelos DEPOIS de inicializar db
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registrar blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.business import business_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(business_bp)
    
    # Aplicar headers de segurança
    @app.after_request
    def apply_security_headers(response):
        return security_headers(response)
    
    return app
