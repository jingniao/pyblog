# -*- coding: utf-8 -*-
from .exts import db
import time


def nowtime():
    return int(time.time())


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Article(db.Model):
    aid = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    version = db.Column(db.Integer)
    update_time = db.Column(db.TIMESTAMP, onupdate=nowtime)
    create_time = db.Column(db.TIMESTAMP, nullable=False)


class Comment(db.Model):
    cid = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True)
    uid = db.Column(db.Integer)
    aid = db.Column(db.Integer)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.TIMESTAMP, nullable=False)
