from core import db
from flask import session
from core.common import check, WebException
from core.annotations import log_action,validation
from datetime import datetime
from voluptuous import Required, Length, Schema
from modules.models import Model1

sample_schema = Schema({
    Required('username'): check(
        ("Usernames must be between 3 and 20 characters.", [str, Length(min=3, max=20)])
    ),
    Required('password'):
        check(("Passwords must be between 3 and 20 characters.", [str, Length(min=3, max=20)])
    )
}, extra=True)


@log_action
@validation(schema = sample_schema)
def method1(params):
    model1 = Model1( data1= params['data1'], ts= int(datetime.now().timestamp()))
    db.session.add(model1)

@log_action
def method2(params):
    if( is_something_true() ):
            session['some_key'] = params["username"]
            session.permanent = True
            return {
                "some_key": params["username"]
            }
    else:
        raise WebException("Login Error")


def is_something_true():
    return True

@log_action
def method3(arg1):
    from_db = Model1.query.filter_by(data1 = arg1).limit(30).all()
    return {
        "data": from_db
    }