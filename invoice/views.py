from rest_framework import generics

from invoice.models import Order
from invoice.serializers import OrderSerializer


class OrderList(generics.ListCreateAPIView):
  """
  get:
  Return a list of all the existing orders.
  post:
  Create a new order instance.
  """
  queryset = Order.objects.all()
  serializer_class = OrderSerializer
  filter_fields = {'customer': ['exact'], 'date': ['range', 'exact']}


# TODO completar el servicio para el cliente
class CustomerList(generics.ListAPIView):
  pass
