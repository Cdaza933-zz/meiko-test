from django.test import TestCase
import pycodestyle
from rest_framework import status
from rest_framework.test import APIClient


class DatoTestCase(TestCase):
  factory = APIClient()

  def test_login_get(self):
    response = self.factory.get('/api-token-auth/')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

  def test_login_post_bad_request(self):
    response = self.factory.post('/api-token-auth/')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_login_post_ok(self):
    data = {
      "correo": "test@grupomeiko.com",
      "contrasenia": "d2hZ$u%5xvUc#2DY6ekLYiD#naXcjg%z"
    }
    response = self.factory.post('/api-token-auth/', data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_login_post_unprocessable_entity(self):
    data = {
      "correo": "test@grupomeiko.com",
      "contrasenia": "1sdf32fa1465aa879rwe"
    }
    response = self.factory.post('/api-token-auth/', data)
    self.assertEqual(response.status_code,
                     status.HTTP_422_UNPROCESSABLE_ENTITY)

  def test_customer_get_unauthorized(self):
    response = self.factory.get('/tendencia/categorias/')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_orders_get_unauthorized(self):
    response = self.factory.get('/tendencia/matrices/')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_conformance(self):
    """Test that we conform to PEP-8."""
    style = pycodestyle.StyleGuide(quiet=False, config_file='mypy.ini')
    result = style.check_files(['invoice'])
    self.assertEqual(result.total_errors, 0,
                     "Found code style errors (and warnings).")

  # TODO crear pruebas unitarias para los servicios
