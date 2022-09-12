#!/usr/bin/python3
""" Handles RESTful API actions """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def all_places_of_city():
    """ Returns all objects """
    all_objs = []
    objs = storage.all(Place)
    for obj in objs.values():
        all_objs.append(obj.to_dict())
    return jsonify(all_objs)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Handles POST request. Creates a new entry with status 201, else 400 """
    body_req = request.get_json(force=True, silent=True)
    if body_req is None:
        abort(400, "Not a JSON")
    if 'name' not in body_req:
        abort(400, "Missing name")
    new_place = Place(**request.get_json())
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Handles GET request. Returns the obj to dictionary else raise 404 """
    obj = storage.get(Place, place_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Handles DELETE request. Returns empty dictionary else raise 404 err """
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Handles PUT request. Updates the obj with status 200, else 400 """
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    obj = storage.get(Place, place_id)
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
