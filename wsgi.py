import flask
from flask import request, jsonify
import sqlite3
import os
port = int(os.environ.get('PORT', 5000))

app = flask.Flask(__name__)


@app.route('/')
def home():
    return "<h1>Hello World !!!</h1>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
