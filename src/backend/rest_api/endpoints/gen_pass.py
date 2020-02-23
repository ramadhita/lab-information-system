from werkzeug.security import generate_password_hash, check_password_hash

def generatePassword(password):
    return generate_password_hash(password, method='sha256')

def checkPassword(pwhash,password):
    return check_password_hash(pwhash,password)