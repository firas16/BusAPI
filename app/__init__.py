from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, abort, make_response

#from flask_api import FlaskAPI

# local import
from instance.config import app_config


# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from data.bus import Bus

    @app.route('/buses/', methods=['POST', 'GET'])
    def buses():

        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]
        if access_token:
            # Attempt to decode the token and get the User ID
            from data.user import User
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated
                if(request.method == "POST"):
                    name = str(request.form.get('name', ''))
                    line = str(request.form.get('line', ''))
                    if(name):
                        bus = Bus(name=name, line=line)
                        bus.save()
                        response = jsonify({
                            'id': bus.id,
                            'name': bus.name,
                            'line': bus.line,
                            'longitude' : 0,
                            'latitude': 0,
                        })
                        response.status_code = 201
                    return response
                else:
                    bucketlists = Bus.get_all()
                    results = []
                    for bucketlist in bucketlists:
                        obj = {
                            'name': bucketlist.name,
                        }
                        results.append(obj)
                    response = jsonify(results)
                    response.status_code = 200
                return response
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


    @app.route('/buses/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bus_manipulation(id, **kwargs):

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
                           ,200)

                elif request.method == 'PUT':
                    name = str(request.form.get('name', ''))
                    bus.name = name
                    bus.save()
                    response = jsonify({
                        'id': bus.id,
                        'name': bus.name,
                        'line': bus.line
                    })
                    response.status_code = 200
                    return response
                else:
                    # GET
                    response = jsonify({
                        'id': bus.id,
                        'name': bus.name,
                        'line': bus.line,
                        'longitude': bus.longitude,
                        'latitude' : bus.latitude
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
                return make_response(jsonify(response)), 401

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
