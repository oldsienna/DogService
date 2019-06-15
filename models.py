#!/usr/bin/env python

#########################################################
# This is the functional processing file.
# It contains the DB connections, queries and processes
#########################################################

# Import modules required for app
import os, time, json, re
from pymongo import MongoClient
from bson.objectid import ObjectId

def db_conn():
    # Check if user defined environment variable exists
    if "DB_URI" in os.environ:
        DB_ENDPOINT = MongoClient(os.environ['DB_URI'])
        DB_NAME = os.environ['DB_Name']

	# Check if running in Pivotal Web Services with MongoDB service bound
    elif 'VCAP_SERVICES' in os.environ:
        VCAP_SERVICES = json.loads(os.environ['VCAP_SERVICES'])
        MONGOCRED = VCAP_SERVICES["mlab"][0]["credentials"]
        DB_ENDPOINT = MongoClient(MONGOCRED["uri"])
        DB_NAME = str(MONGOCRED["uri"].split("/")[-1])

    # Otherwise, assume running locally with local MongoDB instance
    else:
	    DB_ENDPOINT = MongoClient('127.0.0.1:27017')
	    DB_NAME = "Dogs"
    # Get database connection using database endpoint and name defined above
    global db
    db = DB_ENDPOINT[DB_NAME]

def init_db():
    db_conn() # Connect to database

def new_dog(dog):
    # If dog id already exists in the system then raise an error
    dog_exists = db.dog_details.find_one({'registration_id': dog['registration_id']})

    if not dog_exists:
        # Add dog to database
        return_code = 0
        _id = db.dog_details.insert({'registration_id': dog['registration_id'],
                                    'description': dog['description'],
                                    'handler_id': dog['handler_id'],
                                    'name': dog['name'],
                                    'pedigree': dog['pedigree'],
                                    'reg_status': dog['reg_status'],
                                    'vacc_status': dog['vacc_status']})
 
	return str(_id)

def get_dog(dog_id):
    # Retrieve a dog by id
    dog_rec = db.dog_details.find_one({'_id': ObjectId(dog_id)})
    # Check if dog exists
    if dog_rec:
        dog = {
            'id': dog_id,
            'registration_id': dog_rec.get('registration_id'),
            'name':dog_rec.get('name'),
            'description': dog_rec.get('description'),
            'handler_id': dog_rec.get('handler_id'),
            'pedigree': dog_rec.get('pedigree'),
            'reg_status': dog_rec.get('reg_status'),
            'vacc_status': dog_rec.get('vacc_status')
        }
        return dog
    else:
        return None

def update_dog(dog):
    # Update dog fields if present
    db.dog_details.update_one({'_id': ObjectId(dog['id'])},
                    { "$set" :{ 'registration_id': dog['registration_id'],
                                'name': dog['name'],
                                'description': dog['description'],
                                'handler_id': dog['handler_id'],
                                'pedigree': dog['pedigree'],
                                'reg_status': dog['reg_status'],
                                'vacc_status': dog['vacc_status'] }
                    },
                    upsert=True)
    return

def delete_dog(dog_id):
    db.dog_details.delete_one({'_id': ObjectId(dog_id)})