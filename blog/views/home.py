# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, redirect, session, flash
from ..models import Article, Comment
from ..forms import BaseComment
from ..exts import db

home = Blueprint('home', __name__)


@home.route('/')
def index():
    # db.session.
    art_list = Article.query.all()
    return render_template('index.html', art_list=art_list)


@home.route('/article_detail/<int:aid>/')
def article_detail(aid):
    art_detail = Article.query.filter_by(aid=aid).first()
    if art_detail:
        comment_list = Comment.query.filter_by(aid=aid).all()
        form = BaseComment()
        return render_template(
            'article_detail.html',
            article=art_detail,
            form=form,
            comment_list=comment_list)


@home.route("/post_comment/", methods=['POST'])
def post_comment():
    form = BaseComment()
    if form.validate_on_submit():
        aid = form.aid.data
        art_detail = Article.query.filter_by(aid=aid).first()
        uid = session.get('uid')
        if art_detail and uid:
            comment_one = Comment(aid=aid, uid=uid, content=form.content.data)
            db.session.add(comment_one)
            db.session.commit()
            flash(u'成功添加评论')
            return redirect(url_for('home.article_detail', aid=aid))
        else:
            flash(u'未找到文章或未登陆')
            return redirect(url_for('home.index'))
