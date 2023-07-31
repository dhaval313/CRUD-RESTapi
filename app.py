from flask import Flask
from flask_pymongo import PyMongo
from flask import jsonify, request
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://localhost:27017/flask_crud"

mongo = PyMongo(app)


@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    name = data['name']
    email = data['email']
    pwd = data['pwd']

    if name and email and pwd and request.method == 'POST':
        id = mongo.db.users.insert_one({
            'name' : name,
            'email' : email,
            'pwd' : pwd
        })
    
        response = jsonify("User added successfully!")
        response.status_code = 200
        return response
    
    else:
        return not_found()
    
@app.route('/users', methods=['GET'])
def users():
    users = mongo.db.users.find()
    response = dumps(users)
    return response

@app.route('/users/<id>', methods=['GET'])
def user(id):
    user = mongo.db.users.find_one({'_id':ObjectId(id)})
    response = dumps(user)
    return response

@app.route('/users/<id>', methods=['DELETE'])
def delete(id):
    mongo.db.users.delete_one({'_id':ObjectId(id)})
    response = jsonify("User deleted!")
    response.status_code = 200
    return response

@app.route('/users/<id>', methods=['PUT'])
def update(id):
    _id = id
    data = request.json
    name = data['name']
    email = data['email']
    pwd = data['pwd']

    if name and email and pwd and _id and request.method == 'PUT':
        mongo.db.users.update_one({
            '_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)
        },
        {
            '$set':{
                'name': name,
                'email': email,
                'pwd' : pwd 
            }
        })

        response = jsonify("User updated!")
        response.status_code = 200
        return response
    
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        message : 'Not found ' + request.url
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)