import os
import random

from flask import Flask, send_from_directory

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello to the Catto Web API!"


@app.route('/api/random_catto')
def random_catto():
    return {'file_name': random.choice(os.listdir('images'))}


@app.route('/api/get/<path:file_name>')
def get_image(file_name):
    return send_from_directory('images', file_name)


@app.errorhandler(404)
def invalid_route(e):
    return "404 catto!"
