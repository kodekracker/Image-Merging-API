#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import settings
from flask import Flask
from flask import request
from flask import session
from flask import g
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template
from flask import flash
from flask import make_response
from flask import jsonify
from flask import send_from_directory
from merger import Merger

app = Flask(__name__)
app.config.from_object(settings)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/v1.0/merge', methods=['OPTIONS','POST'])
def merge():
    try:
        if request.method == 'OPTIONS':
            return make_response(jsonify({"Allow":"POST"}), 200)

        if not request.json or not 'foreground_url' in request.json or not 'background_url' in request.json:
            abort(400)

        foreground_url = request.json['foreground_url']
        background_url = request.json['background_url']
        m = Merger(foreground_url, background_url)
        m.merge_images()
        response = {
            'image_name': m.get_output_image('name'),
            'image_url' : url_for('get_image', image_name = m.get_output_image('name'),_external=True),
            'image_base64' : m.get_output_image('base64')
        }
        return jsonify(response), 201
    except Exception as e:
        return make_response(jsonify({'Error': e.message}), 200)

@app.route('/image/<string:image_name>', methods=['GET'])
def get_image(image_name):
    return send_from_directory(app.config['OUTPUT_IMAGES_FOLDER'], image_name, as_attachment=True)

@app.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'Error': 'Internal Server Error'}), 500)

@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({'Error': 'Method Not Allowed'}), 405)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'Error': 'Bad Request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()
