#!/usr/bin/python3

import models
from api import auth
from api.views import app_views
from flask import Flask, make_response, jsonify, g
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger


app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SECRET_KEY'] = 'AAAAB3NzaC1yc2EAAAADAQABAAABgQCyfPez'

app.register_blueprint(app_views)
cors = CORS(app, resources={r'/api/*':  {'origins': '*'}})


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    from models.admin import Admin
    user = Admin.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        users = models.storage.all(Admin)
        if not users:
            return False
        for user in users.values():
            if user.username == username_or_token:
                if user.verify_password(password):
                    g.user = user
                    return True
        return False
    g.user = user
    return True

@app.teardown_appcontext
def close_db(error):
    models.storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


app.config['SWAGGER'] = {'title': 'Corvus Restful API'}

Swagger(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True, debug=True)
