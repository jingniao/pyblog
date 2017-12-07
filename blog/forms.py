from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField

# from wtforms.validators import DataRequired, Length


class BaseArticle(FlaskForm):
    title = StringField('title')
    content = TextAreaField('content')
