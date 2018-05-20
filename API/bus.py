from flask import jsonify, Flask
from data.bus import Bus
from flask.ext.restful import Api, Resource, abort, request
from app import db

app = Flask(__name__)
api = Api(app)

class BusAPI(Resource):
    def get(self, id):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            # Get the user id related to this access token
            from data.user import User
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                # retrieve a bus using it's ID
                bus = Bus.query.filter_by(id=id).first()
                if not bus:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)
                    # GET
                response = jsonify({
                    'id': bus.id,
                    'name': bus.name,
                    'line': bus.line,
                    'longitude': bus.longitude,
                    'latitude': bus.latitude
                })
                response.status_code = 200
                return response
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return (jsonify(response)), 401

    @app.route('/cars/', methods=['POST'])
    def post(self, id):
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            # Attempt to decode the token and get the User ID
            from data.user import User
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated
                name = str(request.form.get('name', ''))
                line = str(request.form.get('line', ''))
                if (name):
                    bus = Bus(name=name, line=line)
                    bus.save()
                    response = jsonify({
                        'id': bus.id,
                        'name': bus.name,
                        'line': bus.line,
                        'longitude': 0,
                        'latitude': 0,
                    })
                    response.status_code = 201
                return response

            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return (jsonify(response)), 401

    def put(self, id):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            # Get the user id related to this access token
            from data.user import User
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                # retrieve a bus using it's ID
                bus = Bus.query.filter_by(id=id).first()
                if not bus:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == 'PUT':
                    name = str(request.form.get('name', ''))
                    line = str(request.form.get('line', ''))
                    bus.name = name
                    bus.line = line
                    bus.save()
                    response = jsonify({
                        'id': bus.id,
                        'name': bus.name,
                        'line': bus.line
                    })
                    response.status_code = 200
                    return response

                    return response
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return (jsonify(response)), 401

    def delete(self, id):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            # Get the user id related to this access token
            from data.user import User
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                # retrieve a bus using it's ID
                bus = Bus.query.filter_by(id=id).first()
                if not bus:
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                if request.method == 'DELETE':
                    bus.delete()
                    return (
                        "bus {} deleted successfully".format(bus.id)
                        , 200)
                    return response
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return (jsonify(response)), 401

api.add_resource(BusAPI, '/cars/<int:id>', endpoint = 'bus')



