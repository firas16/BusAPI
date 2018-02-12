from crud import db, ma
from sqlalchemy import create_engine

db_connect = create_engine('postgresql://localhost:5432/postgres')

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    line = db.Column(db.Integer)

    def serialize(self):
        return {
            'gene_id': self.name
        }



    @staticmethod
    def get_all():
        return Bus.query.all()

    @staticmethod
    def get():
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from bus")  # This line performs query and returns json result
        return {'bus': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID

    def __repr__(self):
        return "<Bus '{}'".format(self.name)


class BusSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name')


bus_schema = BusSchema()
buses_schema = BusSchema(many=True)