# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Adjust the view name accordingly
]