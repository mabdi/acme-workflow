from core import db
from sqlalchemy.orm import relationship

roles = {
    "sales":10,
    "engineering":20,
    "production":30,
    "finance":40,
    "test":50,
    "customer":90
}

states = {
    "added" : 1,
    "confirm_add" : 2,
    "cost_set" : 3,
    "confirm_cost" : 4,
    "payed" : 5,
    "confirm_pay": 6,
    "production_done":8,
    "test_done":9,
    "production_test_done":10,
    "confirm_ready":11
}

states_str = {
    1: "Waiting for approve by sales",
    2: "Waiting for set cost by engineering",
    3: "Waiting for approve cost by sales",
    4: "Waiting for pay by customer",
    5: "Waiting for approve payment by finance",
    6: "Waiting for finish production ",
    8: "Waiting for QC Test done",
    9: "Waiting for finish QC problems",
    10: "Waiting for approve product by sales",
    11: "Ready"
}

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(11),index=True, unique=True)
    password = db.Column(db.String(11))
    role = db.Column(db.Integer)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name  = db.Column(db.String(100))
    picture  = db.Column(db.String(100))
    description = db.Column(db.String(200))

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", foreign_keys=user_id)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = relationship("Product", foreign_keys=product_id)
    count = db.Column(db.Integer)
    description =  db.Column(db.String(200))
    date = db.Column(db.Integer)
    state = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    test_pass = db.Column(db.Integer)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    order = relationship("Order", foreign_keys=order_id)
    amount =  db.Column(db.Integer)
    date =  db.Column(db.Integer)

