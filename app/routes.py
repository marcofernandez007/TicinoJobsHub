from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_babel import _
from app import db
from app.models import User, Job, Application
from app.forms import LoginForm, RegistrationForm, JobForm, ApplicationForm
from app.utils import save_picture

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title=_('Home'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('login.html', title=_('Sign In'), form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, is_employer=form.is_employer.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('main.login'))
    return render_template('register.html', title=_('Register'), form=form)

@bp.route('/jobs')
def job_listing():
    page = request.args.get('page', 1, type=int)
    jobs = Job.query.order_by(Job.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('job_listing.html', title=_('Job Listings'), jobs=jobs)

@bp.route('/job/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_details.html', title=job.title, job=job)

@bp.route('/job/new', methods=['GET', 'POST'])
@login_required
def new_job():
    if not current_user.is_employer:
        flash(_('Only employers can post jobs.'))
        return redirect(url_for('main.index'))
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, description=form.description.data,
                  location=form.location.data, salary=form.salary.data,
                  employer=current_user)
        db.session.add(job)
        db.session.commit()
        flash(_('Your job has been posted!'))
        return redirect(url_for('main.job_listing'))
    return render_template('job_form.html', title=_('Post a New Job'), form=form)

@bp.route('/api/jobs')
def api_jobs():
    try:
        jobs = Job.query.order_by(Job.created_at.desc()).limit(10).all()
        return jsonify([{
            'id': job.id,
            'title': job.title,
            'location': job.location,
            'salary': job.salary,
            'created_at': job.created_at.isoformat()
        } for job in jobs])
    except Exception as e:
        current_app.logger.error(f"Error in api_jobs: {str(e)}")
        return jsonify({"error": "An error occurred while fetching jobs"}), 500
