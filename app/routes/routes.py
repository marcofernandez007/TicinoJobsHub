from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from app import db
from app.forms import LoginForm, RegistrationForm, JobForm, ApplicationForm, SearchForm, ProfileForm
from app.models import User, Job, Application, Profile, get_job_recommendations
from flask_babel import _
from app.routes import bp

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
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
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

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if not current_user.profile:
            profile = Profile(user=current_user)
            db.session.add(profile)
        else:
            profile = current_user.profile
        profile.full_name = form.full_name.data
        profile.location = form.location.data
        profile.bio = form.bio.data
        profile.skills = form.skills.data
        profile.desired_salary = form.desired_salary.data
        profile.preferred_company_size = form.preferred_company_size.data
        db.session.commit()
        flash(_('Your profile has been updated.'))
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        if current_user.profile:
            form.full_name.data = current_user.profile.full_name
            form.location.data = current_user.profile.location
            form.bio.data = current_user.profile.bio
            form.skills.data = current_user.profile.skills
            form.desired_salary.data = current_user.profile.desired_salary
            form.preferred_company_size.data = current_user.profile.preferred_company_size
    recommended_jobs = get_job_recommendations(current_user)
    return render_template('profile.html', title=_('Profile'), form=form, recommended_jobs=recommended_jobs)

@bp.route('/job/<int:job_id>')
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job_details.html', title=_('Job Details'), job=job)

@bp.route('/job_listing')
def job_listing():
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('keyword', '')
    location = request.args.get('location', '')
    salary_min = request.args.get('salary_min', type=int)
    salary_max = request.args.get('salary_max', type=int)
    company_size = request.args.get('company_size', '')

    jobs_query = Job.query

    if keyword:
        jobs_query = jobs_query.filter(Job.title.contains(keyword) | Job.description.contains(keyword))
    if location:
        jobs_query = jobs_query.filter(Job.location.contains(location))
    if salary_min:
        jobs_query = jobs_query.filter(Job.salary_max >= salary_min)
    if salary_max:
        jobs_query = jobs_query.filter(Job.salary_min <= salary_max)
    if company_size:
        jobs_query = jobs_query.filter(Job.company_size == company_size)

    jobs = jobs_query.order_by(Job.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    
    recommended_jobs = []
    if current_user.is_authenticated and not current_user.is_employer:
        recommended_jobs = get_job_recommendations(current_user)

    return render_template('job_listing.html', title=_('Job Listings'), jobs=jobs, recommended_jobs=recommended_jobs)

@bp.route('/create_test_user')
def create_test_user():
    username = 'testuser'
    email = 'testuser@example.com'
    password = 'testpassword'
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Test user already exists'}), 200
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Test user created successfully'}), 201

@bp.route('/api/jobs')
def get_jobs():
    jobs = Job.query.order_by(Job.created_at.desc()).limit(10).all()
    return jsonify([{
        'id': job.id,
        'title': job.title,
        'location': job.location,
        'salary': f"{job.salary_min} - {job.salary_max}",
        'created_at': job.created_at.isoformat()
    } for job in jobs])
