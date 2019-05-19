"""
invoice URL Configuration
"""
from django.urls import re_path

from invoice import views

app_name = 'invoice'
urlpatterns = [
  re_path(r'^order/$', views.OrderList.as_view()),
  re_path(r'^customer/$', views.CustomerList.as_view()),
]
