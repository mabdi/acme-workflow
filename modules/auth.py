from flask import session,redirect, url_for
from core import db
from modules.models import User
from core.common import check, WebException
from voluptuous import Required, Length, Schema
from core.annotations import log_action,validation
from modules import captcha


login_schema = Schema({
    Required('username'): check(
        ("Usernames must be between 3 and 20 characters.", [str, Length(min=3, max=20)])
    ),
    Required('password'):
        check(("Passwords must be between 3 and 20 characters.", [str, Length(min=3, max=20)])
    ),
    Required('captcha'):
        check(("CAPTCHA must be 5 characters.", [str, Length(min=5, max=5)])
    )
}, extra=True)

@validation(schema = login_schema)
def login(params):
    if not captcha.validate(params['captcha']):
        raise WebException('Captcha is not correct.')
    user = User.query.filter_by(username = params['username']).first()
    if user is None:
        raise WebException('username/password is not correct.')
    if user.password == params['password']:
        # login success
        session["uid"] = user.id
        session["username"] = user.username
        session["password"] = user.password
        session["role"] = user.role
        return
    raise WebException('login failed.')

def is_logged_in():
    return  "uid" in session

def is_admin():
    return session.get('isAdmin', False)

def error404():
    return redirect(url_for("root"))