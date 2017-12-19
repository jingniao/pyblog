# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager

from .exts import db
from .models import User
from .views.background import background
from .views.home import home
from .views.test import test

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(home)
app.register_blueprint(background, url_prefix='/background')
app.register_blueprint(test, url_prefix='/test')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "background.login"
# 未登陆会闪现下面一条
login_manager.login_message = u'您未登陆，请先登陆后再操作'
# 如果需要自定义未登录返回，需要将处理函数用 LoginManager.unauthorized_handler装饰


@login_manager.user_loader
def load_user(userid):
    try:
        return User.query.filter(User.uid == int(userid)).first()
    except ValueError:
        return None


app.config.from_object('config')
app.config.from_pyfile('config.py')
try:
    app.config.from_envvar('APP_CONFIG_FILE')
except Exception:
    pass
db.init_app(app)

# db.create_all()
# db = SQLAlchemy(app)
# 在这里导入，会运行这两个文件，这样就将views以及models注册到了app，否则app找不到这些内容
# from blog import views, models
