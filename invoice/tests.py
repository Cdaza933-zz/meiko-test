import json

from django.contrib.auth.models import User
from django.test import TestCase
import pycodestyle
from rest_framework import status
from rest_framework.test import APIClient

from invoice.models import Product, Customer, AvailableProduct


class DatoTestCase(TestCase):
  factory = APIClient()

  def setUp(self):
    user = User.objects.create_user('test1', 'test1@grupomeiko.com', 'd2hZ$u%5xvUc#2DY6ekLYiD#naXcjg%z')
    customer = Customer.objects.create(name='customer test', email='customent.test@email.co', created_by=user)
    product_1 = Product.objects.create(name='arroz', price=1500, product_description='grano', created_by=user)
    product_2 = Product.objects.create(name='cafe', price=1390, product_description='instantaneo', created_by=user)
    product_3 = Product.objects.create(name='garbanzo', price=2500, product_description='grano', created_by=user)
    product_4 = Product.objects.create(name='milo', price=5900, product_description='chocolate', created_by=user)
    product_5 = Product.objects.create(name='frijol', price=1900, product_description='grano', created_by=user)
    product_6 = Product.objects.create(name='atun', price=9740, product_description='pez', created_by=user)
    product_7 = Product.objects.create(name='alpinito', price=5200, product_description='lactio', created_by=user)
    product_8 = Product.objects.create(name='leche', price=32500, product_description='lactio', created_by=user)
    product_9 = Product.objects.create(name='sal', price=5210, product_description='condimento', created_by=user)
    product_10 = Product.objects.create(name='pimienta', price=13400, product_description='condimento', created_by=user)
    product_11 = Product.objects.create(name='azucar', price=4500, product_description='azucar', created_by=user)
    product_12 = Product.objects.create(name='chocolate', price=5560, product_description='chocolate', created_by=user)
    product_13 = Product.objects.create(name='maiz', price=3560, product_description='verdura', created_by=user)
    product_14 = Product.objects.create(name='manzana', price=9850, product_description='fruta', created_by=user)
    product_15 = Product.objects.create(name='mango', price=9086, product_description='fruta', created_by=user)
    AvailableProduct.objects.create(product=product_1, customer=customer, created_by=user)
    AvailableProduct.objects.create(product=product_3, customer=customer, created_by=user)
    AvailableProduct.objects.create(product=product_4, customer=customer, created_by=user)
    AvailableProduct.objects.create(product=product_9, customer=customer, created_by=user)
    AvailableProduct.objects.create(product=product_13, customer=customer, created_by=user)
    AvailableProduct.objects.create(product=product_7, customer=customer, created_by=user)


  def test_login_get(self):
    response = self.factory.get('/api-token-auth/')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

  def test_login_post_bad_request(self):
    response = self.factory.post('/api-token-auth/')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

  def test_login_post_ok(self):
    data = {
      "correo": "test1@grupomeiko.com",
      "contrasenia": "d2hZ$u%5xvUc#2DY6ekLYiD#naXcjg%z"
    }
    response = self.factory.post('/api-token-auth/', data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_create_create_order_more_than_five_products(self):
    data = {
      "correo": "test1@grupomeiko.com",
      "contrasenia": "d2hZ$u%5xvUc#2DY6ekLYiD#naXcjg%z"
    }
    response = self.factory.post('/api-token-auth/', data)
    token = response.json()['token']
    order_data = {
      "customer": 1,
      "delivery_address": "Diagonal 86a # 101 - 40",
      "date": "2018-10-06",
      "order_details": [
        {
          "product_id": 1,
          "quantity": 2
        },
        {
          "product_id": 2,
          "quantity": 1
        },
        {
          "product_id": 3,
          "quantity": 41
        },
        {
          "product_id": 4,
          "quantity": 23
        },
        {
          "product_id": 5,
          "quantity": 43
        },
        {
          "product_id": 6,
          "quantity": 89
        }
      ]
    }
    self.factory.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    order_response = self.factory.post('/invoice/order/', json.dumps(order_data), content_type="application/json")

    self.assertEqual(order_response.status_code,
                     status.HTTP_403_FORBIDDEN)
    self.assertEqual(order_response.data, 'cant process orders with more than 5 products')

  def test_create_create_order_restricted(self):
    data = {
      "correo": "test1@grupomeiko.com",
      "contrasenia": "d2hZ$u%5xvUc#2DY6ekLYiD#naXcjg%z"
    }
    response = self.factory.post('/api-token-auth/', data)
    token = response.json()['token']
    order_data = {
      "customer": 1,
      "delivery_address": "Diagonal 86a # 101 - 40",
      "date": "2018-10-06",
      "order_details": [
        {
          "product_id": 1,
          "quantity": 2
        },
        {
          "product_id": 2,
          "quantity": 1
        },
        {
          "product_id": 3,
          "quantity": 41
        },
        {
          "product_id": 4,
          "quantity": 23
        }
      ]
    }
    self.factory.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    order_response = self.factory.post('/invoice/order/', json.dumps(order_data), content_type="application/json")

    self.assertEqual(order_response.status_code,
                     status.HTTP_403_FORBIDDEN)
    self.assertEqual(order_response.data, 'some products are restricted for this client')

  def test_create_create_order_successful(self):
    data = {
      "correo": "test1@grupomeiko.com",
      "contrasenia": "d2hZ$u%5xvUc#2DY6ekLYiD#naXcjg%z"
    }
    response = self.factory.post('/api-token-auth/', data)
    token = response.json()['token']
    order_data = {
      "customer": 1,
      "delivery_address": "Diagonal 86a # 101 - 40",
      "date": "2018-10-06",
      "order_details": [
        {
          "product_id": 1,
          "quantity": 22
        },
        {
          "product_id": 7,
          "quantity": 14
        },
        {
          "product_id": 3,
          "quantity": 41
        },
        {
          "product_id": 4,
          "quantity": 23
        }
      ]
    }
    self.factory.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    order_response = self.factory.post('/invoice/order/', json.dumps(order_data), content_type="application/json")

    self.assertEqual(order_response.status_code,
                     status.HTTP_201_CREATED)

  def test_check_order_for_client(self):
    data = {
      "correo": "test1@grupomeiko.com",
      "contrasenia": "d2hZ$u%5xvUc#2DY6ekLYiD#naXcjg%z"
    }
    response = self.factory.post('/api-token-auth/', data)
    token = response.json()['token']
    self.test_create_create_order_successful()
    self.factory.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    customer = 1
    order_response = self.factory.get('/invoice/order/?customer={}'.format(customer))

    self.assertEqual(order_response.status_code,
                     status.HTTP_200_OK)
    order_details = [
      {
        "product_id": 1,
        "quantity": 22,
        "name":"arroz" ,
      },
      {
        "product_id": 7,
        "quantity": 14,
        "name": "alpinito"

      },
      {
        "product_id": 3,
        "quantity": 41,
        "name": "alpinito"
      },
      {
        "product_id": 4,
        "quantity": 23,
        "name": "alpinito"
      }
    ]
    all_order_data = order_response.json()
    for order_data in all_order_data:
      self.assertEqual(order_data['customer'],
                       customer)
      total = sum([Product.objects.get(pk=detail['product_id']).price * detail['quantity'] for detail in order_details])
      self.assertEqual(order_data['total'],
                       total)
      for test in order_details:
        self.assertTrue(test["name"] in order_data["products"])

  def test_check_order_for_client_in_exact_date(self):
    self.test_create_create_order_successful()
    data = {
      "correo": "test1@grupomeiko.com",
      "contrasenia": "d2hZ$u%5xvUc#2DY6ekLYiD#naXcjg%z"
    }
    response = self.factory.post('/api-token-auth/', data)
    token = response.json()['token']
    customer = 1
    check_date = '2018-10-06'
    order_data = {
      "customer": 1,
      "delivery_address": "Diagonal 86a # 101 - 40",
      "date": "2017-11-06",
      "order_details": [
        {
          "product_id": 1,
          "quantity": 22
        },
        {
          "product_id": 7,
          "quantity": 14
        },
        {
          "product_id": 3,
          "quantity": 41
        },
        {
          "product_id": 4,
          "quantity": 23
        }
      ]
    }
    self.factory.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    self.factory.post('/invoice/order/', json.dumps(order_data), content_type="application/json")
    order_data = {
      "customer": 1,
      "delivery_address": "Diagonal 86a # 101 - 40",
      "date": "2018-11-06",
      "order_details": [
        {
          "product_id": 1,
          "quantity": 322
        },
        {
          "product_id": 7,
          "quantity": 142
        },
        {
          "product_id": 13,
          "quantity": 41
        },
        {
          "product_id": 9,
          "quantity": 23
        }
      ]
    }
    self.factory.post('/invoice/order/', json.dumps(order_data), content_type="application/json")
    order_response = self.factory.get('/invoice/order/?customer={}&date={}'.format(customer, check_date))
    order_data = order_response.json()
    self.assertTrue(len(order_data) == 1)

  def test_check_order_for_client_between_date(self):
    self.test_check_order_for_client_in_exact_date()
    customer = 1
    check_date__gte = '2017-01-01'
    check_date__lte = '2018-12-01'
    order_response = self.factory.get('/invoice/order/?customer={}&date__range={},{}'.format(
      customer, check_date__gte, check_date__lte))
    order_data = order_response.json()
    self.assertTrue(len(order_data) == 3)


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
