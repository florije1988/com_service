# -*- coding: utf-8 -*-
__author__ = 'florije'

import os
from flask import Flask, send_from_directory
from redis import Redis
from celery import Celery
import gunicorn

print gunicorn.__version__

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010, debug=False)
