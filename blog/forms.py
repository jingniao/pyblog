# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, HiddenField, PasswordField
from wtforms.validators import DataRequired, Length


class BaseArticle(FlaskForm):
    title = StringField('title')
    content = TextAreaField('content')


class BaseComment(FlaskForm):
    content = TextAreaField('content')
    aid = HiddenField('aid')


class BaseLogin(FlaskForm):
    username = StringField(
        'username',
        validators=[
            DataRequired(message=u"用户名不能为空"),
            Length(6, 20, message=u'长度位于6~20之间')
        ],
        render_kw={
            'placeholder': u'输入用户名'
        })
    password = PasswordField(
        'password',
        validators=[
            DataRequired(message=u"密码不能为空"),
            Length(6, 20, message=u'长度位于6~20之间')
        ],
        render_kw={
            'placeholder': u'输入密码'
        })
