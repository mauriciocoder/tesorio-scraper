from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from model.shared_model import db

RepositoryUser = db.Table('repository_user',
                          db.Column('repository_id', db.Integer, db.ForeignKey('repository.id')),
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')))


class Repository(db.Model, SerializerMixin):
    __tablename__ = 'repository'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(80), unique=False, nullable=True)
    description = db.Column(db.String(200), unique=False, nullable=True)
    language = db.Column(db.String(80), unique=False, nullable=True)
    html_url = db.Column(db.String(80), unique=False, nullable=True)
    forks = db.Column(db.Integer, unique=False, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    contributors = db.relationship('User', secondary=RepositoryUser, backref='Repository')

    def __repr__(self):
        return '<Repository %r>' % self.name


class User(db.Model, SerializerMixin):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=True)
    company = db.Column(db.String(80), unique=True, nullable=True)
    bio = db.Column(db.String(80), unique=True, nullable=True)
    location = db.Column(db.String(80), unique=True, nullable=True)
    html_url = db.Column(db.String(80), unique=True, nullable=True)
    public_repos = db.Column(db.String(80), unique=True, nullable=True)
    public_gists = db.Column(db.String(80), unique=True, nullable=True)
    followers = db.Column(db.String(80), unique=True, nullable=True)
    following = db.Column(db.String(80), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    repositories = db.relationship('Repository', secondary=RepositoryUser, backref='User')

    def __repr__(self):
        return '<User %r>' % self.login
