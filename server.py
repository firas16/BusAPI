from app import create_app
from flask_restful import Api
from API.bus import Busitem

app = create_app('development')
api = Api(app)

api.add_resource(Busitem, '/bus/<bus_id>')  # Route_3

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)