#!flask/bin/python
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
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'handler_id': 1,
        'reg_status': True,
        'vacc_status': False,
        'pedigree': u'Poodle'
    },
    {
        'id': 2,
        'registration_id': u'G2345',
        'name': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
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
    
@app.route('/todo/api/v1.0/dogs', methods = ['GET'])
#@auth.login_required
def get_dogs():
    return jsonify( { 'dogs': map(make_public_dog, dogs) } )

@app.route('/todo/api/v1.0/dogs/<int:dog_id>', methods = ['GET'])
#@auth.login_required
def get_dog(dog_id):
    dog = filter(lambda t: t['id'] == dog_id, dogs)
    if len(dog) == 0:
        abort(404)
    return jsonify( { 'dog': make_public_dog(dog[0]) } )

@app.route('/todo/api/v1.0/dogs', methods = ['POST'])
#@auth.login_required
def create_dog():
    if not request.json or not 'name' in request.json:
        abort(400)
    dog = {
        'id': dogs[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', ""),
        'done': False
    }
    dogs.append(dog)
    return jsonify( { 'dog': make_public_dog(dog) } ), 201

@app.route('/todo/api/v1.0/dogs/<int:dog_id>', methods = ['PUT'])
#@auth.login_required
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
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    dog[0]['name'] = request.json.get('name', dog[0]['name'])
    dog[0]['description'] = request.json.get('description', dog[0]['description'])
    dog[0]['done'] = request.json.get('done', dog[0]['done'])
    return jsonify( { 'dog': make_public_dog(dog[0]) } )
    
@app.route('/todo/api/v1.0/dogs/<int:dog_id>', methods = ['DELETE'])
#@auth.login_required
def delete_dog(dog_id):
    dog = filter(lambda t: t['id'] == dog_id, dogs)
    if len(dog) == 0:
        abort(404)
    dogs.remove(dog[0])
    return jsonify( { 'result': True } )
    
if __name__ == '__main__':
    app.run(debug = True)
