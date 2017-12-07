# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from ..models import Article

home = Blueprint('home', __name__)


@home.route('/')
def index():
    # db.session.
    art_list = Article.query.all()
    return render_template('index.html', art_list=art_list)
