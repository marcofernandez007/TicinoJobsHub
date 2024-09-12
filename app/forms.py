from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, ValidationError
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
    vat_number = StringField(_l('VAT Number'), validators=[Optional()])
    submit = SubmitField(_l('Register'))

class JobForm(FlaskForm):
    title = StringField(_l('Job Title'), validators=[DataRequired()])
    description = TextAreaField(_l('Job Description'), validators=[DataRequired()])
    location = StringField(_l('Location'), validators=[DataRequired()])
    salary_min = IntegerField(_l('Minimum Salary'), validators=[DataRequired(), NumberRange(min=0)])
    salary_max = IntegerField(_l('Maximum Salary'), validators=[DataRequired(), NumberRange(min=0)])
    company_size = SelectField(_l('Company Size'), choices=[
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501+', '501+ employees')
    ], validators=[DataRequired()])
    submit = SubmitField(_l('Post Job'))

class ApplicationForm(FlaskForm):
    cover_letter = TextAreaField(_l('Cover Letter'), validators=[DataRequired(), Length(min=50, max=1000)])
    resume = TextAreaField(_l('Resume'), validators=[DataRequired(), Length(min=100, max=2000)])
    submit = SubmitField(_l('Submit Application'))

class SearchForm(FlaskForm):
    keyword = StringField(_l('Keyword'))
    location = StringField(_l('Location'))
    salary_min = IntegerField(_l('Minimum Salary'), validators=[Optional(), NumberRange(min=0)])
    salary_max = IntegerField(_l('Maximum Salary'), validators=[Optional(), NumberRange(min=0)])
    company_size = SelectField(_l('Company Size'), choices=[
        ('', 'Any'),
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501+', '501+ employees')
    ], validators=[Optional()])
    submit = SubmitField(_l('Search'))

class ProfileForm(FlaskForm):
    full_name = StringField(_l('Full Name'), validators=[DataRequired()])
    location = StringField(_l('Location'), validators=[DataRequired()])
    bio = TextAreaField(_l('Bio'), validators=[Optional(), Length(max=500)])
    skills = StringField(_l('Skills'), validators=[Optional()])
    desired_salary = IntegerField(_l('Desired Salary'), validators=[Optional(), NumberRange(min=0)])
    preferred_company_size = SelectField(_l('Preferred Company Size'), choices=[
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501+', '501+ employees')
    ], validators=[Optional()])
    submit = SubmitField(_l('Update Profile'))
