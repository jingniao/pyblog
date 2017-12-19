# -*- coding: utf-8 -*-
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from ..exts import db
from ..forms import BaseComment
from ..models import Article, Comment

home = Blueprint('home', __name__)


@home.route('/')
@home.route('/page/<int:page>')
def index(page=1):
    art_list = Article.query.paginate(page, 3, True)
    return render_template('index.html', art_list=art_list)


@home.route('/article_detail/<int:aid>/')
@home.route('/article_detail/<int:aid>/page/<int:page>')
def article_detail(aid, page=1):
    art_detail = Article.query.filter_by(aid=aid).first()
    if art_detail:
        comment_list = art_detail.comments.paginate(page, 3, True)
        form = BaseComment()
        return render_template(
            'article_detail.html',
            article=art_detail,
            form=form,
            comment_list=comment_list)


@home.route("/post_comment/", methods=['POST'])
@login_required
def post_comment():
    form = BaseComment()
    if form.validate_on_submit():
        aid = form.aid.data
        art_detail = Article.query.filter_by(aid=aid).first()
        if art_detail:
            comment_one = Comment(
                article_id=aid,
                user_id=current_user.uid,
                content=form.content.data)
            db.session.add(comment_one)
            db.session.commit()
            flash(u'成功添加评论')
            return redirect(url_for('home.article_detail', aid=aid))
        else:
            flash(u'未找到文章或未登陆')
            return redirect(url_for('home.index'))
