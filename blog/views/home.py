# -*- coding: utf-8 -*-
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from flask_restful import Api, Resource, reqparse

from ..exts import db
from ..forms import BaseComment, BaseArticle
from ..models import Article, Comment

home = Blueprint('home', __name__)

api = Api(home, prefix='/api')
get_parser = reqparse.RequestParser()
get_parser.add_argument('page', type=int, required=False)
get_parser.add_argument('per_page', type=int, required=False)


@home.route('/')
@home.route('/page/<int:page>')
def index(page=1):
    art_list = Article.query.paginate(page, 3, True)
    return render_template('index.html', art_list=art_list)


# class HomeList(Resource):
#     def get(self, page=1):
#         art_list = Article.query.paginate(page, 3, True).items
#         art_list = [item.to_json() for item in art_list]

#         return {'page': page, 'art_list': art_list}


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


@home.route('/post_article/', methods=['GET', 'POST'])
@login_required
def post_article():
    form = BaseArticle()
    if form.validate_on_submit():
        article = Article(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.uid)
        db.session.add(article)
        db.session.commit()
        flash(u'文章 <{0}> 添加'.format(form.title.data))
        return redirect(url_for('home.index'))
    else:
        return render_template('post.html', form=form)


class ArticleInfo(Resource):
    def get(self):
        args = get_parser.parse_args()
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        art_list = Article.query.paginate(page, per_page, True)
        total = art_list.total
        pages = art_list.pages
        art_list = [item.to_json() for item in art_list.items]
        res = {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': pages,
            'art_list': art_list
        }
        return res

    @login_required
    def post(self):
        pass


class CommentList(Resource):
    def get(self, aid, page=1):
        comment_list = Comment.query.filter_by(article_id=aid).paginate(
            page, 3, False).items
        comment_list = [item.to_json() for item in comment_list]
        return comment_list

    def post(self, aid):
        pass


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


# api.add_resource(HomeList, '/index/')
api.add_resource(ArticleInfo, '/article/')
api.add_resource(CommentList, '/comments/<int:aid>/')
