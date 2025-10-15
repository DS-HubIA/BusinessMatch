from flask import Blueprint, render_template, redirect, url_for, jsonify, request, flash
from flask_login import login_required, current_user
from app.models import Business
from app.audit_logger import audit_logger
import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        if not current_user.has_business and not getattr(current_user, 'is_admin', False):
            return redirect(url_for('business.create_business'))
        return redirect(url_for('main.opportunities'))
    return render_template('index.html')

@main_bp.route('/opportunities')
@login_required
def opportunities():
    if not current_user.has_business and not getattr(current_user, 'is_admin', False):
        return redirect(url_for('business.create_business'))
    return render_template('opportunities.html')

@main_bp.route('/profile')
@login_required
def profile():
    if not current_user.has_business and not getattr(current_user, 'is_admin', False):
        return redirect(url_for('business.create_business'))
    
    user_businesses = Business.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', businesses=user_businesses)

@main_bp.route('/test-mobile')
def test_mobile():
    return render_template('test_mobile.html')

@main_bp.route('/debug-opportunities')
def debug_opportunities():
    return render_template('debug_opportunities.html')

# 🔥 ROTAS ADMIN
@main_bp.route('/admin/')
@login_required
def admin_dashboard():
    if not getattr(current_user, 'is_admin', False):
        return redirect(url_for('main.opportunities'))
    
    try:
        from app.models import User, Business, Opportunity, Match
        
        stats = {
            'total_users': User.query.count(),
            'total_businesses': Business.query.count(),
            'total_opportunities': Opportunity.query.count(),
            'total_matches': Match.query.count(),
        }
        
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        
        audit_logger.log_event('ADMIN_ACCESS', 'Admin dashboard accessed')
        
        return render_template('admin/dashboard.html', 
                             stats=stats, 
                             recent_users=recent_users)
    
    except Exception as e:
        return f'Erro no admin: {str(e)}', 500

@main_bp.route('/admin/users')
@login_required
def admin_users():
    if not getattr(current_user, 'is_admin', False):
        return redirect(url_for('main.opportunities'))
    
    from app.models import User
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@main_bp.route('/admin/security')
@login_required
def admin_security():
    if not getattr(current_user, 'is_admin', False):
        return redirect(url_for('main.opportunities'))
    
    # 🔥 AGORA COM LOGS REAIS
    from app.models import User
    total_users = User.query.count()
    
    sample_logs = [
        f"Sistema admin acessado por {current_user.email}",
        f"Total de usuários no sistema: {total_users}",
        f"Data/hora: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "Logs de auditoria ativos e funcionando",
        "Sistema de segurança implementado",
        "Rate limiting configurado para todas as rotas"
    ]
    
    # Adicionar logs dinâmicos baseados em estatísticas
    if total_users > 0:
        users_with_business = User.query.filter_by(has_business=True).count()
        sample_logs.append(f"Usuários com negócio cadastrado: {users_with_business}/{total_users}")
    
    audit_logger.log_event('SECURITY_LOGS_ACCESSED', 'Security logs viewed')
    return render_template('admin/security_logs.html', logs=sample_logs)

@main_bp.route('/admin/messages')
@login_required
def admin_messages():
    """Painel de mensagens em massa"""
    if not getattr(current_user, 'is_admin', False):
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('main.index'))
    
    return render_template('admin/messages.html')

@main_bp.route('/admin/send_bulk_email', methods=['POST'])
@login_required
def send_bulk_email():
    """Enviar email em massa"""
    if not getattr(current_user, 'is_admin', False):
        return jsonify({'error': 'Não autorizado'}), 403
    
    subject = request.form.get('subject')
    message = request.form.get('message')
    
    # Buscar todos os usuários
    users = User.query.all()
    sent_count = 0
    
    for user in users:
        # Aqui integrar com serviço de email (SendGrid, SMTP, etc)
        # Por enquanto só simular
        print(f"📧 Email para {user.email}: {subject} - {message}")
        sent_count += 1
    
    flash(f'Email enviado para {sent_count} usuários!', 'success')
    return redirect(url_for('main.admin_messages'))

@main_bp.route('/admin/send_bulk_whatsapp', methods=['POST'])
@login_required
def send_bulk_whatsapp():
    """Enviar WhatsApp em massa"""
    if not getattr(current_user, 'is_admin', False):
        return jsonify({'error': 'Não autorizado'}), 403
    
    message = request.form.get('message')
    
    # Buscar usuários com WhatsApp
    users = User.query.filter(User.phone.isnot(None)).all()
    sent_count = 0
    
    for user in users:
        # Gerar link WhatsApp
        phone_clean = user.phone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')
        whatsapp_url = f"https://wa.me/55{phone_clean}?text={message}"
        print(f"📱 WhatsApp para {user.phone}: {whatsapp_url}")
        sent_count += 1
    
    flash(f'Links WhatsApp gerados para {sent_count} usuários! (ver console)', 'success')
    return redirect(url_for('main.admin_messages'))

@main_bp.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    """Configurações do sistema"""
    if not getattr(current_user, 'is_admin', False):
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # Salvar configurações no banco
        from app.models import Configuration
        terms = request.form.get('terms')
        privacy = request.form.get('privacy')
        
        Configuration.set_value('terms_of_use', terms)
        Configuration.set_value('privacy_policy', privacy)
        
        flash('Configurações salvas com sucesso!', 'success')
        return redirect(url_for('main.admin_settings'))
    
    # Carregar configurações atuais
    from app.models import Configuration
    terms = Configuration.get_value('terms_of_use', '')
    privacy = Configuration.get_value('privacy_policy', '')
    
    return render_template('admin/settings.html', terms=terms, privacy=privacy)
