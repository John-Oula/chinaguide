from flask_wtf import FlaskForm
from wtforms import  validators,StringField, TextAreaField, SelectField, DateTimeField, FileField, SubmitField


class Session_form(FlaskForm):
    title = StringField('TITLE',[validators.DataRequired()])
    description = TextAreaField('DESCRIPTION',[validators.DataRequired()])
    category = SelectField('CATEGORY', choices=[('MANDARIN','MANDARIN'), ('LEGAL', 'LEGAL'), ('CAREER', 'CAREER'), ('BUSINESS', 'BUSINESS'), ('LIVING', 'LIVING')],widget=None)
    date = DateTimeField("DATE",[validators.DataRequired()])
class Upload_form(FlaskForm):
    title = StringField('Title')
    category = SelectField('Category', choices=[('Mandarin','Mandarin'), ('Communication skills', 'Communication skills'), ('Academics', 'Academics'), ('Visa', 'Visa'), ('Living', 'Living'), ('Talent policy', 'Talent policy'), ('Finance & Law', 'Finance & Law'), ('Entrepreneur', 'Entrepreneur'), ('Others', 'Others')],widget=None)
    description = StringField('Description')
    price = StringField('Price')
    upload = FileField('Upload')
    submit = SubmitField('Submit')

class Lesson_form(FlaskForm):
    title = StringField()
    description = TextAreaField()

class Comment_form(FlaskForm):
    content = StringField()
    submit = SubmitField('Submit')