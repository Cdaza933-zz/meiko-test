from django.db.models.aggregates import Sum
from django.db.models.expressions import F
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
        return order.orderdetail_set.all().aggregate(total=Sum(F('quantity') * F('product__price')))['total']

    # TODO completar el metodo para obtener los productos
    def get_products(self, order):
        orders = order.orderdetail_set.all().values_list('product__name', 'quantity')
        products = ''
        for product, name in orders:
            products += '{} x {},'.format(product, name)
        return products[:-2]

    # TODO completar el metodo para crear una orden
    def create(self, validated_data):
        """
    Create and return a new `Order` instance, given the validated data.
    """
        order_details = validated_data.pop('order_details')
        created_by = validated_data['created_by']
        order = Order.objects.create(**validated_data)
        for order_detail in order_details:
            OrderDetail.objects.create(order=order, created_by=created_by, **order_detail)
        return order

    # TODO completar el metodo para actualizar una orden
    def update(self, instance, validated_data):
        """
    Update and return an existing `Order` instance, given the validated data.
    """
        instance.delivery_address = validated_data.pop('delivery_address')
        instance.save()
        return instance

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
