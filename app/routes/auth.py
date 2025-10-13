from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('business.opportunities'))
    
    form = RegistrationForm(request.form)
    
    if request.method == 'POST' and form.validate():
        try:
            # Verificar se email já existe
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Este email já está cadastrado.', 'danger')
                return render_template('register.html', form=form)
            
            # Criar novo usuário
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            
            # Formatar telefone para armazenar apenas números
            phone_digits = ''.join(filter(str.isdigit, form.phone.data))
            
            user = User(
                name=form.name.data,
                email=form.email.data,
                phone=phone_digits,
                company=form.company.data,
                company_size=form.company_size.data,
                password=hashed_password
            )
            
            db.session.add(user)
            db.session.commit()
            
            flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
            print(f"✅ Usuário criado: {user.name} - Redirecionando para login...")
            return redirect(url_for('auth.login'))  # 🔧 GARANTIR REDIRECT
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erro no cadastro: {e}")
            flash('Erro ao realizar cadastro. Tente novamente.', 'danger')
    
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm(request.form)
    
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login falhou. Verifique seu email e senha.', 'danger')
    
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
