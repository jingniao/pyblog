# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, url_for, redirect, flash
from ..models import User
from ..exts import db
import time
import string
import random
test = Blueprint('test', __name__)


def randstr():
    return ''.join(random.sample(string.ascii_lowercase, 6))


@test.route('/index/')
def index():
    return render_template('test/index.html')


@test.route('/user/')
def user():
    start_time = time.time()
    for _ in range(1000):
        one_user = User(username=randstr(), password='111111')
        db.session.add(one_user)
    db.session.commit()
    flash(u'批量添加1000用户，用时{0}'.format(time.time() - start_time))
    return redirect(url_for('test.index'))
