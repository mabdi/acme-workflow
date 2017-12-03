from core import db

class Model1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data1 = db.Column(db.String(11),index=True, unique=True)
    