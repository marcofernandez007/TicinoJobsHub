from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional
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

class JobForm(FlaskForm):
    title = StringField(_l('Job Title'), validators=[DataRequired()])
    description = TextAreaField(_l('Job Description'), validators=[DataRequired()])
    location = StringField(_l('Location'), validators=[DataRequired()])
    salary_min = IntegerField(_l('Minimum Salary'), validators=[DataRequired(), NumberRange(min=0)], render_kw={"step": "1000"})
    salary_max = IntegerField(_l('Maximum Salary'), validators=[DataRequired(), NumberRange(min=0)], render_kw={"step": "1000"})
    company_size = SelectField(_l('Company Size'), choices=[
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501+', '501+ employees')
    ], validators=[DataRequired()])
    submit = SubmitField(_l('Post Job'))

class ApplicationForm(FlaskForm):
    submit = SubmitField(_l('Apply'))

class SearchForm(FlaskForm):
    keyword = StringField(_l('Keyword'))
    location = StringField(_l('Location'))
    salary_min = IntegerField(_l('Minimum Salary'), validators=[Optional(), NumberRange(min=0)], render_kw={"step": "1000"})
    salary_max = IntegerField(_l('Maximum Salary'), validators=[Optional(), NumberRange(min=0)], render_kw={"step": "1000"})
    company_size = SelectField(_l('Company Size'), choices=[
        ('', 'Any'),
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501+', '501+ employees')
    ], validators=[Optional()])
    submit = SubmitField(_l('Search'))
