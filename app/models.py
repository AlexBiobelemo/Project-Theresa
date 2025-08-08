from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # This relationship links a User to all their Resumes
    resumes = db.relationship('Resume', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Store the large, structured resume data as a JSON string in a Text field
    structured_data_json = db.Column(db.Text)

    # Foreign key to link to the User who owns this resume
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # This relationship links a Resume to all its Analyses
    analyses = db.relationship('Analysis', backref='resume', lazy='dynamic', cascade="all, delete-orphan")

    # Property to easily get the structured data back as a Python dictionary
    @property
    def structured_data(self):
        return json.loads(self.structured_data_json) if self.structured_data_json else {}

    def __repr__(self):
        return f'<Resume {self.original_filename}>'


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Store the AI's analysis results as a JSON string
    analysis_data_json = db.Column(db.Text)

    # Foreign key to link to the Resume that was analyzed
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))

    @property
    def analysis_data(self):
        return json.loads(self.analysis_data_json) if self.analysis_data_json else {}

    def __repr__(self):
        return f'<Analysis for Resume {self.resume_id}>'
