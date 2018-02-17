from app import db


class Bus(db.Model):
    __tablename__ = 'bus'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    line = db.Column(db.Integer)

    def __init__(self, name, longitude, latitude):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude

    def serialize(self):
        return {
            'gene_id': self.name
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bus.query.all()

    def __repr__(self):
        return "<Bus '{}'".format(self.name)


# class BusSchema(ma.Schema):
#     class Meta:
#         # Fields to expose
#         fields = ('name')
#
#
# bus_schema = BusSchema()
# buses_schema = BusSchema(many=True)