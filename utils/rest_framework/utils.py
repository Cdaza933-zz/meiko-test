from calendar import timegm
from datetime import datetime
import uuid
import warnings

from rest_framework_jwt.compat import get_username
from rest_framework_jwt.settings import api_settings


def jwt_get_user_id_from_payload_handler(payload):
  """
  Override this function if user_id is formatted differently in payload
  """
  warnings.warn(
    'The following will be removed in the future. '
    'Use `JWT_PAYLOAD_GET_USERNAME_HANDLER` instead.',
    DeprecationWarning
  )

  return payload.get('sub').get('user_id')


def jwt_get_username_from_payload_handler(payload):
  """
  Override this function if username is formatted differently in payload
  """
  return payload.get('sub').get('username')

def jwt_payload_handler(user):
  username = get_username(user)

  warnings.warn(
    'The following fields will be removed in the future: '
    '`email` and `user_id`. ',
    DeprecationWarning
  )

  payload = {
    'iat': datetime.utcnow(),
    'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
    'sub': {
      'user_id': user.pk,
      'username': username
    }
  }
  if hasattr(user, 'email'):
    payload['sub']['email'] = user.email
  if isinstance(user.pk, uuid.UUID):
    payload['sub']['user_id'] = str(user.pk)

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
