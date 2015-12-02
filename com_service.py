# -*- coding: utf-8 -*-
__author__ = 'florije'

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8010, debug=False)
