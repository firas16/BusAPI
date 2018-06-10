from app import db

class Station(db.Model):
    __tablename = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    sens = db.Column(db.Boolean)