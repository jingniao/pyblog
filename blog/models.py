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
        return unicode(self.uid)

    def to_json(self):
        return {'uid': self.uid, 'username': self.username}

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
    create_time = db.Column(db.TIMESTAMP, nullable=False)
    update_time = db.Column(db.TIMESTAMP, onupdate=nowtime)

    def to_json(self, ret_comments=False):
        ret = {
            'aid': self.aid,
            'username': self.user.username,
            'title': self.title,
            'content': self.content,
            # 'comments': [item.to_json() for item in self.comments.all()],
            'create_time': str(self.create_time)
        }
        if ret_comments:
            ret['comments'] = [item.to_json() for item in self.comments.all()]
        return ret


class Comment(db.Model):
    cid = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.aid'))
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.TIMESTAMP, nullable=False)

    def to_json(self):
        return {
            'cid': self.cid,
            'user': self.user.username,
            'aid': self.article_id,
            'content': self.content,
            'create_time': str(self.create_time)
        }
