#!/usr/bin/env python
# -*- coding: utf-8 -*-
# rest framework

from rest_framework import routers, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# django
from django.contrib.auth.models import User
from django.urls import path, re_path
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

# other
from .serializers import TranslatorSerializer, SupervisorSerializer,\
    StaffLoginSerializer
from customer.serializers import CustomerRegistrationSerializer, CustomerProfileSerializer
from atlas.permissions import SupPermission
from user.serializers import UserRegistrationSerializer,UserSerializer
from .models.supervisor import Supervisor
from .models.translator import Translator
from customer.models import Customer
from reservation.models import Reservation
import uuid


class UserViewSet(ModelViewSet):

    """ View for handling creating different types of users request. """
    # serializer_class = UserSerializer
    filter_backends = (filters.OrderingFilter,DjangoFilterBackend,)
    filter_fields = '__all__'
    ordering_fields = '__all__'
    # permissions_classes = ( SupPermission,)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action in ['retrieve','list']:
            if 'role' not in self.request.query_params:
                return UserSerializer
            elif self.request.query_params['role'] == 0:
                return CustomerProfileSerializer
            elif self.request.query_params['role'] == 1:
                return SupervisorSerializer
            elif self.request.query_params['role'] in [2,3]:
                return TranslatorSerializer
        return UserSerializer

    def get_queryset(self):
        if self.action in ['retrieve','list']:
            if 'role' not in self.request.query_params:
                return User.objects.all()
            elif self.request.query_params['role'] == 0:
                return Customer.objects.all()
            elif self.request.query_params['role'] == 1:
                return Supervisor.objects.all()
            elif self.request.query_params['role'] in [2,3]:
                return Translator.objects.all()
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        # Validating our serializer from the UserRegistrationSerializer
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Everything's valid, so send it to the different type of User serializer
            user = serializer.save()
            if request.data['role'] == 0: # customer
                auth = {
                    'email': request.data['email'],
                    'password': request.data['password'],
                    'password_confirmation': request.data['confirmed_password'],
                    'first_name': request.data['first_name'],
                    'last_name': request.data['last_name']
                }
                customer = {
                    'tel': serializer.validated_data['tel'],
                    'address': serializer.validated_data['address']
                }
                data = {
                    'customer':customer,
                    'auth':auth
                }
                data['customer']['user'] = user.id
                customer = CustomerRegistrationSerializer(
                    data=data['customer']
                )
                if customer.is_valid(raise_exception=True):
                    customer.save()
                    return Response({'msg':'created',
                                     'user_id':user.id,
                                     'role': 'customer',
                                     'customer_id':Customer.objects.get(user=user).id},status=201)
                else:
                    user.delete()

            elif request.data['role'] == 1:  # supervisor
                data = {
                    'user':user.id,
                    'role':request.data['role']
                }

                supervisor_serializer = SupervisorSerializer(data=data)

                if supervisor_serializer.is_valid(raise_exception=True):
                    supervisor = supervisor_serializer.save()
                    return Response({'msg':'created',
                                     'user_id':user.id,
                                     'role':'supervisor',
                                     'staff_id':Supervisor.objects.get(user=user).id},status=201)
                else:
                    user.delete()

            elif request.data['role'] == 2:  # translator C2E
                data = {
                    'user':user.id,
                    'role':request.data['role']
                }
                trans = TranslatorSerializer(data=data)
                if trans.is_valid(raise_exception=True):
                    trans.save()
                    return Response({'msg':'created',
                                     'user_id':user.id,
                                     'role':'translator_c2e',
                                     'staff_id':Translator.objects.get(user=user).id},status=201)
                else:
                    user.delete()

            elif request.data['role'] == 3:
                data = {
                    'user':user.id,
                    'role':request.data['role']
                }
                trans = TranslatorSerializer(data=data)
                if trans.is_valid(raise_exception=True):
                    trans.save()
                    return Response({'msg':'created',
                                     'user_id':user.id,
                                     'role':'translator_e2c',
                                     'staff_id':Translator.objects.get(user=user).id},status=201)
                else:
                    user.delete()


class Login(APIView):
    """ View for handling login request. """

    def post(self, request, format=None):
        errors = {}
        login_serializer = StaffLoginSerializer(data=request.data)
        if login_serializer.is_valid():
            user = login_serializer.login()
            staff = Supervisor.objects.filter(user=user).first()
            if staff:
                return Response({"msg": "success",
                                 "user_id":user.id,
                                 "staff_id":staff.id,
                                 "role":"supervisor"}, status=200)
            else:
                staff = Translator.objects.filter(user=user).first()
                if staff:
                    return Response({"msg": "success",
                                     "user_id":user.id,
                                     "staff_id":staff.id,
                                     "role":"translator"}, status=200)
                else:
                    return Response({"msg":"Invalid Login Type"},status=400)

        else:
            for field, msg in login_serializer.errors.items():
                errors[field] = msg[-1]
        return Response(errors, status=400)


class Assignments(APIView):
    """View for handling get staff assignments"""

    def get(self, request, *args, **kwargs):
        staff_id = self.kwargs['staff_id']
        query = {k:v for k,v in request.query_params.items() if v}
        if Supervisor.objects.filter(id=staff_id).exists():
            assignments = Reservation.objects.exclude(status=7).exclude(trans_status=12)
        elif Translator.objects.filter(id=staff_id).exists():
            assignments = Reservation.objects.filter(translator_id=staff_id).exclude(trans_status=12)
        else:
            return Response({'errors':'Not found'}, status=400)
        if query != {}:
            assignments.filter(**query)
        return Response({'assignments':assignments}, status=200)


class Summary(APIView):
    """View for handling staff summarize website"""

    def get(self, request, *args, **kwargs):
        staff_id = self.kwargs['staff_id']
        summary ={
            'num_reservation':None,
            'num_reservation_done':None,
            'num_reservation_translating':None,
            'num_reservation_approving':None
        }
        if Supervisor.objects.filter(id=staff_id).exists():
            summary['num_reservation'] = len(Reservation.objects.all())
            summary['num_reservation_done'] = len(Reservation.objects.filter(status=7))
            summary['num_reservation_translating'] = len(Reservation.objects.exclude(trans_status=5)
                                                         .exclude(trans_status=12)
                                                         .exclude(status=0)
                                                         .exclude(status=7))
            summary['num_reservation_approving'] = len(Reservation.objects.get(Q(trans_status=2)&Q(trans_status=8)))
        elif Translator.objects.filter(id=staff_id).exists():
            assignments = Reservation.objects.filter(translator_id=staff_id)
            translator = Translator.objects.get(id=staff_id)
            summary['num_reservation'] = len(assignments)
            summary['num_reservation_done'] = len(assignments.filter(trans_stauts=5 if translator.role == 1 else 11))
            summary['num_reservation_translating'] = \
                len(assignments.filter(trans_stauts=1 if translator.role == 1 else 7))
            summary['num_reservation_approving'] = len(assignments.filter(trans_status=2 if translator.role == 1 else 8))
        else:
            return Response({'errors': 'Not Found'},status=400)
        return Response(summary, status=200)


router = routers.DefaultRouter()
router.register(r'user', UserViewSet,base_name='staff-user')
urlpatterns = router.urls+\
              [
                  path('login', Login.as_view(), name='staff-login'),
                  re_path(r'assignment/(?P<staff_id>[^/.]+)$', Assignments.as_view(), name='staff-assignments'),
                  re_path(r'summary/(?P<staff_id>[^/.]+)$', Summary.as_view(), name='staff-summary'),

                ]
