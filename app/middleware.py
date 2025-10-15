from flask import request, jsonify
from functools import wraps
import time

def security_headers(response):
    """Adiciona headers de segurança às respostas"""
    # Headers de segurança
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    
    return response

def require_roles(*roles):
    """Decorator para verificar roles de usuário"""
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            from flask_login import current_user
            
            if not current_user.is_authenticated:
                return jsonify({'error': 'Authentication required'}), 401
            
            # TODO: Implementar sistema de roles
            # Por enquanto, apenas verifica se é admin
            if 'admin' in roles and not getattr(current_user, 'is_admin', False):
                return jsonify({'error': 'Admin access required'}), 403
                
            return func(*args, **kwargs)
        return decorated_function
    return decorator

def log_security_event(event_type, description, user_id=None):
    """Log de eventos de segurança"""
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    user_info = f"User: {user_id}" if user_id else "Anonymous"
    
    log_entry = f"[{timestamp}] {event_type} - {description} - {user_info}"
    print(f"🔒 SECURITY: {log_entry}")
    
    # TODO: Salvar em arquivo de log ou banco de dados
