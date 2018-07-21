from django.http import JsonResponse
from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule
from rest_framework.views import APIView
from .models import Patient
from .serializers import PatientSerializer, OptionalPatientSerializer

patient_module = AModule()

## For security reasons, change api to ~/customer/<customer_id>/patient/...? or ~/patient/<customer>/...

@patient_module.route("create", name="patient_create")
class Create(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=PatientSerializer)
    def post(self, serializer, format=None):
        posted = serializer.create(serializer.data)
        return JsonResponse(PatientSerializer(posted).data)


@patient_module.route(r"(?<ptid>.+?)/info$", name="patient_get")
class FetchRecord(APIView):

    @any_exception_throws_400
    def get(self, request, ptid, format=None):
        instance = Patient.objects.get(id=ptid)

        return JsonResponse(PatientSerializer(instance).data)


@patient_module.route(r"(?<ptid>.+?)/update$", name="patient_update")
class Update(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=OptionalPatientSerializer)
    def post(self, serializer, ptid, format=None):
        instance = Patient.objects.get(id=ptid)

        posted = serializer.update(instance, serializer.data)
        return JsonResponse(PatientSerializer(posted).data)


urlpatterns = patient_module.urlpatterns