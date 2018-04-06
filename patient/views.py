from django.http import JsonResponse
from atlas.guarantor import use_serializer
from atlas.locator import AModule
from rest_framework.views import APIView
from .serializers import PatientSerializer

patient_module = AModule()

@patient_module.route("create", name="patient_create")
class Create(APIView):

    @use_serializer(Serializer=PatientSerializer)
    def post(self, data, request=None):
        return JsonResponse(data, status=200)
