#!/usr/bin/python3
""" Status of our API """
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
HOST = getenv('HBNB_API_HOST', '0.0.0.0')
PORT = getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def teardown_storage(self):
    """ closes sessions of storage if exists """
    if storage is not None:
        storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ Page Not Found """
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, threaded=True, debug=True)
