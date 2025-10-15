from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User, Business, Opportunity, Interest, Match
from app.security import limiter, sanitize_input, validate_email, validate_phone, AUTH_LIMITS
from app.audit_logger import audit_logger

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
@limiter.limit(AUTH_LIMITS)
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.opportunities'))
    
    if request.method == 'POST':
        name = sanitize_input(request.form.get('name'))
        email = sanitize_input(request.form.get('email'))
        phone = sanitize_input(request.form.get('phone'))
        company = sanitize_input(request.form.get('company'))
        company_size = sanitize_input(request.form.get('company_size'))
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms_accepted = request.form.get('terms_accepted')
        
        # Validações de segurança
        if not validate_email(email):
            flash('Email inválido!', 'danger')
            audit_logger.log_security_event(f"Tentativa de registro com email inválido: {email}")
            return render_template('register.html')
        
        if not validate_phone(phone):
            flash('Telefone inválido!', 'danger')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('Senha deve ter pelo menos 8 caracteres!', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Senhas não coincidem!', 'danger')
            return render_template('register.html')
        
        if not terms_accepted:
            flash('Você deve aceitar os Termos de Uso para se cadastrar.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado!', 'danger')
            return render_template('register.html')
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(
            name=name,
            email=email,
            phone=phone,
            company=company,
            company_size=company_size,
            password=hashed_password,
            terms_accepted=True
        )
        
        db.session.add(user)
        db.session.commit()
        
        # 🔥 LOG DE AUDITORIA
        audit_logger.log_account_creation()
        
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit(AUTH_LIMITS)
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    
    if request.method == 'POST':
        email = sanitize_input(request.form.get('email'))
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            
            # 🔥 LOG DE AUDITORIA - Login bem-sucedido
            audit_logger.log_login(success=True)
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.profile'))
        else:
            # 🔥 LOG DE AUDITORIA - Login falhou
            audit_logger.log_login(success=False, reason="Credenciais inválidas")
            flash('Login falhou. Verifique email e senha!', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # 🔥 LOG DE AUDITORIA - Logout
    audit_logger.log_event('USER_LOGOUT', 'User logged out')
    
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/delete-account', methods=['POST'])
@login_required
@limiter.limit("5 per hour")
def delete_account():
    try:
        user_id = current_user.id
        user_email = current_user.email

        Interest.query.filter_by(user_id=user_id).delete()
        Match.query.filter((Match.user1_id == user_id) | (Match.user2_id == user_id)).delete()

        user_businesses = Business.query.filter_by(user_id=user_id).all()
        for business in user_businesses:
            business_opportunities = Opportunity.query.filter_by(business_id=business.id).all()
            for opportunity in business_opportunities:
                Interest.query.filter_by(opportunity_id=opportunity.id).delete()
                Match.query.filter_by(opportunity_id=opportunity.id).delete()
            
            Opportunity.query.filter_by(business_id=business.id).delete()
        
        Business.query.filter_by(user_id=user_id).delete()
        User.query.filter_by(id=user_id).delete()
        
        db.session.commit()

        # 🔥 LOG DE AUDITORIA - Conta excluída
        audit_logger.log_account_deletion()
        audit_logger.log_event('ACCOUNT_DATA_DELETED', f'All data for user {user_email} deleted')

        flash('Sua conta e todos os dados foram excluídos com sucesso.', 'success')
        return redirect(url_for('main.index'))
        
    except Exception as e:
        db.session.rollback()
        audit_logger.log_security_event(f"Erro ao excluir conta: {str(e)}", severity='HIGH')
        flash('Erro ao excluir conta. Tente novamente.', 'danger')
        return redirect(url_for('main.profile'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Solicitar reset de senha"""
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Gerar token (simplificado por agora)
            import secrets
            token = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=24)
            
            reset_token = PasswordResetToken(
                user_id=user.id,
                token=token,
                expires_at=expires_at
            )
            
            db.session.add(reset_token)
            db.session.commit()
            
            # Aqui enviaria email com link (por enquanto só mostra)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            flash(f'Link de reset enviado para {email}. Link: {reset_url}', 'info')
        else:
            flash('Email não encontrado.', 'error')
        
        return redirect(url_for('auth.forgot_password'))
    
    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Resetar senha com token"""
    reset_token = PasswordResetToken.query.filter_by(token=token).first()
    
    if not reset_token or not reset_token.is_valid():
        flash('Link inválido ou expirado.', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Senhas não coincidem.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if len(password) < 6:
            flash('Senha deve ter pelo menos 6 caracteres.', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        # Atualizar senha
        user = reset_token.user
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        reset_token.used = True
        
        db.session.commit()
        
        flash('Senha redefinida com sucesso! Faça login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)
