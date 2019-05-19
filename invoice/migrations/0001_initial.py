# Generated by Django 2.1.7 on 2019-03-12 19:17
from django.contrib.auth.models import User
from django.db import migrations, models
import django.db.models.deletion

from invoice.models import Customer, Product, AvailableProduct


def create_superuser(apps, schema_editor):
  superuser = User()
  superuser.is_active = True
  superuser.is_superuser = True
  superuser.is_staff = True
  superuser.username = 'sistema'
  superuser.email = 'test@grupomeiko.com'
  superuser.set_password('d2hZ$u%5xvUc#2DY6ekLYiD#naXcjg%z')
  superuser.save(using=schema_editor.connection.alias)


def create_data(apps, schema_editor):
  Customer.objects.create(name="Jose Moreno", email="jose@grupomeiko.com")
  Customer.objects.create(name="Andrea Barragan",
                          email="andrea@grupomeiko.com")
  Customer.objects.create(name="Nicolas Posada",
                          email="nicolas@grupomeiko.com")
  Customer.objects.create(name="Martin Arias", email="martin@grupomeiko.com")
  Customer.objects.create(name="Camila Cardona", email="camila@grupomeiko.com")

  Product.objects.create(name="Arroz", price=1200,
                         product_description="libra")
  Product.objects.create(name="Lenteja", price=2000,
                         product_description="libra")
  Product.objects.create(name="Garbanzo", price=2350,
                         product_description="libra")
  Product.objects.create(name="Frijol", price=1900,
                         product_description="libra")
  Product.objects.create(name="Pasta", price=1500,
                         product_description="libra")
  Product.objects.create(name="Panela", price=800,
                         product_description="libra")
  Product.objects.create(name="Tomate", price=950,
                         product_description="libra")

  AvailableProduct.objects.create(customer_id=1, product_id=1)
  AvailableProduct.objects.create(customer_id=1, product_id=2)
  AvailableProduct.objects.create(customer_id=1, product_id=3)
  AvailableProduct.objects.create(customer_id=1, product_id=4)
  AvailableProduct.objects.create(customer_id=1, product_id=5)

  AvailableProduct.objects.create(customer_id=2, product_id=2)
  AvailableProduct.objects.create(customer_id=2, product_id=3)
  AvailableProduct.objects.create(customer_id=2, product_id=4)
  AvailableProduct.objects.create(customer_id=2, product_id=5)
  AvailableProduct.objects.create(customer_id=2, product_id=6)

  AvailableProduct.objects.create(customer_id=3, product_id=3)
  AvailableProduct.objects.create(customer_id=3, product_id=4)
  AvailableProduct.objects.create(customer_id=3, product_id=5)
  AvailableProduct.objects.create(customer_id=3, product_id=6)
  AvailableProduct.objects.create(customer_id=3, product_id=7)

  AvailableProduct.objects.create(customer_id=4, product_id=1)
  AvailableProduct.objects.create(customer_id=4, product_id=3)
  AvailableProduct.objects.create(customer_id=4, product_id=5)
  AvailableProduct.objects.create(customer_id=4, product_id=7)

  AvailableProduct.objects.create(customer_id=5, product_id=2)
  AvailableProduct.objects.create(customer_id=5, product_id=4)
  AvailableProduct.objects.create(customer_id=5, product_id=6)


class Migration(migrations.Migration):
  initial = True

  dependencies = [
  ]

  operations = [
    migrations.RunPython(create_superuser),
    migrations.CreateModel(
      name='AvailableProduct',
      fields=[
        ('id',
         models.AutoField(auto_created=True, primary_key=True, serialize=False,
                          verbose_name='ID')),
      ],
    ),
    migrations.CreateModel(
      name='Customer',
      fields=[
        ('id',
         models.AutoField(auto_created=True, primary_key=True, serialize=False,
                          verbose_name='ID')),
        ('name', models.CharField(max_length=100)),
        ('email', models.EmailField(max_length=254)),
      ],
    ),
    migrations.CreateModel(
      name='Order',
      fields=[
        ('id',
         models.AutoField(auto_created=True, primary_key=True, serialize=False,
                          verbose_name='ID')),
        ('delivery_address',
         models.CharField(help_text='customer delivery address',
                          max_length=100)),
        ('date', models.DateField(help_text='date order processing')),
        ('customer', models.ForeignKey(
          help_text='customer who made the order',
          on_delete=django.db.models.deletion.CASCADE,
          to='invoice.Customer'
        )),
      ],
    ),
    migrations.CreateModel(
      name='OrderDetail',
      fields=[
        ('id',
         models.AutoField(auto_created=True, primary_key=True, serialize=False,
                          verbose_name='ID')),
        ('quantity', models.PositiveIntegerField()),
        ('order',
         models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                           to='invoice.Order')),
      ],
    ),
    migrations.CreateModel(
      name='Product',
      fields=[
        ('id',
         models.AutoField(auto_created=True, primary_key=True, serialize=False,
                          verbose_name='ID')),
        ('name', models.CharField(max_length=100)),
        ('price', models.PositiveIntegerField()),
        ('product_description', models.TextField()),
      ],
      options={
        'ordering': ('name',),
      },
    ),
    migrations.AddField(
      model_name='orderdetail',
      name='product',
      field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                              to='invoice.Product'),
    ),
    migrations.AddField(
      model_name='availableproduct',
      name='customer',
      field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                              to='invoice.Customer'),
    ),
    migrations.AddField(
      model_name='availableproduct',
      name='product',
      field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                              to='invoice.Product'),
    ),
    migrations.RunPython(create_data),
  ]