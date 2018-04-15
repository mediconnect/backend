from django.http import JsonResponse
from atlas.guarantor import use_serializer
from atlas.locator import AModule
from rest_framework.views import APIView
from .serializers import CompleteReservationSerializer, CreateReservationSerializer, ReservationSerializer
from .models import Reservation

reservation_module = AModule()


@reservation_module.route("create", name="reservation_init")
class InitialCreate(APIView):

    @use_serializer(Serializer=CreateReservationSerializer)
    def put(self, serializer, format=None):
        created = serializer.create(serializer.data)
        new_reservation = Reservation.objects.create(**created)
        return JsonResponse({'rid': new_reservation['id']}, status=200)

@reservation_module.route(r"(?<resid>.+?)/update", name="reservation_update")
class Update(APIView):

    @use_serializer(Serializer=CompleteReservationSerializer)
    def post(self, serializer, resid, format=None):
        try:
            reservation = Reservation.objects.get(id=resid)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        for attr, value in serializer.data.items():
            try:
                reservation[attr].set(value)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        reservation.save()
        return JsonResponse({'updated_fields': serializer.data.keys()}, status=200)


@reservation_module.route(r"(?<resid>.+?)/info", name="reservation_get")
class GetReservationInfo():

    def get(self, se):