from flask_jwt_extended import JWTManager
jwt = JWTManager()
# @jwt.user_claims_loader
# def add_claims_to_access_token(user):
#     return {
#         'role': user['role'],
#     }
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['username']