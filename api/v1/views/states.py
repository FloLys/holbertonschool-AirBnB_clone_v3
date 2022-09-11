#!/usr/bin/python3
""" States view for state objects handled with RESTful API actions """
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request



@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Returns all state objects """
    all_objs = []
    objs = storage.all(State)
    for obj in objs.values():
        all_objs.append(obj.to_dict())
    return jsonify(all_objs)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get(state_id):
    """ Handles GET request. Returns the obj to dictionary else raise 404 """
    objs = storage.all(State)
    for obj in objs.values():
        if obj.id == state_id:
            return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete(state_id):
    """ Handles DELETE request. Returns empty dictionary else raise 404 err """
    objs = storage.all(State)
    for obj in objs.values():
        if obj.id == state_id:
            delete
            return jsonify(obj.to_dict())
    abort(404)


