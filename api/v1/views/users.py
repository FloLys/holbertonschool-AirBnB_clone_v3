#!/usr/bin/python3
""" Handles RESTful API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ Returns all objects """
    all_objs = []
    objs = storage.all(User)
    for obj in objs.values():
        all_objs.append(obj.to_dict())
    return jsonify(all_objs)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_users():
    """ Handles POST request. Creates a new entry with status 201, else 400 """
    body_req = request.get_json(force=True, silent=True)
    if body_req is None:
        abort(400, "Not a JSON")
    if 'name' not in body_req:
        abort(400, "Missing name")
    new_user = User(**request.get_json())
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users(user_id):
    """ Handles GET request. Returns the obj to dictionary else raise 404 """
    obj = storage.get(User, user_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_users(user_id):
    """ Handles DELETE request. Returns empty dictionary else raise 404 err """
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_users(user_id):
    """ Handles PUT request. Updates the obj with status 200, else 400 """
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    obj = storage.get(User, user_id)
    new_attr = request.get_json(force=True, silent=True)
    if not obj:
        abort(404)
    if new_attr is None:
        abort(400, "Not a JSON")
    else:
        for key, value in new_attr.items():
            if key in ignore_keys:
                continue
            setattr(obj, key, value)
        storage.save()
        return jsonify(obj.to_dict()), 200
