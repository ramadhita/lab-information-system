import datetime

from http import HTTPStatus
from sqlalchemy import and_, update
from flask_jwt_extended import jwt_required
from flask_restplus import Resource, reqparse, fields
from ...settings import sess #(.) itu nunjukkin mundur satu langkah
from ..api import api
from ...database import Pasien, CheckIn

check_out_namespace = api.namespace('v1/checkout', description='System process done') #

_data_get_req = reqparse.RequestParser()
_data_get_req.add_argument('PasienID', required=True, location='form', help='noKTP (sementara)')

_data_get_return = api.model('Token', {
    'status':fields.String(description='Status Berhasil'),
   # 'token' : fields.String(description='Generated token to use for requesting REST APIs') #bisa tambahin status nanti
})

@check_out_namespace.route('')
@api.doc(responses={
    HTTPStatus.UNPROCESSABLE_ENTITY:'Invalid token.'
})
class check_outAPI(Resource):
    @jwt_required
    @api.expect(_data_get_req, validate=True)
    @api.response(HTTPStatus.UNAUTHORIZED, 'gagal masuk')
    @api.marshal_with(_data_get_return, description='Token generated.')
    def post(self):
        r = _data_get_req.parse_args()
        result = {'status': None}
        IDpasien = r['PasienID']
        waktu = datetime.datetime.now()

        session = sess()
        session.query(CheckIn).filter(CheckIn.PasienID == IDpasien).update({CheckIn.waktuSelesai:waktu,
                                                                            CheckIn.statusbayar:'Sudah Bayar'},
                                                                            synchronize_session=False)
        session.commit()
        session.close()
        result['status'] = 'Check-out berhasil'
        return result