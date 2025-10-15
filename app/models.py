from flask_login import UserMixin
from datetime import datetime
from app import db

# Categorias pré-definidas para padronização
BUSINESS_SECTORS = [
    'Comércio', 'Serviços', 'Indústria', 'Agronegócio', 'Tecnologia',
    'Saúde', 'Educação', 'Construção Civil', 'Alimentação', 'Moda',
    'Transporte', 'Turismo', 'Financeiro', 'Imobiliário', 'Outros'
]

BUSINESS_CATEGORIES = {
    'Comércio': ['Varejo', 'Atacado', 'E-commerce', 'Shopping', 'Loja Conveniência'],
    'Serviços': ['Consultoria', 'Manutenção', 'Limpeza', 'Transporte', 'Educação', 'Saúde'],
    'Indústria': ['Alimentícia', 'Têxtil', 'Metalmecânica', 'Química', 'Farmacêutica'],
    'Agronegócio': ['Agricultura', 'Pecuária', 'Agroindústria', 'Fruticultura'],
    'Tecnologia': ['Software', 'Hardware', 'TI', 'Internet', 'Telecomunicações'],
    'Saúde': ['Hospital', 'Clínica', 'Farmácia', 'Laboratório'],
    'Educação': ['Escola', 'Curso', 'Faculdade', 'Treinamento'],
    'Construção Civil': ['Construtora', 'Incorporadora', 'Materiais'],
    'Alimentação': ['Restaurante', 'Lanches', 'Supermercado', 'Padaria'],
    'Moda': ['Confecção', 'Calçados', 'Acessórios'],
    'Transporte': ['Logística', 'Carga', 'Passageiros'],
    'Turismo': ['Hotel', 'Agência', 'Eventos'],
    'Financeiro': ['Banco', 'Seguros', 'Investimentos'],
    'Imobiliário': ['Imobiliária', 'Corretagem'],
    'Outros': ['Outros']
}

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    company_size = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    has_business = db.Column(db.Boolean, default=False)
    terms_accepted = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)  # 🔥 CORREÇÃO: Campo admin adicionado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    businesses = db.relationship('Business', backref='owner', lazy=True)
    opportunities = db.relationship('Opportunity', backref='creator', lazy=True)

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    entrepreneur_name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(18), nullable=False)
    description = db.Column(db.Text, nullable=False)
    business_sector = db.Column(db.String(50), nullable=False)
    business_category = db.Column(db.String(50), nullable=False)
    
    # O que VENDE (OFERTA)
    sells_products = db.Column(db.Text)
    sells_services = db.Column(db.Text)
    
    # O que COMPRA (DEMANDA)  
    buys_products = db.Column(db.Text)
    buys_services = db.Column(db.Text)
    
    tags = db.Column(db.String(200))
    location = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    
    # Fotos
    profile_image = db.Column(db.String(200))
    cover_image = db.Column(db.String(200))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    opportunities = db.relationship('Opportunity', backref='business', lazy=True)

    @staticmethod
    def validate_cnpj(cnpj):
        """
        Valida CNPJ com dígitos verificadores reais
        """
        # Limpar caracteres não numéricos
        cnpj = ''.join(filter(str.isdigit, cnpj))
        
        # Verificar se tem 14 dígitos
        if len(cnpj) != 14:
            return False
        
        # Verificar se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False
        
        # Cálculo do primeiro dígito verificador
        soma = 0
        peso = 5
        for i in range(12):
            soma += int(cnpj[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        # Verificar primeiro dígito
        if digito1 != int(cnpj[12]):
            return False
        
        # Cálculo do segundo dígito verificador
        soma = 0
        peso = 6
        for i in range(13):
            soma += int(cnpj[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        # Verificar segundo dígito
        if digito2 != int(cnpj[13]):
            return False
        
        return True

class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'), nullable=False)
    interested = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunity.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    opportunity = db.relationship('Opportunity', backref='matches')

class Product(db.Model):
    """Modelo para produtos/serviços dos negócios"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    category = db.Column(db.String(50))
    tags = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    business = db.relationship('Business', backref=db.backref('products', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'tags': self.tags,
            'image_url': self.image_url,
            'business_id': self.business_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.name}>'

class PasswordResetToken(db.Model):
    """Tokens para reset de senha"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('reset_tokens', lazy=True))
    
    def is_valid(self):
        return not self.used and self.expires_at > datetime.utcnow()

class Configuration(db.Model):
    """Configurações do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_value(key, default=None):
        config = Configuration.query.filter_by(key=key).first()
        return config.value if config else default
    
    @staticmethod
    def set_value(key, value):
        config = Configuration.query.filter_by(key=key).first()
        if config:
            config.value = value
        else:
            config = Configuration(key=key, value=value)
            db.session.add(config)
        db.session.commit()
        return config
