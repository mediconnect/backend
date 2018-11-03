#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest framework

from rest_framework.views import APIView
from rest_framework import routers
from rest_framework.response import Response

# django
from django.http.request import QueryDict
from django.urls import path
from django.contrib.auth.models import User
from django.core.mail import send_mail

# other
from atlas.permissions import SupPermission
from .serializers import ReservationUpdateSerializer,ValidationSerializer
from reservation.models import Reservation


class UpdateReservation(APIView):

    permission_classes = [SupPermission]

    def post(self, request, format=None):

        resid = request.data['res_id']
        reservation = Reservation.objects.get(res_id=resid)

        updated_fields = {k: v for k, v in request.data.items()}

        for attr, value in updated_fields.items():
            setattr(reservation, attr, value)

        reservation.save()

        return Response({'updated_fields': list(updated_fields.keys())},status=200)


class ValidateOperation(APIView):

    def post(self, request,format=None):
        payload = request.data.copy()
        payload['user_id'] = request.user.id

        validation_serializer = ValidationSerializer(data=payload)

        if validation_serializer.is_valid():

            return Response({'Msg':'Allowed'},status=202)
        else:
            errors = {}
            for field, msg in validation_serializer.errors.items():
                errors[field] = msg[-1]
        return Response({'Error':'Illegal Operation'},status=403)


class StaffSendEmail(APIView):

    def post(self,request):
        content = request.data['content']
        user_id =  request.data['user_id']
        user =  User.objects.get(user_id=user_id)
        errors = send_mail(
            '',
            content,
            user.email,
            'gabrielwry@gmail.com',
            fail_silently=False,
        )
        return Response({'errors':errors},status=200)


urlpatterns = [path('api/reservation/admin/',
                    UpdateReservation.as_view(),
                    name='manage-reservation'),
               path('api/auth/validate',
                    ValidateOperation.as_view(),
                    name='validate-operation'),
               path('api/auth/send',
                    StaffSendEmail.as_view(),
                    name='staff-send-email')
               ]