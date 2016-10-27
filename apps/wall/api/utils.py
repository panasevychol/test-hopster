import ast
import jwt
import datetime
import endpoints


JWT_SECRET = 'mega secret'

def get_token(email):
    return jwt.encode({
        'email': email,
        'today': str(datetime.date.today())
        }, JWT_SECRET, algorithm='HS256')

def verify_token(token, email):
    return (jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            == { 'email': email, 'today': str(datetime.date.today()) })

def authenticate(request):
    auth_data = ast.literal_eval(request.auth_data)
    if not verify_token(**auth_data):
        raise endpoints.UnauthorizedException('Invalid token')
