import flask_wtf
from pyparsing import Regex
from wtforms import FileField, IntegerField, SelectField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Regexp

class FormLogin(flask_wtf.FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,100)])
    lembrar = BooleanField('Lembrar-me')
    enviar_login = SubmitField('Enviar', validators=[DataRequired()])

class FormRPN(flask_wtf.FlaskForm):
    part_number = SelectField('Part number', choices=[('', 'Selecione um Part Number')], validators=[DataRequired()])
    location = SelectField('Location', render_kw={'data-base-url':'teste'},choices=[('', 'Selecione uma localização')], validators=[DataRequired()])
    ci_level = SelectField('Costumer impact level', choices=[('', 'Selecione uma opção'), ('4', 'Incomplete'), ('1', 'No Impact'), ('2', 'Shipment Delays'), ('3', 'Costumer Shutdown')], validators=[DataRequired()])
    scondition = SelectField('Spare Condition', choices=[('', 'Selecione uma opção'), ('6', 'Incomplete'), ('1', 'Excellent Condition'), ('3', 'Good Condition'), ('5', 'Fair Condition'), ('4', 'Poor Condition'), ('2', 'Do Not Use or No Spare')], validators=[DataRequired()])
    savailability = SelectField('Spare Availability', choices=[('', 'Selecione uma opção'),('5', 'Incomplete'), ('1', 'Installed Spare'), ('3', 'Spare On Site or Off Site < 8 Hours Lead Time'), ('2', 'Spare On Site or Off Site > 8 Hours Lead Time'), ('4', 'No Spare')], validators=[DataRequired()])
    vsupport = SelectField('Vendor Support', choices=[('', 'Selecione uma opção'), ('1', 'Very Limited'), ('2', 'Poor'), ('3', 'Marginal'), ('4', 'Adequate'), ('5', 'Excellent'), ('6', 'Incomplete')], validators=[DataRequired()])
    scomplexity = SelectField('System Complecity', choices=[('', 'Selecione uma opção'), ('1', 'Low & Multiple Sourcing'), ('2', 'Medium Specialized & Limited Sourcing'), ('3', 'Medium Specialized & Multiple Sourcing'), ('4', 'Highly Specialized &  Limited Sourcing'), ('5', 'Incomplete')], validators=[DataRequired()])
    sgroup = SelectField('System Group', choices=[('', 'Selecione uma opção')], validators=[DataRequired()])
    inactive = BooleanField('Inactive')
    quantity = StringField('Installed quantity')
    cost = StringField('Cost')
    project_number = StringField('Project Number')
    description = StringField('Description')
    contingency = SelectField('Contingency', choices=[])
    save_btt = SubmitField('Salvar', validators=[DataRequired()])

class FormAddVendor(flask_wtf.FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    after_sales_support = BooleanField('After sales support')
    active = BooleanField('Active')
    region = SelectField('Region', choices=[])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(min=10, max=14), Regexp(regex=r'^\+?1?\d{9,15}$', message="Número de telefone inválido.")])
    email = StringField('E-mail', validators=[Email(message="Por favor, insira um endereço de e-mail válido.")])
    site = StringField('Site')
    save_btt = SubmitField('Salvar', validators=[DataRequired()])

class FormAddPartNumber(flask_wtf.FlaskForm):
    part_number = StringField('Part Number', validators=[DataRequired()])
    product = StringField('Product', validators=[DataRequired()])
    vendor = SelectField('Vendor', choices=[])
    obsolescence = SelectField('Obsolescence', choices=[])
    year_discontinued = StringField('Year of Discontinued State', validators=[DataRequired()])
    foto = FileField("Foto", validators=[DataRequired()])
    save_btt = SubmitField('Salvar', validators=[DataRequired()])