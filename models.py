from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from __init__ import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

# Define the link table for the many-to-many relationship between communities and users
membership_table = Table('community_member_link', db.Model.metadata,
    Column('community_id', Integer, ForeignKey('community.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    bio = db.Column(db.Text(), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    # Relationship to associate communities with posts
    posts = db.relationship('Post', backref='community', lazy=True)
    # Relationship to associate communities with members (users)
    members = db.relationship('User', secondary=membership_table, backref='communities')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    # Foreign key for the user who authored the post
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Relationship to associate posts with authors (users)
    author = db.relationship('User', backref='posts')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

def init_db():
    db.create_all()

if __name__ == '__main__':
    #db.drop_all()
    init_db()
