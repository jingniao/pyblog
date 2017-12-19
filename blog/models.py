# -*- coding: utf-8 -*-
import time

from flask_login import UserMixin

from .exts import db


def nowtime():
    return int(time.time())


class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    articles = db.relationship('Article', backref='user', lazy='dynamic')
    comments = db.relationship(
        'Comment',
        backref='user',
        lazy='dynamic',
        primaryjoin='User.uid==Comment.user_id')

    def get_id(self):
        return self.uid

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Article(db.Model):
    aid = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship(
        'Comment',
        backref='article',
        lazy='dynamic',
        primaryjoin='Article.aid==Comment.article_id')
    version = db.Column(db.Integer)
    update_time = db.Column(db.TIMESTAMP, onupdate=nowtime)
    create_time = db.Column(db.TIMESTAMP, nullable=False)


class Comment(db.Model):
    cid = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.aid'))
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.TIMESTAMP, nullable=False)
