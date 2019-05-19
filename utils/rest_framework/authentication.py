from django.utils.encoding import smart_text
from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings


def get_authorization_header(request):
  """
  Return request's 'Authorization:' header, as a bytestring.

  Hide some test client ickyness where the header can be unicode.
  """
  auth = request.META.get('HTTP_AUTHORIZATION')
  if (auth and isinstance(auth, text_type)):
    # Work around django test client oddness
    auth = auth.encode(HTTP_HEADER_ENCODING)
  else:
    auth = request.query_params.get('token', b'')
    if isinstance(auth, text_type):
      auth = api_settings.JWT_AUTH_HEADER_PREFIX.encode(
        'utf8') + b' ' + auth.encode(
        HTTP_HEADER_ENCODING)
  return auth


class TokenAuthentication(JSONWebTokenAuthentication):
  """
  Simple token based authentication.

  Clients should authenticate by passing the token key in the "Authorization"
  HTTP header, prepended with the string "Token ".  For example:

      Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a

  Also, clients can authenticate by passing the token key in the query params
  body, using "token" key. For example:

      ?token=401f7ac837da42b97f613d789819ff93537bee6a
  """

  def get_jwt_value(self, request):
    auth = get_authorization_header(request).split()
    auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

    if not auth:
      return None

    if smart_text(auth[0].lower()) != auth_header_prefix:
      return None

    if len(auth) == 1:
      msg = _('Invalid Authorization header. No credentials provided.')
      raise exceptions.AuthenticationFailed(msg)
    elif len(auth) > 2:
      msg = _('Invalid Authorization header. Credentials string '
              'should not contain spaces.')
      raise exceptions.AuthenticationFailed(msg)

    return auth[1]
