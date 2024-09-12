from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_babel import _
from app import db
from app.models import User, Job, Application
from app.forms import LoginForm, RegistrationForm, JobForm, ApplicationForm, SearchForm
from app.utils import save_picture
from sqlalchemy import and_
import random
from urllib.parse import urlparse

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('main.job_listing', 
                                keyword=form.keyword.data,
                                location=form.location.data,
                                salary_min=form.salary_min.data,
                                salary_max=form.salary_max.data,
                                company_size=form.company_size.data))
    return render_template('index.html', title=_('Home'), form=form)

# ... (keep all other existing routes)

@bp.route('/jobs', methods=['GET', 'POST'])
def job_listing():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    
    if form.validate_on_submit() or request.args:
        filters = []
        keyword = form.keyword.data or request.args.get('keyword')
        location = form.location.data or request.args.get('location')
        salary_min = form.salary_min.data or request.args.get('salary_min')
        salary_max = form.salary_max.data or request.args.get('salary_max')
        company_size = form.company_size.data or request.args.get('company_size')
        
        if keyword:
            filters.append(Job.title.ilike(f'%{keyword}%'))
        if location:
            filters.append(Job.location.ilike(f'%{location}%'))
        if salary_min:
            filters.append(Job.salary_max >= salary_min)
        if salary_max:
            filters.append(Job.salary_min <= salary_max)
        if company_size:
            filters.append(Job.company_size == company_size)
        
        jobs = Job.query.filter(and_(*filters)).order_by(Job.created_at.desc()).paginate(page=page, per_page=10)
    else:
        jobs = Job.query.order_by(Job.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('job_listing.html', title=_('Job Listings'), jobs=jobs, form=form)

# ... (keep all other existing routes)
