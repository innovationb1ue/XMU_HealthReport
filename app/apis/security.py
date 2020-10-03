from functools import wraps
from flask import request
from flask_restplus import abort
from ..Cores.DB_conn import DBConnector

def require_auth(func):
    """ Secure method decorator """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verify if User is Authenticated
        # Authentication logic goes here
        if request.headers.get('Authorization'):
            return func(*args, **kwargs)
        else:
            return abort(401)
    return wrapper