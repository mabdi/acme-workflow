import uuid
import core
import random
import string

from voluptuous import Invalid, MultipleInvalid
from hashlib import md5


def esc(s):
    """
    Escapes a string to prevent html injection

    Returns a string with special HTML characters replaced.
    Used to sanitize output to prevent XSS. We looked at 
    alternatives but there wasn't anything of an appropriate 
    scope that we could find. In the long-term this should be 
    replaced with a proper sanitization function written by 
    someone else."""
    return s\
        .replace('&', '&amp;')\
        .replace('<', '&lt;')\
        .replace('>', '&gt;')\
        .replace('"', '&quot;')\
        .replace("'", '&#39;')

def token():
    """
    Generate a token, should be random but does not have to be secure necessarily. Speed is a priority.

    Returns:
        The randomly generated token
    """

    return str(uuid.uuid4().hex)

def hash(string):
    """
    Hashes a string

    Args:
        string: string to be hashed.
    Returns:
        The hex digest of the string.
    """

    return md5(string.encode("utf-8")).hexdigest()

class APIException(Exception):
    """
    Exception thrown by the API.
    """
    data = {}


def WebSuccess(message=None, data=None):
    """
    Successful web request wrapper.
    """

    return {
        "status": 1,
        "message": message,
        "data": data
    }

def WebError(message=None, data=None):
    """
    Unsuccessful web request wrapper.
    """

    return {
        "status": 0,
        "message": message,
        "data": data
    }

class WebException(APIException):
    """
    Errors that are thrown that need to be displayed to the end user.
    """

    pass

class InternalException(APIException):
    """
    Exceptions thrown by the API constituting mild errors.
    """

    pass

class SevereInternalException(InternalException):
    """
    Exceptions thrown by the API constituting critical errors.
    """

    pass

def flat_multi(multidict):
    """
    Flattens any single element lists in a multidict.

    Args:
        multidict: multidict to be flattened.
    Returns:
        Partially flattened database.
    """

    flat = {}
    for key, values in multidict.items():
        flat[key] = values[0] if type(values) == list and len(values) == 1 \
                    else values
    return flat


def check(*callback_tuples):
    """
    Voluptuous wrapper function to raise our APIException

    Args:
        callback_tuples: a callback_tuple should contain (status, msg, callbacks)
    Returns:
        Returns a function callback for the Schema
    """

    def v(value):
        """
        Trys to validate the value with the given callbacks.

        Args:
            value: the item to validate
        Raises:
            APIException with the given error code and msg.
        Returns:
            The value if the validation callbacks are satisfied.
        """

        for msg, callbacks in callback_tuples:
            for callback in callbacks:
                try:
                    result = callback(value)
                    if not result and type(result) == bool:
                        raise Invalid()
                except Exception:
                    raise WebException(msg)
        return value
    return v

def validate(schema, data):
    """
    A wrapper around the call to voluptuous schema to raise the proper exception.

    Args:
        schema: The voluptuous Schema object
        data: The validation data for the schema object

    Raises:
        APIException with status 0 and the voluptuous error message
    """

    try:
        schema(data)
    except MultipleInvalid as error:
        raise APIException(0, None, error.msg)

def safe_fail(f, *args, **kwargs):
    """
    Safely calls a function that can raise an APIException.

    Args:
        f: function to call
        *args: positional arguments
        **kwargs: keyword arguments
    Returns:
        The function result or None if an exception was raised.
    """

    try:
        return f(*args, **kwargs)
    except APIException:
        
        return None


def random_digits(digit_numbers):
    return ''.join(random.choice(string.digits) for _ in range(digit_numbers))