import os
from datetime import timedelta

class ProductionConfig:
    # Segurança Básica
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32)
    DEBUG = False
    TESTING = False
    
    # Database PostgreSQL para produção
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'max_overflow': 20,
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Session Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Rate Limiting para produção
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')
    RATELIMIT_STRATEGY = 'fixed-window'
    RATELIMIT_DEFAULT = "1000 per day, 200 per hour"
    
    # CORS para produção
    CORS_ORIGINS = [
        "https://business-match-sebrae.onrender.com",
        "https://*.onrender.com"
    ]
    
    # Upload limits
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Performance
    JSONIFY_PRETTYPRINT_REGULAR = False
    EXPLAIN_TEMPLATE_LOADING = False
