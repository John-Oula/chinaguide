from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import validators,StringField, PasswordField, SubmitField, ValidationError, IntegerField, DateField, FileField
from wtforms.validators import Required

from flask_blog.models import User


class Signup_form(FlaskForm):
    email = StringField('EMAIL', [validators.Email()])
    username = StringField('USERNAME', [validators.Length(min=4,max=15)])
    password = PasswordField('PASSWORD', [validators.DataRequired(),validators.Length(min=6)])
    confirm_password = PasswordField('CONFIRM PASSWORD',[validators.DataRequired(),validators.EqualTo('password',message='Password must much')])
    submit = SubmitField('Submit')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email already exists')




class Login_form(FlaskForm):
    username = StringField('USERNAME', [validators.Length(min=4,max=15)])
    password = PasswordField('PASSWORD', [validators.DataRequired()])
    submit = SubmitField()

    def check_username(self,username):
        user = User.query.filter_by(username=username.data)
        if username not in user.username:
            raise ValidationError('That username does not exist')

class Verify_form(FlaskForm):

    id_type = StringField('ID type', validators=[Required()])
    id_number = StringField('ID number.', validators=[Required()])
    id_document = StringField('ID document', validators=[Required()])
    email = StringField('Email', validators=[Required()])
    nationality = StringField('Nationality', validators=[Required()])
    province = StringField('Province', validators=[Required()])
    city = StringField('City', validators=[Required()])
    occupation = StringField('Occupation', validators=[Required()])
    phone = IntegerField('Phone', validators=[Required()])
#    city = RadioField('City',choices=[('Bengbu','Bengbu'),('Hefei','Hefei'),('Huainan','Huainan'),('Huangshan','Huangshan'),('Ma’anshan','Ma’anshan'),('Shexian','Shexian'),('Tongcheng','Tongcheng') ('Tongling','Tongling'),('Wuhu','Wuhu'),('Xuancheng','Xuancheng')])



class Payment_form(FlaskForm):

    card_number = IntegerField('Card number', validators=[Required()])
    cardholder = StringField('Cardholders name' , validators=[Required()])
    exp_date = DateField('Expiry Date', validators=[Required()])
    cvc = IntegerField('CVC', validators=[Required()])
    zip = StringField('ZIP', validators=[Required()])
    address = StringField('Address', validators=[Required()])


class UpdateAccount(FlaskForm):

    fullname = StringField('FULLNAME', [validators.Length(min=4,max=15)])
    username = StringField('USERNAME', [validators.Length(min=4,max=15)])
    email = StringField('EMAIL', [validators.Length(min=4,max=15)])
    pic = FileField('Update Profile photo')
    password = PasswordField('PASSWORD', [validators.DataRequired()])

    submit = SubmitField('Submit')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username has been taken')

class Request_reset(FlaskForm):
    email = StringField('EMAIL', [validators.Email()])
    submit = SubmitField()

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('THere is no email registered')

class Reset_password(FlaskForm):
    password = PasswordField('PASSWORD', [validators.DataRequired(),validators.Length(min=6)])
    confirm_password = PasswordField('CONFIRM PASSWORD',[validators.DataRequired(),validators.EqualTo('password',message='Password must much')])
    submit = SubmitField('Reset')
