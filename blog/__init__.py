# -*- coding: utf-8 -*-
from flask import Flask

from .exts import db
# from .views import

app = Flask(__name__, instance_relative_config=True)
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
from blog import views, models
