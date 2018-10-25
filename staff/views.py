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
from django.urls import path

# other
from .serializers import TranslatorSerializer, SupervisorSerializer,\
    StaffLoginSerializer
from customer.serializers import CustomerRegistrationSerializer

from atlas.permissions import SupPermission
from user.serializers import UserRegistrationSerializer


class UserViewSet(ModelViewSet):

    """ View for handling creating different types of users request. """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permissions_classes = ( SupPermission,)

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

router = routers.SimpleRouter()
router.register(r'supervisor/user', UserViewSet)
urlpatterns = router.urls+\
              [path('staff/login/', Login.as_view(), name='staff-login'),]
