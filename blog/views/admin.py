# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, flash, redirect, url_for
from ..models import Article
from ..forms import BaseArticle
from .. import db

admin = Blueprint('admin', __name__)


@admin.route('/post/', methods=['GET', 'POST'])
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
