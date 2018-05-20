from app import create_app
from flask_restful import Api
from API.bus import BusAPI

app = create_app('development')
api = Api(app)

api.add_resource(BusAPI, '/cars/<int:id>')  # Route_1
#api.add_resource(BusAPI, '/cars/')  # Route_2

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)