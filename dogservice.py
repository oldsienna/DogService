#!flask/bin/python
import os
import pymongo
import models
from flask import Flask, jsonify, abort, request, make_response, url_for

app = Flask(__name__)

# Error Handler for 400: Bad Request
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

# Error Handler for 404: Not Found 
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
    
# Service Call for retrieving list of dogs
@app.route('/api/v1.0/dogs', methods = ['GET'])
def get_dogs():
    dogs = models.get_dogs()
    return jsonify( { 'dogs': dogs } ), 201

# Service Call for retrieving a dog's details using id
@app.route('/api/v1.0/dog/<string:dog_id>', methods = ['GET'])
def get_dog(dog_id):
    dog = models.get_dog(dog_id)

    if not dog:
        # No dog with that id found
        abort(404)

    return jsonify( { 'dog': dog })

# Service Call for creating a new dog
@app.route('/api/v1.0/dog', methods = ['POST'])
def create_dog():
    # Check for JSON input, plus:
    # Mandatory dog name and registration_id must be unique
    if not request.json or not 'name' in request.json:
        abort(400)
    dog = {
        'registration_id': str(request.json['registration_id']).strip().upper(),
        'name': str(request.json['name']).strip().capitalize(),
        'description': request.json.get('description', ""),
        'handler_id': request.json.get('handler_id', None),
        'pedigree': str(request.json.get('pedigree', "")).strip().lower(),
        'reg_status': request.json.get('reg_status', False),
        'vacc_status': request.json.get('vacc_status', False)
    }
    id = models.new_dog(dog)
    dog['id'] = id

    return jsonify( { 'dog': dog } ), 201

# Service Call for updating a dog
@app.route('/api/v1.0/dog/<string:dog_id>', methods = ['PUT'])
def update_dog(dog_id):
    dog = models.get_dog(dog_id)
    if len(dog) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'registration_id' in request.json and type(request.json['registration_id']) is not unicode:
        abort(400)
    if 'handler_id' in request.json and type(request.json['handler_id']) is not int:
        abort(400)
    if 'reg_status' in request.json and type(request.json['reg_status']) is not bool:
        abort(400)
    if 'vacc_status' in request.json and type(request.json['vacc_status']) is not bool:
        abort(400)
    if 'pedigree' in request.json and type(request.json['pedigree']) is not unicode:
        abort(400)
    dog['name'] = str(request.json.get('name', dog['name'])).strip().capitalize()
    dog['registration_id'] = str(request.json.get('registration_id', dog['registration_id'])).strip().upper()
    dog['description'] = request.json.get('description', dog['description'])
    dog['handler_id'] = request.json.get('handler_id', dog['handler_id'])
    dog['reg_status'] = request.json.get('reg_status', dog['reg_status'])
    dog['vacc_status'] = request.json.get('vacc_status', dog['vacc_status'])
    dog['pedigree'] = str(request.json.get('pedigree', dog['pedigree'])).strip().lower()
    models.update_dog(dog)

    return jsonify( { 'dog': dog } )

# Service Call for deleting a dog
@app.route('/api/v1.0/dog/<string:dog_id>', methods = ['DELETE'])
def delete_dog(dog_id):
    dog = models.get_dog(dog_id)
    if dog is None:
        abort(404)
    models.delete_dog(dog_id)
    return jsonify( { 'result': True } )

# Service Call for finding handlers by criteria (similar to Update Handler method)
# Accepts a single field or multiple fields which are then AND'ed
@app.route('/api/v1.0/search', methods = ['PUT'])
def search():
    if not request.json:
        abort(400)
    if 'reg_status' in request.json and type(request.json['reg_status']) is not bool:
        abort(400)
    if 'vacc_status' in request.json and type(request.json['vacc_status']) is not bool:
        abort(400)
    criteria = {}

    if 'registration_id' in request.json:
        registration_id = str(request.json['registration_id']).strip()
        criteria['registration_id'] = registration_id

    if 'name' in request.json:
        name = str(request.json['name']).strip().capitalize()
        criteria['name'] = name

    if 'handler_id' in request.json:
        handler_id = request.json['handler_id']
        if not (handler_id is None):
            str(handler_id).strip()
        criteria['handler_id'] = handler_id

    if 'reg_status' in request.json:
        criteria['reg_status'] = request.json['reg_status']

    if 'vacc_status' in request.json:
        criteria['vacc_status'] = request.json['vacc_status']

    dogs = models.search(criteria)
    return jsonify( {'dogs': dogs} )

# Initialise DB before starting web service
models.init_db()
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv('PORT', '5000')), threaded=True)
