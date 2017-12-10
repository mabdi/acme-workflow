""" API annotations and assorted wrappers. """

import json, traceback
import core
import modules.auth

from core.common import WebSuccess, WebError, WebException, InternalException, SevereInternalException
from core.common import validate
from datetime import datetime
from functools import wraps
from flask import session, request, abort, Response, render_template

write_logs_to_db = False # Default value, can be overwritten by api.py
 

_get_message = lambda exception: exception.args[0]

def log_action(f):
    """
    Logs a given request if available.
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        """
        Provides contextual information to the logger.
        """

        log_information = {
            "name": "{}.{}".format(f.__module__, f.__name__),
            "args": args,
            "kwargs": kwds,
            "result": None,
        }

        try:
            log_information["result"] = f(*args, **kwds)
        except WebException as error:
            log_information["exception"] = _get_message(error)
            raise
        finally:
            core.logger.info(log_information)

        return log_information["result"]

    return wrapper

def api_wrapper(f):
    """
    Wraps api routing and handles potential exceptions
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        web_result = {}
        try:
            web_result = f(*args, **kwds)
            if type(web_result) is not WebSuccess:
                web_result = WebSuccess(message = "Action performed successfully",data = web_result)
        except WebException as error:
            web_result = WebError(_get_message(error), error.data)
        except InternalException as error:
            message = _get_message(error)
            if type(error) == SevereInternalException:
                core.logger.critical(traceback.format_exc())
                web_result = WebError("There was a critical internal error. Contact an administrator.")
            else:
                core.logger.error(traceback.format_exc())
                web_result = WebError(message)
        except Exception as error:
            core.logger.error(traceback.format_exc())

        return Response(json.dumps(web_result),content_type='appication/json') 

    return wrapper

def require_login(f):
    """
    Wraps routing functions that require a user to be logged in
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        if not modules.auth.is_logged_in():
            raise WebException("You must be logged in")
        return f(*args, **kwds)
    return wrapper

def check_csrf(f):
    @wraps(f)
    @require_login
    def wrapper(*args, **kwds):
        if 'token' not in session:
            raise InternalException("CSRF token not in session")
        if 'token' not in request.form:
            raise InternalException("CSRF token not in form")
        if session['token'] != request.form['token']:
            raise InternalException("CSRF token is not correct")
        return f(*args, **kwds)
    return wrapper

def require_admin(f):
    """
    Wraps routing functions that require a user to be an admin
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        if not modules.auth.is_admin():
            raise WebException("You must be an admin!")
        return f(*args, **kwds)
    return wrapper



def validation(schema):
    def true_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            validate(schema, args[0])
            return f(*args, **kwargs)
        return wrapped
    return true_decorator

def web_wrapper(template, requires_login):
    
    def true_decorator(f):

        @wraps(f)
        def wrapper(*args, **kwds):          
            try:
                if requires_login and not modules.auth.is_logged_in():
                    return modules.auth.error404()      # TODO do parametric
                data = f(*args, **kwds) 
                return render_template(template, data = data)
            except Exception as error:
                core.logger.error(traceback.format_exc())
                # return  render_template('error500')

        return wrapper

    return true_decorator