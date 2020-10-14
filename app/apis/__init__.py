""" API Blueprint Application """

from flask import Blueprint
from flask_restplus import Api

api_rep = Blueprint('api_rep', __name__, url_prefix=None)
api_rest = Api(api_rep)


@api_rep.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response


# Import resources to ensure view is registered
from .report import * # NOQA
from .manage import *
