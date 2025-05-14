import flask_wtf
from pyparsing import Regex
from wtforms import FileField, SelectField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Regexp
from portal.models import Almox, Location, Obsolescence, Parts, Regions, System_groups, User_otms, Rpn, Vendors

class FormLogin(flask_wtf.FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,100)])
    lembrar = BooleanField('Lembrar-me')
    enviar_login = SubmitField('Enviar', validators=[DataRequired()])

class FormPhoto(flask_wtf.FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    btt_confirm = SubmitField("Salvar")

class FormRPN(flask_wtf.FlaskForm):
    part_number = SelectField('Part number', choices=[])
    vendor = StringField('Vendor')
    obsolescence = StringField('Obsolescence')

class FormAddVendor(flask_wtf.FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    after_sales_support = BooleanField('After sales support')
    active = BooleanField('Active')
    region = SelectField('Region', choices=[])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(min=10, max=14), Regexp(regex=r'^\+?1?\d{9,15}$', message="Número de telefone inválido.")])
    email = StringField('E-mail', validators=[Email(message="Por favor, insira um endereço de e-mail válido.")])
    site = StringField('Site')
    save_btt = SubmitField('Salvar', validators=[DataRequired()])