from flask import session



def is_logged_in():
    return  "uid" in session

def is_admin():
    return session.get('isAdmin', False)