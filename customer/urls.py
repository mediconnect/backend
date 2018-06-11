from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.Register.as_view(), name='customer_register'),
    path('login/', views.Login.as_view(), name='customer_login'),
    path('profile/', views.Profile.as_view(), name='customer_profile')
]
