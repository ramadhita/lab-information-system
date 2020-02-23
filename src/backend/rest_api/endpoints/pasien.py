from datetime import timedelta
from http import HTTPStatus
from sqlalchemy import and_
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, reqparse, fields
from ...settings import sess #(.) itu nunjukkin mundur satu langkah
from ..api import api
from ...database import Pasien

pasien_namespace = api.namespace('v1/pasien', description='Insert new Patient to Database') #

_data_get_req = reqparse.RequestParser()
_data_get_req.add_argument('nama', required=True, location='form', help='Your Full Name')
_data_get_req.add_argument('noKTP', required=True, location='form',   help='no KTP (16 digit)')
_data_get_req.add_argument('notelp', required=True, location='form',   help='Phone Number')
_data_get_req.add_argument('tanggalLahir', required=True, location='form', help='YYYY/MM/DD')
_data_get_req.add_argument('jenisKelamin', location='form', choices=('L','P'),help='Gender (L/P)')
_data_get_req.add_argument('alamat', required=True, location='form', help='Address')

_data_get_return = api.model('Token', {
    'status':fields.String(description='Status Berhasil'),
   # 'token' : fields.String(description='Generated token to use for requesting REST APIs') #bisa tambahin status nanti
})

@pasien_namespace.route('')
@api.doc(responses={
    HTTPStatus.UNPROCESSABLE_ENTITY:'Invalid token.'
})
class pasienAPI(Resource):
    @jwt_required
    @api.expect(_data_get_req, validate=True)
    @api.response(HTTPStatus.UNAUTHORIZED, 'gagal masuk')
    @api.marshal_with(_data_get_return, description='Token generated.')
    def post(self):
        r = _data_get_req.parse_args()
        result = {'status': None}
        nama = r['nama']
        noKTP = r['noKTP']
        notelp = r['notelp']
        tanggalLahir = r['tanggalLahir']
        jenisKelamin = r['jenisKelamin']
        alamat   = r['alamat']

        session = sess()
        query   = session.query(Pasien).filter(and_(Pasien.nama == nama,
                                                   Pasien.noKTP==noKTP,
                                                   Pasien.tglLahir==tanggalLahir,
                                                   Pasien.jenisKelamin== jenisKelamin,
                                                   )).one_or_none()
        if query:
            result['status'] = 'Sudah terdaftar'
        else:
            entry               = Pasien(nama,noKTP,notelp,tanggalLahir,jenisKelamin,alamat)
            session.add(entry)
            result['status']    = 'Akun Pasien berhasil dibuat'
            session.commit()
        session.close()
        return result