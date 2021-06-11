#!/usr/bin/python3

from flask import request, abort, g
import models
from models.employee import Employee
from models.item import Item
from api import auth
from api import auth
from api.views import app_views
from flask import jsonify
from flasgger.utils import swag_from


@app_views.route('/items', methods=['GET'], strict_slashes=False)
@swag_from('documentation/aplication/all_items.yml')
@auth.login_required
def get_all_items():
    ret = {}
    for employee in g.user.company.employees:
        for item in employee.item:
            ret[employee.id] = item.to_dict()
    return jsonify(ret)


@app_views.route('/<employee_id>/items', methods=['GET'], strict_slashes=False)
@swag_from('documentation/aplication/all_employee_items.yml')
@auth.login_required
def get_employee_items(employee_id):
    ret = {}
    for employee in g.user.company.employees:
        if employee.id == employee_id:
            ret[employee.id] = employee.item
            return jsonify(ret)
    abort(404, description='No Valid dni')


@app_views.route('/<employee_id>/items', methods=['POST'], strict_slashes=False)
@swag_from('documentation/aplication/create_item.yml')
@auth.login_required
def create_item(employee_id):
    if not request.get_json():
        abort(400, description="Not a JSON")
    name = request.json.get('name')
    description = request.json.get('description')
    u_value = request.json.get('unit_value')
    for employee in g.user.company.employees:
        if employee.id == employee_id:
            new = Item(name=name, description=description,
                       unitary_value=u_value, employee_id=employee.id)
            new.save()
            return jsonify({ 'success': new.to_dict() }), 201
    abort(404)


@app_views.route('/<employee_id>/items', methods=['DELETE'], strict_slashes=False)
@swag_from('/documentation/aplication/delete_item.yml')
@auth.login_required
def remove_item(employee_id):
    if not request.get_json():
        abort(400, description="Not a JSON")
    item_id = request.json.get('item_id')
    if not item_id:
        abort(400, description='Missing item_id')
    employees = g.user.company.employees
    for employee in employees.values():
        if employee.id == employee_id:
            items = employee.item
            for item in items:
                if item.id == item_id:
                    models.storage.delete(item)
                    return jsonify({ 'success': True }), 200
            abort(400, description='Invalid item')
    abort(400, description='Invalid dni')


@app_views.route('/<employee_id>/items', methods=['PUT'], strict_slashes=False)
@swag_from('/documentation/aplication/delete_item.yml')
@auth.login_required
def update_item(employee_id):
    if not request.get_json():
        abort(400, description="Not a JSON")
    item_id = request.json.get('item_id')
    data = request.get_json()
    if not item_id:
        abort(400, description='Missing item_id')
    employees = g.user.company.employees
    for employee in employees.values():
        if employee.id == employee_id:
            for item in employee.item:
                if item.id == item_id:
                    for key, value in data.items():
                        if key not in ['id', 'created_at', 'updated_at']:
                            setattr(item, key, value)
                    models.storage.save()
                return jsonify({ 'updated': employee.to_dict() }), 200
            abort(404, description='Invalid item')
    abort(404, description='Invalid dni')
