#!/bin/bash

echo "INICIANDO CORREÇÕES - FASE 4"

echo "1. CORRIGINDO BASE.HTML"
cat > app/templates/base.html << 'BASE_EOF'
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Business Match SEBRAE{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/professional.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
    
    {% block scripts %}{% endblock %}
</body>
</html>
BASE_EOF
echo "BASE.HTML OK"

echo "2. ATUALIZANDO DASHBOARD"
cat > app/templates/dashboard.html << 'DASH_EOF'
{% extends "base.html" %}

{% block title %}Dashboard - Business Match{% endblock %}

{% block content %}
<div class="app-header">
    <h1>Dashboard</h1>
</div>

<div style="padding: 20px;">
    <h2>Bem-vindo, {{ current_user.entrepreneur_name }}!</h2>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>📊</h3>
            <p>Seu Negócio</p>
            <a href="{{ url_for('business.edit_business') }}">Ver Detalhes</a>
        </div>
        
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>💼</h3>
            <p>Oportunidades</p>
            <a href="{{ url_for('business.opportunities') }}">Explorar</a>
        </div>
        
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>❤️</h3>
            <p>Matches</p>
            <a href="{{ url_for('business.matches') }}">Ver Matches</a>
        </div>
        
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>👀</h3>
            <p>Interesses</p>
            <a href="{{ url_for('business.interests') }}">Ver Interesses</a>
        </div>
    </div>
</div>

<nav class="bottom-nav">
    <a href="{{ url_for('main.dashboard') }}" class="nav-item active">
        <span class="nav-icon">📊</span>
        <span>Dashboard</span>
    </a>
    <a href="{{ url_for('business.opportunities') }}" class="nav-item">
        <span class="nav-icon">💼</span>
        <span>Oportunidades</span>
    </a>
    <a href="{{ url_for('business.matches') }}" class="nav-item">
        <span class="nav-icon">❤️</span>
        <span>Matches</span>
    </a>
    <a href="{{ url_for('business.interests') }}" class="nav-item">
        <span class="nav-icon">👀</span>
        <span>Interesses</span>
    </a>
    <a href="{{ url_for('main.profile') }}" class="nav-item">
        <span class="nav-icon">👤</span>
        <span>Perfil</span>
    </a>
</nav>
{% endblock %}
DASH_EOF
echo "DASHBOARD OK"

echo "3. ATUALIZANDO PROFILE"
cat > app/templates/profile.html << 'PROFILE_EOF'
{% extends "base.html" %}

{% block title %}Perfil - Business Match{% endblock %}

{% block content %}
<div class="app-header">
    <h1>Meu Perfil</h1>
</div>

<div style="padding: 20px;">
    <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
        <h3>Informações Pessoais</h3>
        <p><strong>Nome:</strong> {{ current_user.entrepreneur_name }}</p>
        <p><strong>Email:</strong> {{ current_user.email }}</p>
        <p><strong>Telefone:</strong> {{ current_user.phone }}</p>
        <p><strong>Porte da Empresa:</strong> {{ current_user.company_size }}</p>
    </div>
    
    {% if current_user.has_business %}
    <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
        <h3>Meu Negócio</h3>
        <p><strong>Nome:</strong> {{ current_user.businesses[0].name }}</p>
        <p><strong>CNPJ:</strong> {{ current_user.businesses[0].cnpj }}</p>
        <p><strong>Setor:</strong> {{ current_user.businesses[0].business_sector }}</p>
        <a href="{{ url_for('business.edit_business') }}" style="color: #4169E1;">Editar Negócio</a>
    </div>
    {% else %}
    <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
        <p>Você ainda não cadastrou um negócio.</p>
        <a href="{{ url_for('business.create_business') }}" style="color: #4169E1;">Cadastrar Negócio</a>
    </div>
    {% endif %}
</div>

<nav class="bottom-nav">
    <a href="{{ url_for('main.dashboard') }}" class="nav-item">
        <span class="nav-icon">📊</span>
        <span>Dashboard</span>
    </a>
    <a href="{{ url_for('business.opportunities') }}" class="nav-item">
        <span class="nav-icon">💼</span>
        <span>Oportunidades</span>
    </a>
    <a href="{{ url_for('business.matches') }}" class="nav-item">
        <span class="nav-icon">❤️</span>
        <span>Matches</span>
    </a>
    <a href="{{ url_for('business.interests') }}" class="nav-item">
        <span class="nav-icon">👀</span>
        <span>Interesses</span>
    </a>
    <a href="{{ url_for('main.profile') }}" class="nav-item active">
        <span class="nav-icon">👤</span>
        <span>Perfil</span>
    </a>
</nav>
{% endblock %}
PROFILE_EOF
echo "PROFILE OK"

echo "4. ATUALIZANDO MATCHES"
cat > app/templates/matches.html << 'MATCHES_EOF'
{% extends "base.html" %}

{% block title %}Matches - Business Match{% endblock %}

{% block content %}
<div class="app-header">
    <h1>Matches</h1>
</div>

<div style="padding: 20px;">
    {% if matches %}
        {% for match in matches %}
        <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px;">
            <h3>{{ match.business.name }}</h3>
            <p>{{ match.business.description[:100] }}...</p>
            <p><strong>Interesse mútuo identificado!</strong></p>
            <a href="https://wa.me/55{{ match.business.user.phone|replace(' ', '')|replace('-', '')|replace('(', '')|replace(')', '') }}?text=Olá! Encontrei você no Business Match SEBRAE. Gostaria de conversar sobre oportunidades de negócio."
               target="_blank" 
               style="background: #25D366; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; display: inline-block;">
               💬 Conversar no WhatsApp
            </a>
        </div>
        {% endfor %}
    {% else %}
        <div style="background: white; padding: 20px; border-radius: 10px; text-align: center;">
            <p>Nenhum match encontrado ainda.</p>
            <p>Continue explorando oportunidades para encontrar matches!</p>
            <a href="{{ url_for('business.opportunities') }}" style="color: #4169E1;">Explorar Oportunidades</a>
        </div>
    {% endif %}
</div>

<nav class="bottom-nav">
    <a href="{{ url_for('main.dashboard') }}" class="nav-item">
        <span class="nav-icon">📊</span>
        <span>Dashboard</span>
    </a>
    <a href="{{ url_for('business.opportunities') }}" class="nav-item">
        <span class="nav-icon">💼</span>
        <span>Oportunidades</span>
    </a>
    <a href="{{ url_for('business.matches') }}" class="nav-item active">
        <span class="nav-icon">❤️</span>
        <span>Matches</span>
    </a>
    <a href="{{ url_for('business.interests') }}" class="nav-item">
        <span class="nav-icon">👀</span>
        <span>Interesses</span>
    </a>
    <a href="{{ url_for('main.profile') }}" class="nav-item">
        <span class="nav-icon">👤</span>
        <span>Perfil</span>
    </a>
</nav>
{% endblock %}
MATCHES_EOF
echo "MATCHES OK"

echo "5. CORRIGINDO VALIDAÇÃO CNPJ"
cp app/models.py app/models.py.backup

python << 'PYTHON_EOF'
with open('app/models.py', 'r') as f:
    content = f.read()

business_start = content.find('class Business(db.Model):')
if business_start == -1:
    print("CLASSE BUSINESS NAO ENCONTRADA")
    exit(1)

next_class = content.find('\nclass ', business_start + 1)
if next_class == -1:
    next_class = len(content)

class_content = content[business_start:next_class]
lines = class_content.split('\n')
last_content_line = 0
for i, line in enumerate(lines):
    if line.strip() and not line.strip().startswith('#'):
        last_content_line = i

method = '''
    @staticmethod
    def validate_cnpj(cnpj):
        cnpj = ''.join(filter(str.isdigit, cnpj))
        if len(cnpj) != 14:
            return False
        if cnpj == cnpj[0] * 14:
            return False
        soma = 0
        peso = 5
        for i in range(12):
            soma += int(cnpj[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        if digito1 != int(cnpj[12]):
            return False
        soma = 0
        peso = 6
        for i in range(13):
            soma += int(cnpj[i]) * peso
            peso = 9 if peso == 2 else peso - 1
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        if digito2 != int(cnpj[13]):
            return False
        return True
'''

new_class_content = '\n'.join(lines[:last_content_line + 1]) + method + '\n'.join(lines[last_content_line + 1:])
new_content = content[:business_start] + new_class_content + content[next_class:]

with open('app/models.py', 'w') as f:
    f.write(new_content)

print("VALIDACAO CNPJ INSERIDA")
PYTHON_EOF

echo "6. TESTANDO CORREÇÕES"
python -c "
from app.models import Business
print('TESTE CNPJ:')
print('12.345.678/0001-95:', Business.validate_cnpj('12.345.678/0001-95'))
print('11.222.333/0001-81:', Business.validate_cnpj('11.222.333/0001-81'))
print('12.345.678/0001-00:', Business.validate_cnpj('12.345.678/0001-00'))
"

python -c "
templates = ['dashboard.html', 'profile.html', 'matches.html', 'base.html']
for tpl in templates:
    with open(f'app/templates/{tpl}', 'r') as f:
        content = f.read()
    has_css = 'professional.css' in content
    uses_base = '{% extends' in content if tpl != 'base.html' else True
    status = 'OK' if has_css and uses_base else 'ERRO'
    print(f'{tpl}: {status}')
"

echo "CORREÇÕES CONCLUÍDAS"
echo "Execute: python run.py"
echo "Teste: http://127.0.0.1:5000/dashboard"
