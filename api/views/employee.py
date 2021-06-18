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
        ret[employee.id]['bonus_count'] = 0
        if employee.item:
            ret[employee.id]['items'] = [item.to_dict()
                                         for item in employee.item]    
            ret[employee.id]['items_count'] = len(ret[employee.id]['items'])
        if employee.bonus:
            ret[employee.id]['bonus'] = [bonus.to_dict()
                                         for bonus in employee.bonus]    
            ret[employee.id]['bonus_count'] = len(ret[employee.id]['bonus'])
        ret[employee.id]['arl'] = employee.arl()
        ret[employee.id]['health'] = employee.health()
        ret[employee.id]['pension'] = employee.pension()
        ret[employee.id]['sub_trans'] = employee.sub_trans()
        ret[employee.id]['parafiscales'] = employee.para_f()
        ret[employee.id]['salary'] = employee.salary()
        ret[employee.id]['vacations'] = employee.vacations()
        ret[employee.id]['cesantias'] = employee.cesantias()
        ret[employee.id]['in_cesantias'] = employee.in_cesantias()
    return jsonify(ret)


@app_views.route('/employees/<employee_id>',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/aplication/employee.yml')
@auth.login_required
def get_employee(employee_id):
    ret = {}
    for employee in g.user.company.employees:
        if employee.id == employee_id:
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
            ret[employee.id]['arl'] = employee.arl()
            ret[employee.id]['health'] = employee.health()
            ret[employee.id]['pension'] = employee.pension()
            ret[employee.id]['parafiscales'] = employee.para_f()
            ret[employee.id]['sub_trans'] = employee.sub_trans()
            ret[employee.id]['salary'] = employee.salary()
            ret[employee.id]['vacations'] = employee.vacations()
            ret[employee.id]['cesantias'] = employee.cesantias()
            ret[employee.id]['in_cesantias'] = employee.in_cesantias()
        return jsonify(ret)
    abort(404)


@app_views.route('/employees', methods=['POST'], strict_slashes=False)
@swag_from('documentation/aplication/create_employee.yml')
@auth.login_required
def create_employee():
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    dni = request.json.get('id')
    names = request.json.get('names')
    forenames = request.json.get('forenames')
    position = request.json.get('position')
    eps = request.json.get('eps')
    c_type = request.json.get('c_type')
    no_acount = request.json.get('no_acount')
    if not names or not dni or not no_acount:
        abort(400)
    elif not forenames or not eps or not position:
        abort(400)
    elif c_type not in ['Termino Indefinido',
                        'Obra Labor', 'Prestacion de Servicios']:
        abort(400)
    if c_type == 'Obra Labor':
        data['base_salary'] = 0

    for key in data.keys():
        if key == 'company':
            del data['company']

    new = Employee(**data, company=g.user.company.id)
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
