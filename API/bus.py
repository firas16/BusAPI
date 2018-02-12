from flask import Flask
from flask.ext.restful import Api, Resource
from flask.ext.restful import reqparse
from sqlalchemy import create_engine

db_connect = create_engine('postgresql://localhost:5432/postgres')
app = Flask(__name__)
api = Api(app)

class BusListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True,
                                   help='No bus name provided', location='json')
        #self.reqparse.add_argument('description', type=str, default="", location='json')
        super(BusListAPI, self).__init__()
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from bus")  # This line performs query and returns json result
        return {'bus': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID

    def post(self):
        pass

from flask.ext.restful import fields, marshal

task_fields = {
    'name': fields.String,
    'longitude': fields.String,
    'latitude': fields.String,
    'line': fields.Float,
    'uri': fields.Url('bus')
}

class BusAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        #self.reqparse.add_argument('description', type=str, location='json')
        #self.reqparse.add_argument('done', type=bool, location='json')
        super(BusAPI, self).__init__()

    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

api.add_resource(BusListAPI, '/buses', endpoint = 'buses')
api.add_resource(BusAPI, '/buses/<int:id>', endpoint = 'bus')