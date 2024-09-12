from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import ForeignKey
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_employer = db.Column(db.Boolean, default=False)
    vat_number = db.Column(db.String(20))
    is_verified = db.Column(db.Boolean, default=False)
    company_name = db.Column(db.String(128))
    company_address = db.Column(db.String(256))
    company_size = db.Column(db.String(20))
    profile = db.relationship('Profile', backref='user', uselist=False)
    jobs = db.relationship('Job', backref='employer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(128), nullable=False)
    salary_min = db.Column(db.Integer, nullable=False)
    salary_max = db.Column(db.Integer, nullable=False)
    company_size = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    employer_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    applications = db.relationship('Application', backref='job', lazy='dynamic')

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, ForeignKey('job.id'), nullable=False)
    cover_letter = db.Column(db.Text, nullable=False)
    resume = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(128))
    location = db.Column(db.String(128))
    bio = db.Column(db.Text)
    skills = db.Column(db.String(256))
    desired_salary = db.Column(db.Integer)
    preferred_company_size = db.Column(db.String(20))

def get_job_recommendations(user):
    if not user.profile:
        return []

    user_profile = f"{user.profile.skills} {user.profile.location} {user.profile.preferred_company_size}"
    jobs = Job.query.all()
    job_descriptions = [f"{job.title} {job.description} {job.location} {job.company_size}" for job in jobs]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user_profile] + job_descriptions)

    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    job_similarity_pairs = list(zip(jobs, cosine_similarities))
    job_similarity_pairs.sort(key=lambda x: x[1], reverse=True)

    return job_similarity_pairs[:5]  # Return top 5 recommendations

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
