import copy
from django.http import JsonResponse
from atlas.guarantor import use_serializer
from atlas.locator import AModule
from rest_framework.views import APIView
from .models import Patient
from .serializers import PatientSerializer, OptionalPatientSerializer

patient_module = AModule()

## For security reasons, change api to ~/customer/<customer_id>/patient/...? or ~/patient/<customer>/...

@patient_module.route("create", name="patient_create")
class Create(APIView):

    @use_serializer(Serializer=PatientSerializer)
    def post(self, serializer, format=None):
        posted = serializer.create(serializer.data)
        return JsonResponse(PatientSerializer(posted).data, status=200)


@patient_module.route(r"(?<ptid>.+?)/info$", name="patient_get")
class FetchRecord(APIView):

    def get(self, request, ptid, format=None):
        try:
            instance = Patient.objects.get(id=ptid)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        return JsonResponse(PatientSerializer(instance).data, status=200)


@patient_module.route(r"(?<ptid>.+?)/update$", name="patient_update")
class Update(APIView):

    @use_serializer(Serializer=OptionalPatientSerializer)
    def post(self, serializer, ptid, format=None):
        try:
            instance = Patient.objects.get(id=ptid)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        posted = serializer.update(instance, serializer.data)
        return JsonResponse(PatientSerializer(posted).data, status=200)



urlpatterns = patient_module.urlpatterns