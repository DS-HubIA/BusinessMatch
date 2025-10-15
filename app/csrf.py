import os
import hmac
import hashlib
from flask import request, session, current_app

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = os.urandom(24).hex()
    return session['_csrf_token']

def validate_csrf_token(token):
    if not token:
        return False
    expected_token = session.get('_csrf_token')
    if not expected_token:
        return False
    return hmac.compare_digest(token, expected_token)

class CSRFProtect:
    def __init__(self):
        self.exempt_views = set()
    
    def init_app(self, app):
        app.jinja_env.globals['csrf_token'] = generate_csrf_token
        app.before_request(self._check_csrf)
    
    def exempt(self, view):
        self.exempt_views.add(view)
        return view
    
    def _check_csrf(self):
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):
            # Exempt API routes if needed
            if request.path.startswith('/api/'):
                return
            token = request.form.get('csrf_token')
            if not validate_csrf_token(token):
                from flask import abort
                abort(403, 'CSRF token inválido')

csrf = CSRFProtect()

def init_csrf(app):
    csrf.init_app(app)
    return csrf
