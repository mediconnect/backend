#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

# rest framework

from rest_framework import routers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# django
from django.contrib.auth.models import User
from django.urls import path, re_path
from django.db.models import Q

# other
from .serializers import TranslatorSerializer, SupervisorSerializer,\
    StaffLoginSerializer
from customer.serializers import CustomerRegistrationSerializer
from atlas.permissions import SupPermission
from user.serializers import UserRegistrationSerializer,UserSerializer
from .models.supervisor import Supervisor
from .models.translator import Translator
from reservation.models import Reservation


class UserViewSet(ModelViewSet):

    """ View for handling creating different types of users request. """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permissions_classes = ( SupPermission,)

    def create(self, request, *args, **kwargs):
        # Validating our serializer from the UserRegistrationSerializer
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # Everything's valid, so send it to the different type of User serializer
            user = serializer.save()

            if request.data['role'] == 0: # customer

                request.data['customer']['user'] = user.id

                customer_serializer = CustomerRegistrationSerializer(
                    data=request.data['customer']
                )
                if customer_serializer.is_valid(raise_exception=True):
                    customer_serializer.save()

            elif request.data['role'] == 1:  # supervisor

                supervisor_serializer = SupervisorSerializer(data = {'user':user.id})

                if supervisor_serializer.is_valid(raise_exception=True):
                    supervisor_serializer.save()

            elif request.data['role'] == 2:  # translator C2E
                trans_serializer = TranslatorSerializer(data = {'user':user.id,
                                                                'role':0})
                if trans_serializer.is_valid(raise_exception=True):
                    trans_serializer.save()

            elif request.data['role'] == 3:
                trans_serializer = TranslatorSerializer(data = {'user':user.id,
                                                                'role':1})
                if trans_serializer.is_valid(raise_exception=True):
                    trans_serializer.save()

        return Response({'msg':'created','id':user.id},status=201)


class Login(APIView):
    """ View for handling login request. """

    def post(self, request, format=None):
        errors = {}
        login_serializer = StaffLoginSerializer(data=request.data)
        if login_serializer.is_valid():
            login_serializer.login()
            return Response({"msg": "success"}, status=200)

        else:
            for field, msg in login_serializer.errors.items():
                errors[field] = msg[-1]
        return Response(errors, status=400)


class Assignments(APIView):
    """View for handling get staff assignments"""

    def get(self, request, *args, user_id, **kwargs):
        query = {k:v for k,v in request.query_params.items() if v}
        if Supervisor.objects.filter(user_id=user_id).exists():
            assignments = Reservation.objects.exclude(status=7).exclude(trans_status=12)
        elif Translator.objects.filter(user_id=user_id).exists():
            assignments = Reservation.objects.filter(translator_id__user=user_id).exclude(trans_status=12)
        else:
            return Response({'errors':'Not found'},status=400)
        if query != {}:
            assignments.filter(**query)
        return Response({'assignments':assignments},status=200)


class Summary(APIView):
    """View for handling staff summarize website"""

    def get(self, request, *args, user_id, **kwargs):
        summary ={
            'num_reservation':None,
            'num_reservation_done':None,
            'num_reservation_translating':None,
            'num_reservation_approving':None
        }
        if Supervisor.objects.filter(user_id=user_id).exists():
            summary['num_reservation'] = len(Reservation.objects.all())
            summary['num_reservation_done'] = len(Reservation.objects.filter(status=7))
            summary['num_reservation_translating'] = len(Reservation.objects.exclude(trans_status=5)
                                                         .exclude(trans_status=12)
                                                         .exclude(status=0)
                                                         .exclude(status=7))
            summary['num_reservation_approving'] = len(Reservation.objects.get(Q(trans_status=2)&Q(trans_status=8)))
        elif Translator.objects.filter(user_id=user_id).exists():
            assignments = Reservation.objects.filter(translator_id__user=user_id)
            translator = Translator.objects.get(user_id=user_id)
            summary['num_reservation'] = len(assignments)
            summary['num_reservation_done'] = len(assignments.filter(trans_stauts=5 if translator.role == 1 else 11))
            summary['num_reservation_translating'] = \
                len(assignments.filter(trans_stauts=1 if translator.role == 1 else 7))
            summary['num_reservation_approving'] = len(assignments.filter(trans_status=2 if translator.role==1 else 8))
        else:
            return Response({'errors':'Not Found'},status=400)
        return Response(summary,status=200)


router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
urlpatterns = router.urls+\
              [
                  path('login', Login.as_view(), name='staff-login'),
                  re_path(r'assignment/(?P<user_id>[^/.]+)/$', Assignments.as_view(), name='staff-assignments'),
                  re_path(r'summary/(?P<user_id>[^/.]+)', Summary.as_view(), name='staff-summary'),

               ]
