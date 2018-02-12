#!flask/bin/python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x91N83\xb3\xea\xdd\x85\xfa\xa1c\xfa\xae\xb1\x1cFFy\xb7i/\xb4\x99\x88'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
db = SQLAlchemy(app)


# @app.route('/buses', methods=['GET'])
# def get_Buses():
#     return jsonify({'buses': tasks})

class Bus(db.Model):
    __tablename__ = 'bus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    line = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name

    def serialize(self):
        return {
            'gene_id': self.name
        }

    @staticmethod
    def get_all():
        return Bus.query.all()

    def __repr__(self):
        return "<Bus '{}'".format(self.name)

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


from flask import request
from flask import abort

@app.route('/bus', methods=['POST'])
def create_task():
    if not request.json or not 'name' in request.json:
        abort(400)
    bus = Bus(name = 'hemla', longitude='1321', latitude='5413', line = 28)

    db.session.add(bus)
    db.session.commit()
    return jsonify({'bus': bus}), 201

# tasks = [
#     {
#         'id': 1,
#         'title': u'Buy groceries',
#         'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
#         'done': False
#     },
#     {
#         'id': 2,
#         'title': u'Learn Python',
#         'description': u'Need to find a good Python tutorial on the web',
#         'done': False
#     }
# ]

# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})
#
# from flask import abort
# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': task[0]})

from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

from flask import request

# @app.route('/todo/api/v1.0/tasks', methods=['POST'])
# def create_task():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     task = {
#         'id': tasks[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     tasks.append(task)
#     return jsonify({'task': task}), 201

if __name__ == '__main__':
    app.run(debug=True)