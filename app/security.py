from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configuração CSP para Bootstrap CDN
csp = {
    'default-src': ['\'self\''],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        '\'unsafe-inline\''
    ],
    'script-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net'
    ],
    'font-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net'
    ],
    'img-src': ['\'self\'', 'data:', 'blob:']  # ✅ CORRIGIDO: adicionado 'blob:'
}

# ✅ CORREÇÃO: Criar limiter como variável GLOBAL
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per hour", "50 per minute"],
    storage_uri="memory://"
)

# Limites específicos para rotas
AUTH_LIMITS = "10 per minute"
BUSINESS_LIMITS = "20 per minute" 
API_LIMITS = "100 per hour"

def init_security(app):
    # Talisman para headers de segurança
    Talisman(
        app,
        content_security_policy=csp,
        force_https=False,  # True em produção
        strict_transport_security=True,
        session_cookie_secure=True,
        session_cookie_http_only=True,
        frame_options='DENY'
    )
    
    # Inicializar o rate limiter (já criado globalmente)
    limiter.init_app(app)
    
    return limiter

# Funções de validação
def sanitize_input(data):
    if data:
        return data.strip()
    return data

def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    import re
    pattern = r'^[\d\s\(\)\-\+]{10,20}$'
    return re.match(pattern, phone) is not None

def validate_cnpj(cnpj):
    import re
    pattern = r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$'
    return re.match(pattern, cnpj) is not None
