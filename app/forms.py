from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])

class UsuarioForm(FlaskForm):
    nome = StringField('nome', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired()])
    is_admin = BooleanField('is_admin', default=False)

class ClientForm(FlaskForm):
    nome = StringField('nome', validators=[DataRequired()])

class ComponentForm(FlaskForm):
    modulo_pai = SelectField('modulo_pai', validators=[DataRequired()])
    nome = StringField('nome', validators=[DataRequired()])
    tipo_component = SelectField('tipo_component', validators=[DataRequired()])

class DispositivoForm(FlaskForm):
    leaf = SelectField('leaf', validators=[DataRequired()])
    porta = IntegerField('porta', validators=[DataRequired()])
    tipo_dispositivo = SelectField('tipo_dispositivo', validators=[DataRequired()])