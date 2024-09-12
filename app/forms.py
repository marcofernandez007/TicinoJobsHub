from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    is_employer = BooleanField(_l('Register as Employer'))
    submit = SubmitField(_l('Register'))

class ProfileForm(FlaskForm):
    full_name = StringField(_l('Full Name'), validators=[DataRequired()])
    location = StringField(_l('Location'), validators=[DataRequired()])
    bio = TextAreaField(_l('Bio'), validators=[Length(min=0, max=280)])
    submit = SubmitField(_l('Update Profile'))

class JobForm(FlaskForm):
    title = StringField(_l('Job Title'), validators=[DataRequired()])
    description = TextAreaField(_l('Job Description'), validators=[DataRequired()])
    location = StringField(_l('Location'), validators=[DataRequired()])
    salary = StringField(_l('Salary'), validators=[DataRequired()])
    submit = SubmitField(_l('Post Job'))

class ApplicationForm(FlaskForm):
    submit = SubmitField(_l('Apply'))
