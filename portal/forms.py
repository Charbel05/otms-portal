import flask_wtf
import psycopg2
from wtforms import FileField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from portal.models import User_otms

class FormLogin(flask_wtf.FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,100)])
    lembrar = BooleanField('Lembrar-me')
    enviar_login = SubmitField('Enviar', validators=[DataRequired()])

class FormPhoto(flask_wtf.FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    btt_confirm = SubmitField("Salvar")