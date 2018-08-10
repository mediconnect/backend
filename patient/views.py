from rest_framework.viewsets import ModelViewSet
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import  PatientSerializer
from .models import Patient
from customer.models import Customer


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def create(self, request, *args, **kwargs):

        user = request.user
        request.data['user'] = Customer.objects.get(user=user).id
        serializer = PatientSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(serializer.errors,status=400)
        # super(PatientViewSet, self).create(request,*args, **kwargs)


router = routers.SimpleRouter()
router.register(r'patient', PatientViewSet)
urlpatterns = router.urls
