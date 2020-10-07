from flask_restplus import Resource, fields
from flask import redirect
from .security import require_auth
from . import api_rest


class SecureResource(Resource):
    method_decorators = [require_auth]


@api_rest.route('/Manage/index')
class ManageIndex(SecureResource):
    def get(self):
        return 'Manage index page'





