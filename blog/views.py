# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for
# from flask_login import login_required, current_user

from . import app, db
from .models import User, Article
from .forms import BaseArticle


@app.route('/')
def index():
    # db.session.
    art_list = Article.query.all()
    return render_template('index.html', art_list=art_list)


@app.route('/post/', methods=['GET', 'POST'])
def post_article():
    form = BaseArticle()
    if form.validate_on_submit():
        article = Article(title=form.title.data, content=form.content.data)
        db.session.add(article)
        db.session.commit()
        flash(u'文章 <{0}> 添加'.format(form.title.data))
        return redirect(url_for('index'))
    else:
        return render_template('post.html', form=form)
