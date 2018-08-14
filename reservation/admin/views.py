#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest framework

from rest_framework.views import APIView
from rest_framework import routers
from rest_framework.response import Response

# django
from django.http.request import QueryDict

# other
from atlas.permissions import SupPermission
from .serializers import ReservationUpdateSerializer,ValidationSerializer
from reservation.models import Reservation

class UpdateReservation(APIView):

    permission_classes = [SupPermission]

    def post(self, request, format=None):

        resid = request.data['resid']
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
        print(payload)

        validation_serializer = ValidationSerializer(data=payload)

        if validation_serializer.is_valid():

            return Response({'Msg':'Allowed'},status=202)
        else:
            errors = {}
            for field, msg in validation_serializer.errors.items():
                errors[field] = msg[-1]
        return Response({'Error':'Illegal Operation'},status=403)

from django.urls import path

urlpatterns = [path('reservation/manage/',
                    UpdateReservation.as_view(),
                    name='manage-reservation'),
               path('auth/validate',
                    ValidateOperation.as_view(),
                    name='validate-operation'),]