from flask import redirect, url_for, render_template, session, request
from core import app 
from core.common import flat_multi,WebException
from modules import auth
from core.annotations import web_wrapper

_get_message = lambda exception: exception.args[0]

def logged_in():
    return redirect(url_for('orders.list_hook'))

@app.route('/')
@app.route('/login', methods=['GET'])
def root():
    if auth.is_logged_in():
        return logged_in()
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    params = flat_multi(request.form)
    try:
        auth.login(params)
        return logged_in()
    except WebException as errorz:
        return render_template('login.html',error = _get_message(errorz))   
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("root"))