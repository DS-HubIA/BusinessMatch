from wtforms import Form, StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
import re

class RegistrationForm(Form):
    name = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    phone = StringField('WhatsApp', validators=[DataRequired()])
    company = StringField('Empresa', validators=[DataRequired()])
    company_size = SelectField('Porte da Empresa', 
                              choices=[('', 'Selecione...'), 
                                      ('MEI', 'MEI - Microempreendedor Individual'),
                                      ('ME', 'ME - Microempresa'), 
                                      ('EPP', 'EPP - Empresa de Pequeno Porte')],
                              validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

    def validate_phone(self, phone):
        phone_digits = re.sub(r'\D', '', phone.data)
        if len(phone_digits) != 11:
            raise ValidationError('WhatsApp deve ter 11 dígitos (DDD + número com 9)')

class LoginForm(Form):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')
