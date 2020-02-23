from datetime import timedelta
from http import HTTPStatus

from flask_jwt_extended import create_access_token
from flask_restplus import Resource, reqparse, fields
from ...settings import sess
from ..api import api
from ...database import User
from .gen_pass import checkPassword

token_namespace = api.namespace('v1/token', description='Generate token.') #yang dipanggil v1/token

_token_get_req = reqparse.RequestParser()
_token_get_req.add_argument('username', required=True, location='form', help='Username of your account.')
_token_get_req.add_argument('password', required=True, location='form', help='Password of your account.')

_token_get_return = api.model('Token', {
    'username':fields.String(description='Username'),
    'token': fields.String(description='Generated token to use for requesting REST APIs'), #bisa tambahin status nanti
    'status' :fields.String(description='Status Berhasil')
})


@token_namespace.route('')
@api.doc(security=None)
class TokenAPI(Resource):
    @api.expect(_token_get_req, validate=True)
    @api.response(HTTPStatus.UNAUTHORIZED, 'Wrong Username/Password')
    @api.marshal_with(_token_get_return, description='Token generated.')
    def post(self):
        r = _token_get_req.parse_args()
        result = {'username': None,'token': None, 'status': None}
        username = r['username']
        password = r['password']
        identity = {
            'username': username,
        }
        session = sess()
        query = session.query(User).filter(User.username == username).one_or_none()
        if query:
            if checkPassword(query.password,password) :
                token = create_access_token(identity=identity, expires_delta=timedelta(hours=8), fresh=True)
                result['token'] = token
                result['status'] = 'Berhasil'
                result['username']= username
            else:
                result['status'] ='Password salah'
        else:
            result['status'] = 'Username tidak ditemukan'
        session.close()
        return result