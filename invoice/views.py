from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from invoice.models import Order, Customer, AvailableProduct
from invoice.serializers import OrderSerializer, CustomerSerializer
from utils.rest_framework.authentication import TokenAuthentication


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
  authentication_classes = (TokenAuthentication,)
  def post(self, request, format=None):
    user = request.user
    data = request.data
    data['created_by'] = user
    customer = Customer.objects.get(pk=data.pop('customer'))
    data['customer'] = customer
    products = [order['product_id'] for order in data['order_details']]
    if len(products) > 5:
      return Response('cant process orders with more than 5 products', status=status.HTTP_403_FORBIDDEN)
    if not AvailableProduct.objects.filter(customer=customer, product_id__in=products).count() < len(products):
      return Response('some products are restricted for this client', status=status.HTTP_403_FORBIDDEN)
    OrderSerializer().create(data)
    return Response(status=status.HTTP_201_CREATED)


# TODO completar el servicio para el cliente
class CustomerList(APIView):
  queryset = Customer.objects.all()
  authentication_classes = (TokenAuthentication,)

  def post(self, request, format=None):
    user = request.user
    data = request.data
    Customer.objects.create(**data, created_by=user)
    return Response(status=status.HTTP_201_CREATED)

  def get(self, request, format=None):
    return Response(CustomerSerializer(Customer.objects.all(), many=True).data, status=status.HTTP_200_OK)

  def patch(self, request, format=None):
    user = request.user
    data = request.data
    Customer.objects.filter(id=data['id']).update(**data, updated_by=user)
    return Response(status=status.HTTP_200_OK)

  def delete(self, request, pk):
    user = request.user
    Customer.objects.get(id=pk).delete(deleted_by=user)
    return Response(status=status.HTTP_200_OK)

