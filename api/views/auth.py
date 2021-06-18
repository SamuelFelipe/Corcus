#!/usr/bin/python3

from flask import request, abort
import models
from api.views import app_views
from api import auth
from flask import jsonify
from flasgger.utils import swag_from


@app_views.route('/signup', methods=['POST'], strict_slashes=False)
@swag_from('documentation/authentication/create_account.yml')
def new_user():
    from models.admin import Admin
    from models.company import Company
    if request.get_json():
        username = request.json.get('username')
        password = request.json.get('password')
        company_name = request.json.get('company')
    elif request.form:
        username = request.form['username']
        password = request.form['password']
        company_name = request.form['company']
    else:
        abort(400)
    if username is None or password is None or company_name is None:
        abort(400) # missing arguments
    for user in models.storage.all(Admin).values():
        if user.username == username:
            abort(400) # existing user
    for comp in models.storage.all(Company).values():
        if comp.name == company_name:
            abort(400) # existing company
    company = Company(name=company_name)
    company.save()
    user = Admin(username=username, company=company)
    user.hash_password(password)
    user.save()
    return jsonify({'user': user.username, 'company': company.name,
        'next_token': 'http://127.0.0.1:5000/api/token',
                    'auth_token': user.generate_auth_token().decode('ascii')}), 201


@app_views.route("auth_status")
@auth.login_required
def auth_status():
    return jsonify({'token_status':'alive'})
