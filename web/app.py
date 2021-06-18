#!/usr/bin/python3

from flask import Flask, jsonify, render_template
from flask_cors import CORS


app = Flask(__name__)

cors = CORS(app, resources={r'/*':  {'origins': '*'}})


@app.route('/', strict_slashes=False)
def landing():
    return render_template('index.html')

@app.route('/signup', strict_slashes=False)
def signup():
    return render_template('signup.html')

@app.route('/login', strict_slashes=False)
def login():
    return render_template('login.html')

@app.route('/app/employees', strict_slashes=False)
def application():
    return render_template('app.html')

@app.route('/app', strict_slashes=False)
def main_app():
    return render_template('main.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5001', threaded=True, debug=True)
