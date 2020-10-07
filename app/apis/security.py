from functools import wraps
from flask import request
from flask_restplus import abort
from ..Cores.DB_conn import DBConnector
from ..CONFIG import *

conn = DBConnector(MONGODB_USER, MONGODB_PWD, MONGODB_DBNAME)

def require_auth(func):
    """ Secure method decorator """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verify if User is Authenticated
        # Authentication logic goes here
        usr = request.cookies.get('userstr')
        if usr:
            print(usr)
            # if conn.get_pwd(username) == pwd:
            return func(*args, **kwargs)
        return abort(401)
    return wrapper