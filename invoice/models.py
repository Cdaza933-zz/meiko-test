from django.db import models


# TODO implementar clase de auditoria
from utils.django.db.models import Auditor


class Product(Auditor):
  """
  table for product.
  """

  name = models.CharField(max_length=100)
  price = models.PositiveIntegerField()
  product_description = models.TextField()

  class Meta:
    ordering = ('name',)

  def __str__(self):
    return "%s %s %s" % (self.name, self.price, self.product_description)


class Customer(Auditor):
  """
  table for customer.
  """

  name = models.CharField(max_length=100)
  email = models.EmailField()

  def __str__(self):
    return "%s - %s" % (self.name, self.email)


class AvailableProduct(Auditor):
  """
  table for available product.
  """

  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)

  def __str__(self):
    return "%s %s" % (self.customer, self.product)


class Order(Auditor):
  """
  table for order.
  """

  customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                               help_text='customer who made the order')
  delivery_address = models.CharField(max_length=100,
                                      help_text='customer delivery address')
  date = models.DateField(help_text='date order processing')

  def __str__(self):
    return "%s %s %s" % (self.customer, self.delivery_address, self.date)


class OrderDetail(Auditor):
  """
  table for order detail.
  """

  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()

  def __str__(self):
    return "%s %s %s" % (self.order, self.product, self.quantity)
