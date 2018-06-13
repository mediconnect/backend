from django.urls import path
from . import views

urlpatterns = [
    path('list_supervisors/',views.SupervisorList.as_view(),name='supervisor-list'),
    path('detail_supervisor/<user_id>/',views.SupervisorDetail.as_view(),name='supervisor-detail'),
    path('list_customer/',views.CustomerList.as_view(),name='customer-list'),
    path('detail_customer/<user_id>/',views.CustomerDetail.as_view(),name='customer-detail'),
    path('list_translator/',views.CustomerList.as_view(),name='translator-list'),
    path('detail_translator/<user_id>/',views.CustomerDetail.as_view(),name='translator-detail'),

    path('create_user/',views.CreateUser.as_view(),name='create-user'),
    path('login/',views.Login.as_view(),name='supervisor-login')
]
