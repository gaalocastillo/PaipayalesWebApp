from calendar import timegm
from datetime import datetime
import uuid

from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.settings import api_settings

def create_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return token

def jwt_payload_handler(user):
    username_field = get_username_field()
    payload = {'user_id': str(user.id), 'email': user.email, 'username': user.email,
               'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA, username_field: user.email}

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload
