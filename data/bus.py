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

    @staticmethod
    def get_bus(id):
        res = Bus.query.get(id)
        return res

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bus.query.all()

    def __repr__(self):
        return "<Bus '{}'".format(self.name)