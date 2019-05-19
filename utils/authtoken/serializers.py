from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework_jwt.compat import Serializer
from rest_framework_jwt.serializers import jwt_payload_handler, \
  jwt_encode_handler


class AuthTokenSerializer(Serializer):
  correo = serializers.CharField(label=_("Correo"))
  contrasenia = serializers.CharField(
    label=_("Contrasenia"),
    style={'input_type': 'password'},
    trim_whitespace=False
  )

  def validate(self, attrs):
    correo = attrs.get('correo')
    contrasenia = attrs.get('contrasenia')
    if correo and contrasenia:

      user = authenticate(request=self.context.get('request'),
                          username=correo, password=contrasenia)

      if user:
        if not user.is_active:
          msg = _('User account is disabled.')
          raise serializers.ValidationError(msg)

        payload = jwt_payload_handler(user)

        return {
          'token': jwt_encode_handler(payload),
          'user': user
        }
      else:
        return attrs
