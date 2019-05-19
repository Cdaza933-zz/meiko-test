from rest_framework import parsers, renderers
from rest_framework import status
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework_jwt.views import JSONWebTokenAPIView, \
  jwt_response_payload_handler

from utils.authtoken.serializers import AuthTokenSerializer


class ObtainAuthToken(JSONWebTokenAPIView):
  """
  API View that receives a POST with a user's username and password.

  Returns a JSON Web Token that can be used for authenticated requests.
  """
  serializer_class = AuthTokenSerializer
  parser_classes = (
    parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
  renderer_classes = (renderers.JSONRenderer,)
  if coreapi is not None and coreschema is not None:
    schema = ManualSchema(
      fields=[
        coreapi.Field(
          name="correo",
          required=True,
          location='form',
          schema=coreschema.String(
            title="Correo",
            description="Correo valido para autenticacion",
          ),
        ),
        coreapi.Field(
          name="contrasenia",
          required=True,
          location='form',
          schema=coreschema.String(
            title="Contrasenia",
            description="Contrasenia valido para autenticacion",
          ),
        ),
      ],
      encoding="application/json",
    )

  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('user')
    if user:
      user = serializer.object.get('user') or request.user
      token = serializer.object.get('token')
      response_data = jwt_response_payload_handler(token, user, request)
      response = Response(response_data)
      return response

    return Response(serializer.errors,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
