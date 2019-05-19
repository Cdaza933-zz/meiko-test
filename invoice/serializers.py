from rest_framework import serializers

from invoice.models import AvailableProduct, Customer, Order, OrderDetail


class OrderSerializer(serializers.ModelSerializer):
  """
  order serializer.
  """
  total = serializers.SerializerMethodField(
    help_text='sum(quantity_i*product_price_i)')
  products = serializers.SerializerMethodField(
    help_text='comma separated list of products and quantities')
  order_details = serializers.JSONField(write_only=True,
                                        help_text='[{"product_id": 1,'
                                                  '"quantity": 2}]')

  # TODO completar el metodo para obtener el total
  def get_total(self, order):
    pass

  # TODO completar el metodo para obtener los productos
  def get_products(self, order):
    pass

  # TODO completar el metodo para crear una orden
  def create(self, validated_data):
    """
    Create and return a new `Order` instance, given the validated data.
    """
    pass

  # TODO completar el metodo para actualizar una orden
  def update(self, instance, validated_data):
    """
    Update and return an existing `Order` instance, given the validated data.
    """
    pass

  class Meta:
    model = Order
    fields = ('customer', 'id', 'delivery_address',
              'date', 'total', 'products', 'order_details')


class CustomerSerializer(serializers.ModelSerializer):
  """
  customer serializer.
  """
  text = serializers.SerializerMethodField(help_text='customer name')

  def get_text(self, customer):
    return customer.name

  class Meta:
    model = Customer
    fields = ('id', 'text')
