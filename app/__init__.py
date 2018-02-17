from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, abort
# local import
from instance.config import app_config


# initialize sql-alchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '\x91N83\xb3\xea\xdd\x85\xfa\xa1c\xfa\xae\xb1\x1cFFy\xb7i/\xb4\x99\x88'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
    db.init_app(app)

    from data.bus import Bus

    @app.route('/buses/', methods=['GET'])
    def buses():
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

    @app.route('/bus/', methods=['POST'])
    def create_task():
        if (request.method == "POST"):
            bus = Bus(name='hemla', longitude=10, latitude=25)
            bus.save()
            response = jsonify({
               'id': bus.id,
               'name': bus.name,
               'longitude': bus.longitude,
               'latitude': bus.latitude,

            })
        return response

    from flask import make_response

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Not found'}), 404)


    return app