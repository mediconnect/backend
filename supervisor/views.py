#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

# rest framework
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import routers
from rest_framework.decorators import (api_view, permission_classes, action)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# django
from django.http import JsonResponse,Http404
from django.shortcuts import get_object_or_404

# other
from .serializers import SupervisorLoginSerializer
from translator.serializers import TranslatorSerializer
from customer.serializers import CustomerProfileSerializer
from reservation.serializers import ReservationSerializer
from reservation.models import Reservation
from .models import Supervisor
from translator.models import Translator
from customer.models import Customer
from django.contrib.auth.models import User
from atlas.permissions import SupPermission
from user.serializers import UserRegistrationSerializer,UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view


class CreateUserViewSet(ModelViewSet):

    """ View for handling creating different types of users request. """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permissions_classes = (IsAuthenticated, SupervisorPermission,)

    def create(self, request, *args, **kwargs):
        # Validating our serializer from the UserRegistrationSerializer
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Everything's valid, so send it to the UserSerializer
        model_serializer = UserSerializer().create(serializer.data)
        model_serializer.save()

        return Response({'id':model_serializer.id},status=201)

    @action(methods=['get'],detail=True)
    def info(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @permission_classes(SupPermission)
    def list(self, request,*args,**kwargs):
        user = request.user
        if not user:
            return JsonResponse(status=400)
        return super(CreateUserViewSet, self).list(request)

    def update(self, request, pk=None,*args,**kwargs):
        user = User.objects.filter(id=pk).first()
        if not user or request.user != user:
            return JsonResponse(status=400)
        return super(CreateUserViewSet, self).update(request)


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


class UpdateReservationStatus(APIView):
    """ View for handling reservation update"""
    lookup_field = 'id'
    serializer_class = ReservationSerializer
    permission_classes = []

    def get_object(self):
        queryset = Reservation.objects.all()
        filter = {}
        for field in self.lookup_field:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj

    def update_status(self, updated_fields, resid, format=None):
        reservation = self.get_object()
        for attr, value in updated_fields.items():
            setattr(reservation, attr, value)
        reservation.save()
        return JsonResponse({'updated_fields': list(updated_fields.keys())})


router = routers.SimpleRouter()
router.register(r'supervisor-create', CreateUserViewSet)
urlpatterns = router.urls
