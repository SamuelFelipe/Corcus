#!/usr/bin/python3

from flask import request, abort, g
import models
from models.employee import Employee
from api import auth
from api import auth
from api.views import app_views
from flask import jsonify
from flasgger.utils import swag_from


@app_views.route('/employees', methods=['GET'], strict_slashes=False)
@swag_from('documentation/aplication/all_employees.yml')
@auth.login_required
def get_employees():
    ret = {}
    for employee in g.user.company.employees:
        ret[employee.id] = employee.to_dict()
        ret[employee.id]['items_count'] = 0
        ret[employee.id]['items_bonus'] = 0
        if employee.item:
            ret[employee.id]['items'] = [item.to_dict()
                                         for item in employee.item]    
            ret[employee.id]['items_count'] = len(ret[employee.id]['items'])
        if employee.bonus:
            ret[employee.id]['bonus'] = [bonus.to_dict()
                                         for bonus in employee.bonus]    
            ret[employee.id]['bonus_count'] = len(ret[employee.id]['bonus'])
    return jsonify(ret)


@app_views.route('/employees/<employee_id>',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/aplication/employee.yml')
@auth.login_required
def get_employee(employee_id):
    ret = {}
    for employee in g.user.company.employees:
        if employee.id == employee_id:
            ret[employee.id]['items_count'] = 0
            if employee.item:
                ret[employee.id]['items'] = [item.to_dict()
                                             for item in employee.item]    
                ret[employee.id]['items_count'] = len(ret[employee.id]['items'])
        if employee.bonus:
            ret[employee.id]['bonus'] = [item.to_dict()
                                         for item in employee.item]    
            ret[employee.id]['bonus_count'] = len(ret[employee.id]['bonus'])
        return jsonify(ret)
    abort(404)


@app_views.route('/employees', methods=['POST'], strict_slashes=False)
@swag_from('documentation/aplication/create_employee.yml')
@auth.login_required
def create_employee():
    if not request.get_json():
        abort(400, description="Not a JSON")
    dni = request.json.get('dni')
    names = request.json.get('names')
    forenames = request.json.get('forenames')
    position = request.json.get('position')
    c_type = request.json.get('contract_type')
    risk = request.json.get('risk')
    base_salary = request.json.get('base_salary')
    if not names or not dni:
        abort(400)
    elif not forenames:
        abort(400)
    elif not c_type:
        abort(400)
    new = Employee(id=dni, names=names, forenames=forenames, position=position,
                   c_type=c_type, risk=risk, base_salary=base_salary,
                   company=g.user.company.id)
    new.save()
    response = '{} {} is a new {} at {}!'.format(new.names, new.forenames,
                                                 new.position,
                                                 g.user.company.name)
    return jsonify({ 'success': response }), 201


@app_views.route('/employees', methods=['DELETE'], strict_slashes=False)
@swag_from('/documentation/aplication/delete_employee.yml')
@auth.login_required
def remove_employee():
    if not request.get_json():
        abort(400, description="Not a JSON")
    dni = request.json.get('dni')
    if not dni:
        abort(400, description='Missing dni')
    employees = g.user.company.employees
    for employee in employees.values():
        if employee.id == dni:
            models.storage.delete(employee)
            models.storage.save()
            return jsonify({ 'success': True }), 200
    abort(400, description='Invalid dni')


@app_views.route('/employees', methods=['PUT'], strict_slashes=False)
@swag_from('/documentation/aplication/delete_employee.yml')
@auth.login_required
def update_employee():
    if not request.get_json():
        abort(400, description="Not a JSON")
    dni = request.json.get('dni')
    data = request.get_json()
    if not dni:
        abort(400, description='Missing dni')
    employees = g.user.company.employees
    for employee in employees.values():
        if employee.id == dni:
            for key, value in data.items():
                if key not in ['created_at', 'updated_at']:
                    setattr(employee, key, value)
            models.storage.save()
            return jsonify({ 'updated': employee.to_dict() }), 200

    abort(400, description='No User Match')
