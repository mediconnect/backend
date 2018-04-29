from django.http import JsonResponse, HttpResponse
from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule
from rest_framework.views import APIView
from .serializers import SlotSerializer
from .models import Slot
from datetime import datetime

slot_module = AModule()

# Create your views here.
slot_module.route("batch/create", name="slot_create_batch")
class CreateList(APIView):

    @any_exception_throws_400
    @use_serializer(SlotSerializer)
    def post(self, serializer, format=None):


