from datetime import timedelta
from http import HTTPStatus
from sqlalchemy.sql import select
from flask_jwt_extended import create_access_token,jwt_required
from flask_restplus import Resource, reqparse, fields
from ...settings import sess #(.) itu nunjukkin mundur satu langkah
from ..api import api
from ...database import Lab
from .gen_pass import generatePassword

listalat_namespace = api.namespace('v1/list_alat', description='Giving Tools list') #

_data_get_req = reqparse.RequestParser()
_data_get_req.add_argument('kodelab', required=True, location='form', help='Lab Code')

_data_get_return = api.model('Token', {
    'list':fields.String(description='Alat yang tersedia di lab'),
})

@listalat_namespace.route('')
@api.doc(responses={
    HTTPStatus.UNPROCESSABLE_ENTITY:'Invalid token.'
})
class signupAPI(Resource):
    @jwt_required
    @api.expect(_data_get_req, validate=True)
    @api.response(HTTPStatus.UNAUTHORIZED, 'gagal masuk')
    @api.marshal_with(_data_get_return, description='Token generated.')
    def post(self):
        r = _data_get_req.parse_args()
        result = {'list': None}
        kodelab= r['kodelab']

        session = sess()
        query   = session.query(Lab).filter(Lab.nama == kodelab).one_or_none()
        if query:
            result['list'] = session.query(Lab.alatTes).filter(Lab.nama == kodelab).all()
        else:
            result['list'] = 'Lab Unidentified'
        session.close()
        return result