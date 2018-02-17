from flask_restful import Resource
from flask import jsonify
from data.bus import Bus
from app import db

class Busitem(Resource):
    def get(self, bus_id):
        result = Bus.get_bus(bus_id)
        obj = {
            'name': result.name,
        }
        return jsonify(obj)


