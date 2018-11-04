from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import PatientSerializer
from .models import Patient
from customer.models import Customer

from django.urls import path


class PatientViewSet(ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        query = {k:v for k,v in self.request.query_params.items() if v}
        if query != {}:
            queryset = Patient.objects.filter(**query)
        else:
            queryset = Patient.objects.all()
        return queryset

    def create(self, request, *args,customer_id=None, **kwargs):
        data = request.data.copy()
        data['customer'] = customer_id
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(serializer.errors,status=400)
        # super(PatientViewSet, self).create(request,*args, **kwargs)

    def list(self, request, *args, customer_id=None,**kwargs):
        if self.queryset:
            return Response(self.queryset.filter(user=customer_id),
                            status=200)
        else:
            return Response({'errors':'Not Found'},status=400)


class ListAllPatients(ListAPIView):
    serializer_class = PatientSerializer

    def get_queryset(self):
        query = {k:v for k,v in self.request.query_params.items() if v}
        if query != {}:
            queryset = Patient.objects.filter(**query)
        else:
            queryset = Patient.objects.all()
        return queryset


router = routers.SimpleRouter()
router.register(r'customer/(?P<customer_id>[^/.]+)', PatientViewSet,base_name='patient')
urlpatterns = router.urls + \
              [
                  path(r'patients',
                       ListAllPatients.as_view(),
                       name='list-all-patients'),
              ]
