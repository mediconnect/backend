from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import routers,filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import PatientSerializer
from .models import Patient
from customer.models import Customer

from django.urls import path
from django_filters.rest_framework import DjangoFilterBackend


class PatientViewSet(ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Patient.objects.filter(customer_id=customer_id)

    def create(self,request,*args,**kwargs):
        customer_id = self.kwargs['customer_id']
        data = request.data.copy()
        data['customer'] = customer_id
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(serializer.errors,status=400)
        # super(PatientViewSet, self).create(request,*args, **kwargs)


class ListAllPatients(ListAPIView):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend,)
    filter_fields = '__all__'
    search_fields = ('=first_name','=last_name')
    ordering_fields = ('customer','first_name','last_name','id')

    # def get_queryset(self):
    #     """
    #     Filter/sort by query params in url
    #     """
    #     queryset = Patient.objects.all()
    #     query_dic = {}
    #
    #     for field in Patient._meta.get_fields():
    #         if field.name in self.request.query_params:
    #             query_dic[field.name] = self.request.query_params.get(field.name)
    #     queryset = queryset.filter(**query_dic)
    #     order_by = self.request.query_params.get('_order',None)
    #     if order_by:
    #         queryset.order_by(order_by)
    #     return queryset


router = routers.SimpleRouter()
router.register(r'customer/(?P<customer_id>[^/.]+)',
                PatientViewSet,
                base_name='patient')
urlpatterns = router.urls + \
              [
                  path(r'patients/',
                       ListAllPatients.as_view(),
                       name='list-all-patients'),
              ]
