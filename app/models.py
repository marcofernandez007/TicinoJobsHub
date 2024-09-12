from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_employer = db.Column(db.Boolean, default=False)
    profile = db.relationship('Profile', backref='user', uselist=False)
    jobs = db.relationship('Job', backref='employer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    full_name = db.Column(db.String(120))
    location = db.Column(db.String(120))
    bio = db.Column(db.Text)
    skills = db.Column(db.String(500))
    desired_salary = db.Column(db.Integer)
    preferred_company_size = db.Column(db.String(20))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    location = db.Column(db.String(120))
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    company_size = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    applications = db.relationship('Application', backref='job', lazy='dynamic')

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    applicant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

def get_job_recommendations(user):
    if not user.profile:
        return []

    user_profile = user.profile
    all_jobs = Job.query.all()
    
    # Calculate similarity scores for each job
    job_scores = []
    for job in all_jobs:
        score = 0
        
        # Location matching (weighted more heavily)
        if user_profile.location.lower() in job.location.lower():
            score += 2.5
        
        # Salary range matching
        if user_profile.desired_salary:
            if job.salary_min <= user_profile.desired_salary <= job.salary_max:
                score += 2
            elif abs(user_profile.desired_salary - job.salary_min) <= 5000 or abs(user_profile.desired_salary - job.salary_max) <= 5000:
                score += 1  # Add some score for near matches
        
        # Company size matching
        if user_profile.preferred_company_size == job.company_size:
            score += 1.5
        elif user_profile.preferred_company_size in ['1-10', '11-50'] and job.company_size in ['1-10', '11-50']:
            score += 0.75  # Add some score for similar company sizes
        elif user_profile.preferred_company_size in ['51-200', '201-500', '501+'] and job.company_size in ['51-200', '201-500', '501+']:
            score += 0.75
        
        # Skills matching using TF-IDF and cosine similarity
        if user_profile.skills and job.description:
            tfidf = TfidfVectorizer(stop_words='english')
            user_skills = user_profile.skills.lower()
            job_description = job.title.lower() + " " + job.description.lower()  # Include job title in the comparison
            tfidf_matrix = tfidf.fit_transform([user_skills, job_description])
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            score += cosine_sim * 4  # Weight skills matching more heavily
        
        # Recency bonus (favor more recent job postings)
        days_old = (datetime.utcnow() - job.created_at).days
        recency_score = max(0, 1 - (days_old / 30))  # Full score for jobs less than a month old, decreasing linearly
        score += recency_score
        
        job_scores.append((job, score))
    
    # Normalize scores
    max_score = max(score for _, score in job_scores) if job_scores else 1
    normalized_scores = [(job, score / max_score * 10) for job, score in job_scores]
    
    # Sort jobs by normalized score in descending order and return top 10
    recommended_jobs = sorted(normalized_scores, key=lambda x: x[1], reverse=True)[:10]
    return [(job, round(score, 2)) for job, score in recommended_jobs]
