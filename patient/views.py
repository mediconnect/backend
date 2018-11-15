from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import routers,filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PatientSerializer
from .models import Patient
from customer.models import Customer
from atlas.permissions import IsOwner, SupPermission, IsOwnerOrStaff
from django.urls import path
from django_filters.rest_framework import DjangoFilterBackend


class PatientViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,IsOwnerOrStaff,IsOwner)
    serializer_class = PatientSerializer

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Patient.objects.filter(customer_id=customer_id)

    def create(self,request,*args,**kwargs):
        user = request.user
        if user.id != Customer.objects.get(id=self.kwargs['customer_id']).user_id:
            return Response({'error':'Not Allowed'},status=403)
        customer_id = int(self.kwargs['customer_id'])
        data = request.data.copy()
        data['customer'] = customer_id
        serializer = PatientSerializer(data=data)
        if serializer.is_valid():
            patient = serializer.save()
            return Response({'msg':'created',
                             'id':patient.id},
                            status=201)
        else:
            return Response(serializer.errors,status=400)
        # super(PatientViewSet, self).create(request,*args, **kwargs)

    # def list(self,request,*args,**kwargs):
    #     user = request.user
    #     if user.id != Customer.objects.get(id=self.kwargs['customer_id']).user_id:
    #         if not Supervisor.objects.filter(user_id=user.id).exists():
    #             return Response({'error':'Not Allowed'},status=403)
    #     else:
    #         return super(PatientViewSet, self).list(request,*args,**kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     customer_id = int(self.kwargs['customer_id'])
    #     user = request.user
    #     if user.id != Customer.objects.get(id=self.kwargs['customer_id']).user_id:
    #         if not Supervisor.objects.filter(user_id=user.id).exists():
    #             return Response({'error':'Not Allowed'},status=403)
    #     patient_id = self.kwargs['pk']
    #     patient = Patient.objects.get(id=patient_id)
    #     if patient.customer.id != customer_id:
    #         return Response({'error':'Not Allowed'},status=403)
    #     else:
    #         return super(PatientViewSet, self).retrieve(request,*args,**kwargs)

    # def update(self, request, *args, **kwargs):
    #     customer_id = int(self.kwargs['customer_id'])
    #     user = request.user
    #     if user.id != Customer.objects.get(id=self.kwargs['customer_id']).user_id:
    #         if not Supervisor.objects.filter(user_id=user.id).exists():
    #             return Response({'error':'Not Allowed'},status=403)
    #     patient_id = self.kwargs['pk']
    #     patient = Patient.objects.get(id=patient_id)
    #     if patient.customer.id != customer_id:
    #         return Response({'error':'Not Allowed'},status=403)
    #     else:
    #         return super(PatientViewSet, self).update(request,*args,**kwargs)
    #
    # def destroy(self, request, *args, **kwargs):
    #     customer_id = int(self.kwargs['customer_id'])
    #     user = request.user
    #     if user.id != Customer.objects.get(id=self.kwargs['customer_id']).user_id:
    #         if not Supervisor.objects.filter(user_id=user.id).exists():
    #             return Response({'error':'Not Allowed'},status=403)
    #     patient_id = self.kwargs['pk']
    #     patient = Patient.objects.get(id=patient_id)
    #     if patient.customer.id != customer_id:
    #         return Response({'error':'Not Allowed'},status=403)
    #     else:
    #         return super(PatientViewSet, self).destroy(request,*args,**kwargs)


class ListAllPatients(ListAPIView):
    permission_classes = (SupPermission,)
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,DjangoFilterBackend,)
    filter_fields = '__all__'
    search_fields = ('=first_name','=last_name')
    ordering_fields = ('customer','first_name','last_name','id')


router = routers.SimpleRouter()
router.register(r'customer/(?P<customer_id>[^/.]+)/patient',
                PatientViewSet,
                base_name='patient')
urlpatterns = router.urls + \
              [
                  path(r'patients/',
                       ListAllPatients.as_view(),
                       name='list-all-patients'),
              ]
