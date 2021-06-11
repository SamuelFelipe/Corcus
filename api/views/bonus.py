#!/usr/bin/python3

from flask import request, abort, g
import models
from models.bonus import Bonus
from api import auth
from api.views import app_views
from flask import jsonify
from flasgger.utils import swag_from


@app_views.route('/bonuses', methods=['GET'], strict_slashes=False)
@swag_from('documentation/aplication/all_bonuses.yml')
@auth.login_required
def get_all_bonuses():
    ret = {}
    for employee in g.user.company.employees:
        for bonus in employee.bonus:
            ret[employee.id] = bonus.to_dict()
    return jsonify(ret)


@app_views.route('/<employee_id>/bonuses', methods=['GET'], strict_slashes=False)
@swag_from('documentation/aplication/all_employee_bonus.yml')
@auth.login_required
def get_employee_bonuses(employee_id):
    ret = {}
    for employee in g.user.company.employees:
        if employee.id == employee_id:
            ret[employee.id] = employee.bonus
            return jsonify(ret)
    abort(404, description='No Valid dni')


@app_views.route('/<employee_id>/bonuses', methods=['POST'], strict_slashes=False)
@swag_from('documentation/aplication/create_bonuses.yml')
@auth.login_required
def create_bonus(employee_id):
    if not request.get_json():
        abort(400, description="Not a JSON")
    type = request.json.get('type')
    description = request.json.get('description')
    value = request.json.get('value')
    for employee in g.user.company.employees:
        if employee.id == employee_id:
            new = Bonus(type=type, description=description,
                       value=value, employee_id=employee.id)
            new.save()
            return jsonify({ 'success': new.to_dict() }), 201
    abort(404)


@app_views.route('/<employee_id>/bonuses', methods=['DELETE'], strict_slashes=False)
@swag_from('/documentation/aplication/delete_bonus.yml')
@auth.login_required
def remove_bonus(employee_id):
    if not request.get_json():
        abort(400, description="Not a JSON")
    bonus_id = request.json.get('bonus_id')
    if not bonus_id:
        abort(400, description='Missing bonus_id')
    employees = g.user.company.employees
    for employee in employees.values():
        if employee.id == employee_id:
            bonuses = employee.bonus
            for bonus in bonuses:
                if bonus.id == bonus_id:
                    models.storage.delete(bonus)
                    return jsonify({ 'success': True }), 200
            abort(400)
    abort(400)


@app_views.route('/<employee_id>/bonuses', methods=['PUT'], strict_slashes=False)
@swag_from('/documentation/aplication/delete_bonus.yml')
@auth.login_required
def update_bonus(employee_id):
    if not request.get_json():
        abort(400, description="Not a JSON")
    bonus_id = request.json.get('bonus_id')
    data = request.get_json()
    if not bonus_id:
        abort(400, description='Missing item_id')
    employees = g.user.company.employees
    for employee in employees.values():
        if employee.id == employee_id:
            for item in employee.item:
                if bonus.id == bonus_id:
                    for key, value in data.items():
                        if key not in ['id', 'created_at', 'updated_at']:
                            setattr(item, key, value)
                    models.storage.save()
                return jsonify({ 'updated': employee.to_dict() }), 200
            abort(404)
    abort(404)
