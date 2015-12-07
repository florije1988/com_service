# -*- coding: utf-8 -*-
__author__ = 'florije'

import os
import logging
import gunicorn
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, send_from_directory
from werkzeug.contrib.fixers import ProxyFix
from redis import Redis
from flask_redis import FlaskRedis
from celery import Celery
from flask_sqlalchemy import SQLAlchemy

print gunicorn.__version__

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['REDIS_URL'] = "redis://localhost:6379/0"


# handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)  # TimedRotatingFileHandler
handler = TimedRotatingFileHandler('logs/com_service.log', when='midnight', interval=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)  # 注册

db = SQLAlchemy(app)
redis_store = FlaskRedis(app)


class BaseModel(db.Model):
    """
    Model基类
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime(), default=db.func.datetime('now', 'localtime'))  # db.func.now()
    update_time = db.Column(db.DateTime(), default=db.func.datetime('now', 'localtime'),
                            onupdate=db.func.datetime('now', 'localtime'))


class ModelMixin(object):
    """
    Model拓展类
    """
    def __repr__(self):
        return unicode(self.__dict__)


class UserModel(BaseModel, ModelMixin):
    """
    用户模型
    """
    __tablename__ = 'users'

    name = db.Column(db.String(6), unique=False, nullable=False)


@app.route('/')
def hello_world():
    res = gunicorn.__version__
    try:
        app.logger.warn('Info')
    except Exception as e:
        res = e.message
    import datetime
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')
    app.logger.warn(current_time)
    redis_store.set('name', 'fuboqing')
    res = redis_store.get('name', 'Not Set')
    if res:
        return res
    return current_time


@app.route('/users')
def get_user_list():
    return "user_list"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8010, debug=False)
