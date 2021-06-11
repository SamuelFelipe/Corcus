#!/usr/bin/python3

from flask import request, abort
import models
from api.views import app_views
from flask import jsonify
from flasgger.utils import swag_from


@app_views.route('/signup', methods=['POST'], strict_slashes=False)
@swag_from('documentation/authentication/create_account.yml')
def new_user():
    from models.admin import Admin
    from models.company import Company
    username = request.json.get('username')
    password = request.json.get('password')
    company_name = request.json.get('company')
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
                    'auth_token': 'http://corvus.com/api/token'}), 201
