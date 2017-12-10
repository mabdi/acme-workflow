from core import db
from flask import session
from core.common import check, WebException, safe_fail
from core.annotations import validation
from datetime import datetime
from voluptuous import Required, Length, Schema, Range
from modules.models import *

new_order_schema = Schema({
    Required('product'): check(
        ("Invalid Product Id", [int]),
        ("Invalid Product", [ lambda id: safe_fail(get_product_by_id, id=id) is not None])
    ),
    Required('count'): check(
        ("Count must be integer.", [int]),
        ("Count must be between 1 and 1000.", [ lambda n:  int(n)>0 and int(n)<=1000] )
    )
}, extra=True)

def list_orders():
    uid = session['uid']
    role = session['role']
    if role == roles["customer"]:
        return Order.query.filter_by(user_id = uid).all()
    if role == roles["sales"]:
        return Order.query.filter( (Order.state == states["added"]) | (Order.state == states["cost_set"]) | (Order.state == states["production_test_done"])).all()
    if role == roles["engineering"]:
        return Order.query.filter( (Order.state == states["confirm_add"]) ).all()
    if role == roles["production"]:
        return Order.query.filter( (Order.state == states["confirm_pay"]) | (Order.state == states["test_done"])).all()
    if role == roles["finance"]:
        return Order.query.filter( (Order.state == states["payed"])).all()
    if role == roles["test"]:
        return Order.query.filter( (Order.state == states["production_done"])).all()
    return None

def list_products():
    return Product.query.all()

@validation(schema=new_order_schema)
def new(params):
    p = Order(user_id= session['uid'], product_id= params['product'], count = params['count'], description= params['description'],
                    date = datetime.now(), state = states['added'],cost=-1, test_pass = 0)
    db.session.add(p)
    db.session.commit()

def get_product_by_id(id):
    return Product.query.filter_by(id=id).first()

def change_state(order_id,to_state):
    order = Order.query.filter_by(id=order_id).first() #.update({"state": to_state})
    order.state = to_state
    db.session.commit()
    
def set_cost(order_id,cost):
    Order.query.filter_by(id=order_id).update({"cost": cost})
    db.session.commit()
