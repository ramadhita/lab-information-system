from datetime import timedelta
from http import HTTPStatus
from sqlalchemy import or_
from flask_jwt_extended import create_access_token,jwt_required
from flask_restplus import Resource, reqparse, fields
from ...settings import sess #(.) itu nunjukkin mundur satu langkah
from ..api import api
from ...database import User
from .gen_pass import generatePassword

signup_namespace = api.namespace('v1/signup', description='Insert new User to Database') #

_data_get_req = reqparse.RequestParser()
_data_get_req.add_argument('username', required=True, location='form', help='Username of your account.')
_data_get_req.add_argument('password', required=True, location='form',   help='Password of your account.')
_data_get_req.add_argument('nama', required=True, location='form', help='Your Full Name')
_data_get_req.add_argument('jabatan', required=True, location='form', choices=('01','02'), default='01',help='Code perawat/dokter')
_data_get_req.add_argument('email', required=True, location='form', help='User email to be verified')

_data_get_return = api.model('Token', {
    'status':fields.String(description='Status Berhasil'),
    'token' : fields.String(description='Generated token to use for requesting REST APIs') #bisa tambahin status nanti
})

@signup_namespace.route('')
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
        result = {'status': None,'token': None}
        username = r['username']
        password = generatePassword(r['password'])
        nama    = r['nama']
        jabatan = r['jabatan']
        email   = r['email']

        session = sess()
        query   = session.query(User).filter(or_(User.username == username, User.email==email)).one_or_none()
        if query:
            result['status'] = 'username/email sudah terdaftar'
        else:
            entry   = User(username,password,nama,jabatan,email)
            session.add(entry)
            result['status'] = 'Akun berhasil dibuat'
            result['token'] = 'Token generated'
            session.commit()
        session.close()
        return result