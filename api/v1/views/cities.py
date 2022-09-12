#!/usr/bin/python3
""" Handles RESTful API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def cities():
    """ Returns all objects """
    all_objs = []
    objs = storage.all(City)
    for obj in objs.values():
        all_objs.append(obj.to_dict())
    return jsonify(all_objs)


@app_views.route('/states/<state_id>/cities/', methods=['POST'], strict_slashes=False)
def post_cities(state_id):
    """ Handles POST request. Creates a new entry with status 201, else 400 """
    body_req = request.get_json(force=True, silent=True)
    if body_req is None:
        abort(400, "Not a JSON")
    if storage.get(State, state_id) is None:
        abort(404)
    if 'name' not in body_req:
        abort(400, "Missing name")
    new_city = City(**request.get_json())
    storage.new(new_city)
    storage.save()
    return jsonify(storage.get(new_city.__class__, new_city.id).to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities(city_id):
    """ Handles GET request. Returns the obj to dictionary else raise 404 """
    obj = storage.get(City, city_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    """ Handles GET request. retrieves all cities based on state_id """
    cities = []
    if storage.get(State, state_id) is None:
        abort (404)
    for obj in storage.all(City).values():
        if obj.state_id == state_id:
            cities.append(obj.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cities(city_id):
    """ Handles DELETE request. Returns empty dictionary else raise 404 err """
    obj = storage.get(City, city_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_cities(city_id):
    """ Handles PUT request. Updates the obj with status 200, else 400 """
    ignore_keys = ['id', 'created_at', 'updated_at']
    obj = storage.get(City, city_id)
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
