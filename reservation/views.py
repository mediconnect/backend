from django.http import JsonResponse
from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule
from rest_framework.views import APIView
from .serializers import CompleteReservationSerializer, CreateReservationSerializer, ReservationSerializer
from .models import Reservation

reservation_module = AModule()


@reservation_module.route("create", name="reservation_init")
class InitialCreate(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=CreateReservationSerializer)
    def put(self, serializer, format=None):
        created = serializer.create(serializer.data)
        new_reservation = Reservation.objects.create(**created)
        return JsonResponse({'rid': new_reservation['id']})

@reservation_module.route(r"(?<resid>.+?)/update", name="reservation_update")
class Update(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=CompleteReservationSerializer)
    def post(self, serializer, resid, format=None):
        reservation = Reservation.objects.get(id=resid)

        for attr, value in serializer.data.items():
            reservation[attr].set(value)

        reservation.save()
        return JsonResponse({'updated_fields': serializer.data.keys()})


@reservation_module.route(r"(?<resid>.+?)/info", name="reservation_get")
class GetReservationInfo():

    @any_exception_throws_400
    def get(self, request, resid, format=None):
        reservation = Reservation.objects.get(id=resid)

        return JsonResponse(ReservationSerializer(reservation).data)