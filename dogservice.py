#!flask/bin/python
import os
from flask import Flask, jsonify, abort, request, make_response, url_for

app = Flask(__name__, static_url_path = "")
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

dogs = [
    {
        'id': 1,
        'registration_id': u'P1234',
        'name': u'Fido',
        'description': u'Friendly fluff ball', 
        'handler_id': 1,
        'reg_status': True,
        'vacc_status': False,
        'pedigree': u'Poodle'
    },
    {
        'id': 2,
        'registration_id': u'G2345',
        'name': u'Rexx',
        'description': u'Good guard dog', 
        'handler_id': 2,
        'reg_status': True,
        'vacc_status': True,
        'pedigree': u'German Shepard'
    }
]

def make_public_dog(dog):
    new_dog = {}
    for field in dog:
        if field == 'id':
            new_dog['uri'] = url_for('get_dog', dog_id = dog['id'], _external = True)
        else:
            new_dog[field] = dog[field]
    return new_dog
    
@app.route('/api/v1.0/dogs', methods = ['GET'])
def get_dogs():
    return jsonify( { 'dogs': map(make_public_dog, dogs) } )

@app.route('/api/v1.0/dog/<int:dog_id>', methods = ['GET'])
def get_dog(dog_id):
    dog = filter(lambda t: t['id'] == dog_id, dogs)
    if len(dog) == 0:
        abort(404)
    return jsonify( { 'dog': make_public_dog(dog[0]) } )

@app.route('/api/v1.0/dog', methods = ['POST'])
def create_dog():
    if not request.json or not 'name' in request.json:
        abort(400)
    dog = {
        'id': dogs[-1]['id'] + 1,
        'registration_id': request.json['registration_id'],
        'name': request.json['name'],
        'description': request.json.get('description', ""),
        'handler_id': request.json.get('handler_id'),
        'pedigree': request.json.get('pedigree'),
        'reg_status': False,
        'vacc_status': False
    }
    dogs.append(dog)
    return jsonify( { 'dog': make_public_dog(dog) } ), 201

@app.route('/api/v1.0/dog/<int:dog_id>', methods = ['PUT'])
def update_dog(dog_id):
    dog = filter(lambda t: t['id'] == dog_id, dogs)
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
    dog[0]['name'] = request.json.get('name', dog[0]['name'])
    dog[0]['description'] = request.json.get('description', dog[0]['description'])
    dog[0]['handler_id'] = request.json.get('handler_id', dog[0]['handler_id'])
    dog[0]['reg_status'] = request.json.get('reg_status', dog[0]['reg_status'])
    dog[0]['vacc_status'] = request.json.get('vacc_status', dog[0]['vacc_status'])
    return jsonify( { 'dog': make_public_dog(dog[0]) } )
    
@app.route('/api/v1.0/dog/<int:dog_id>', methods = ['DELETE'])
def delete_dog(dog_id):
    dog = filter(lambda t: t['id'] == dog_id, dogs)
    if len(dog) == 0:
        abort(404)
    dogs.remove(dog[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
