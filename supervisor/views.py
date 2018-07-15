#!/usr/bin/env python
# -*- coding: utf-8 -*-
# rest framework
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# django
from django.http import JsonResponse,Http404

# other
from .serializers import CreateUserSerializer,SupervisorLoginSerializer,\
    SupervisorSerializer
from translator.serializers import TranslatorSerializer
from customer.serializers import CustomerProfileSerializer
from .models import Supervisor
from translator.models import Translator
from customer.models import Customer
from atlas.permissions import SupPermission


class CreateUser(APIView):

    """ View for handling creating different types of users request. """
    #permissions_classes = (IsAuthenticated, SupervisorPermission,)

    def post(self, request):
        data = JSONParser().parse(request)
        errors = {}
        responseData = {
            'error':errors,
            'user_ID':None,
        }

        user_serializer = CreateUserSerializer(data=data)

        if user_serializer.is_valid():
            responseData['user_ID'] = user_serializer.create(data)
            return Response(responseData, status = status.HTTP_201_CREATED)

        if not user_serializer.is_valid():
            for field, msg in user_serializer.errors.items():
                responseData['errors'][field] = msg[-1]

        return Response(responseData, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    """ View for handling supervisor login request. """

    def post(self, request):
        data = JSONParser().parse(request)
        errors = {}

        supervisor_serializer = SupervisorLoginSerializer(data=data)
        if supervisor_serializer.is_valid():
            supervisor_serializer.login()
            return JsonResponse({"msg": "success"}, status=200)

        if not supervisor_serializer.is_valid():
            for field, msg in supervisor_serializer.errors.items():
                errors[field] = msg[-1]
        return JsonResponse(errors, status=400)


class SupervisorDetail(generics.RetrieveUpdateDestroyAPIView):

    """ Retrieve, update or delete a supervisor instance."""
    permissions_classes = (IsAuthenticated, SupPermission,)
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorSerializer


class SupervisorList(generics.ListAPIView):
    """ List all supervisors. """
    permissions_classes = (IsAuthenticated, SupPermission,)
    queryset = Supervisor.objects.all()
    serializer_class = SupervisorSerializer


class TranslatorDetail(generics.RetrieveUpdateDestroyAPIView):

    """ Retrieve, update or delete a translator instance."""
    permissions_classes = (IsAuthenticated, SupPermission,)
    queryset = Translator.objects.all()
    serializer_class = TranslatorSerializer


class TranslatorList(generics.ListAPIView):
    """ List all translators. """
    permissions_classes = (IsAuthenticated, SupPermission,)
    queryset = Translator.objects.all()
    serializer_class = TranslatorSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):

    """ Retrieve, update or delete a customer instance."""
    permissions_classes = (IsAuthenticated, SupPermission,)
    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer


class CustomerList(generics.ListAPIView):
    """ List all customers. """
    permissions_classes = (IsAuthenticated, SupPermission,)
    queryset = Customer.objects.all()
    serializer_class = CustomerProfileSerializer
