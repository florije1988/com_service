# -*- coding: utf-8 -*-
__author__ = 'florije'

import os
import logging
import gunicorn
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, send_from_directory
from werkzeug.contrib.fixers import ProxyFix
from redis import Redis
from celery import Celery

print gunicorn.__version__

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)  # TimedRotatingFileHandler
handler = TimedRotatingFileHandler('logs/com_service.log', when='midnight', interval=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


@app.route('/')
def hello_world():
    res = gunicorn.__version__
    try:
        app.logger.warn('Info')
    except Exception as e:
        res = e.message
    import datetime
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8010, debug=False)
