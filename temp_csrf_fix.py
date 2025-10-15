from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import get_config
from app.security import init_security
from app.middleware import security_headers
from app.csrf import init_csrf  # ✅ NOVO: CSRF Protection

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
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # ✅ SEGURANÇA: Headers e Rate Limiting
    init_security(app)
    
    # Security headers middleware
    app.after_request(security_headers)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.business import business_bp
    from app.routes.matches import matches_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(business_bp)
    app.register_blueprint(matches_bp)
    
    return app
