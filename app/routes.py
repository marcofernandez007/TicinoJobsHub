from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from app import db
from app.forms import LoginForm, RegistrationForm, JobForm, ApplicationForm, SearchForm, ProfileForm
from app.models import User, Job, Application, Profile, get_job_recommendations
from flask_babel import _
from app.routes import bp
from app.business_verification import verify_business, get_business_details

@bp.route('/')
def index():
    return redirect(url_for('main.job_listing'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, is_employer=form.is_employer.data)
        user.set_password(form.password.data)
        if form.is_employer.data:
            if form.vat_number.data:
                is_verified, message = verify_business(form.username.data, form.vat_number.data)
                user.is_verified = is_verified
                user.vat_number = form.vat_number.data
                flash(message)
                if is_verified:
                    business_details = get_business_details(form.vat_number.data)
                    if business_details:
                        user.company_name = business_details.get('company_name')
                        user.company_address = business_details.get('address')
                        user.company_size = business_details.get('company_size')
            else:
                flash(_('VAT number is required for employer registration'))
                return render_template('register.html', title=_('Register'), form=form)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('main.login'))
    return render_template('register.html', title=_('Register'), form=form)

# ... (keep the rest of the file unchanged)
