# -*- coding: utf-8 -*-
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, logout_user

from .. import db
from ..forms import BaseArticle, BaseLogin
from ..models import Article, User

admin = Blueprint('admin', __name__)


@admin.route('/post_article/', methods=['GET', 'POST'])
def post_article():
    form = BaseArticle()
    if form.validate_on_submit():
        article = Article(title=form.title.data, content=form.content.data)
        db.session.add(article)
        db.session.commit()
        flash(u'文章 <{0}> 添加'.format(form.title.data))
        return redirect(url_for('home.index'))
    else:
        return render_template('post.html', form=form)


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = BaseLogin()
    if not form.validate_on_submit():
        return render_template('login.html', form=form)
    else:
        user_one = User.query.filter_by(username=form.username.data).first()
        if not user_one:
            form.username.errors.append(u'未找到用户')
            return render_template('login.html', form=form)
        elif user_one.password != form.password.data:
            form.password.errors.append(u'密码错误')
            return render_template('login.html', form=form)
        else:
            login_user(user_one)
            flash(u'你已经登陆')
            return redirect(url_for('home.index'))


@admin.route('/logout/')
def logout():
    logout_user()
    flash(u'已经登出')
    return redirect(url_for('home.index'))
