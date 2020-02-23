from http import HTTPStatus
from flask_restplus import Api
from jwt.exceptions import PyJWTError
from flask_jwt_extended.exceptions import JWTExtendedException
authorizations = {
    'tokenkey': {
        'type': 'apiKey',
        'in': 'query',
        'name': 'token',
    }
}
api = Api(version='1', title='LAB SERVICE REST API', doc='/doc/', security='tokenkey',
          description='Documentation and demo for LAB SERVICE REST API', authorizations=authorizations)
@api.errorhandler(PyJWTError)
def jwt_error_handler(e):
    message = 'Token is not valid.'
    return {'message': message}, HTTPStatus.UNPROCESSABLE_ENTITY
@api.errorhandler(JWTExtendedException)
def jwt_extended_erro_handler(e):
    message = 'Token is not valid.'
    return {'message': message}, HTTPStatus.UNPROCESSABLE_ENTITY