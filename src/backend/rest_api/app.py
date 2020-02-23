from flask import Flask, Blueprint
from .api import api
from .jwt import jwt
from .endpoints import all_namespaces
from ..settings import DATABASE_URL

print('Starting API')
app = Flask(__name__)
app.config['RESTPLUS_VALIDATE'] = True
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['APPLICATION_ROOT'] = '/api/'
app.config['RESTPLUS_VALIDATE'] = True
app.config['RESTPLUS_MASK_SWAGGER'] = False
app.config['JWT_SECRET_KEY'] = '\x90\xbclab service super secret key\x1a\xff'
app.config['JWT_TOKEN_LOCATION'] = 'query_string'
app.config['JWT_QUERY_STRING_NAME'] = 'token'
blueprint = Blueprint('rest_api', __name__, url_prefix='/api', template_folder='templates')
api.init_app(blueprint)
for namespace in all_namespaces:
    api.add_namespace(namespace)
app.register_blueprint(blueprint)
jwt.init_app(app)

if __name__== '__main__':
    app.run(host='0.0.0.0',port=80, debug=True)
    #app.run(debug=True)