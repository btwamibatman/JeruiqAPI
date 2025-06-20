import jwt
import datetime
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")

def generate_token(user_id, email, role):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id,
        'email': email,
        'role': role
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return {'message': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'}