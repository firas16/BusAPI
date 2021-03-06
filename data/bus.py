from app import db

class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    line = db.Column(db.Integer)

    def __init__(self, name, line):
        self.name = name
        self.line = line
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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bus '{}'".format(self.name)