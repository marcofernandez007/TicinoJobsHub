from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

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

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    location = db.Column(db.String(120))
    salary = db.Column(db.String(64))
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
