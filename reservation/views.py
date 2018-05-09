from datetime import datetime
import uuid

from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView

from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule

from .serializers import CompleteReservationSerializer, CreateReservationSerializer, ReservationSerializer
from .models import Reservation
from slot.models import TimeSlot, SlotBind

reservation_module = AModule()


def _try_assign_timeslot(res_id, timeslot_id):
    timeslot = TimeSlot.objects.find(timeslot_id=timeslot_id)
    assert timeslot, "Unable to find time slot"
    num_reg = SlotBind.objects.filter(timeslot_id=timeslot_id).count()
    assert num_reg < timeslot.availability, "Full slot!"
    bind = SlotBind.objects.create(
        timeslot_id=timeslot_id,
        reservation_id=res_id
    )
    return bind.slot_id


@reservation_module.route("create", name="reservation_init")
class InitialCreate(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=CreateReservationSerializer, pass_in='data')
    def put(self, payload, format=None):
        timeslot_id = TimeSlot.objects.find(timeslot_id=payload['slot_id'])
        new_reservation = Reservation.objects.create(**serializer.data)
        return JsonResponse({'rid': new_reservation.id})


@reservation_module.route(r"(?<resid>.+?)/update", name="reservation_update")
class Update(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=CompleteReservationSerializer)
    def post(self, serializer, resid, format=None):
        reservation = Reservation.objects.get(id=resid)

        updated_fields = serializer.data

        if (reservation.commit_at is not None) and \
                (set(CompleteReservationSerializer.Meta._on_commit_finalize_fields) & set(updated_fields.keys())):
            raise Exception("Slot cannot be changed after reservation submitted!")

        # TODO: Similar restriction should apply to other fields if the translation process starts!

        for attr, value in updated_fields.items():
            setattr(reservation, attr, value)

        reservation.save()
        return JsonResponse({'updated_fields': list(serializer.data.keys())})


@reservation_module.route(r"(?<resid>.+?)/info", name="reservation_get")
class GetReservationInfo(APIView):

    @any_exception_throws_400
    def get(self, request, resid, format=None):
        reservation = Reservation.objects.get(id=resid)

        return JsonResponse(ReservationSerializer(reservation).data)


@reservation_module.route(r"(?<resid>.+?)/commit", name="reservation_commit")
class Commit(APIView):

    @any_exception_throws_400
    def post(self, request, resid, format=None):
        reservation = Reservation.objects.get(id=resid)

        assert reservation.commit_at is None, "Reservation has already been submitted!"
        assert reservation.slot_id, "Reservation with empty slot info cannot be submitted!"
        assert reservation.first_hospital and reservation.first_doctor_name and reservation.first_doctor_contact, \
            "Reservation with empty medical history cannot be submitted!"

        reservation.commit_at = datetime.now()
        reservation.save()

        return HttpResponse(status=204)

# TODO: payment endpoint

urlpatterns = reservation_module.urlpatterns