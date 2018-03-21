from django.urls import include, path
from . import views

urlpatterns = [
    path('index/', views.register, name='customer_register'),
]