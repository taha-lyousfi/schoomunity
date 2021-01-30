# Purpose: Define models and relevant functions for the database with SQLAlchemy

from flask_bcrypt import Bcrypt
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(260), nullable=True)
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(200), nullable=False)
    posts = db.relationship('Post', backref='users', lazy=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    def __init__(self, data):
        self.username = data.get('username')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.bio = data.get('bio')
        self.profile_picture = data.get('profile_picture')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'bio': self.bio,
            'profile_picture': self.profile_picture,
            'creation_date': self.created_at,
            'posts': [post.serialize for post in self.posts]
        }

    @property
    def serializeable(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'bio': self.bio,
            'profile_picture': self.profile_picture,
            'creation_date': self.created_at,
            'posts': [post.serialize for post in self.posts]
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.__generate_hash(item)
            else:
                try:
                    setattr(self, key, item)
                except:
                    pass
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __generate_hash(self, password):
        if not password:
            print('Woooow')
        else:
            return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_one_user(id):
        return User.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer)
    contents = db.Column(db.Text)
    media = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.contents = data.get('contents')
        self.media = data.get('media')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()
        self.likes = 0

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            try:
                setattr(self, key, item)
            except:
                pass
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        de.session.commit()

    def like(self):
        self.likes += 1

    @staticmethod
    def get_all_blogposts():
        return Post.query.all()

    @staticmethod
    def get_one_blogpost(id):
        return Post.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'owner': User.query.filter_by(id=self.user_id).username,
            'media': self.media,
            'content': self.contents,
            'creation_date': self.created_at,
            'is_modified': self.created_at != self.modified_at,
            'likes_number': self.likes
        }
