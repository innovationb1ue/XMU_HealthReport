from flask_restplus import Resource

from . import api_rest
from .security import require_auth


class SecureResource(Resource):
    method_decorators = [require_auth]


@api_rest.route('/Manage/index')
class ManageIndex(SecureResource):
    def get(self):
        return 'Manage index page'





