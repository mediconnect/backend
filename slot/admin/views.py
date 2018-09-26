from datetime import datetime, timedelta
import uuid

from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView

from atlas.creator import assert_or_throw
from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule
from errors import InvalidArgumentException

from .serializers import PeriodicallySlotUpdateSerializer
from ..serializers import DateNumTupleSerializer as Update
from ..models.timeslot import TimeSlot

from ..utils import date_to_weeknum, weeknum_to_date

slot_module = AModule()


# Admin only: create a batch of slots
@slot_module.route("batch/reset", name="slot_reset_batch")
class CreateOrUpdateList(APIView):


    @any_exception_throws_400
    @use_serializer(PeriodicallySlotUpdateSerializer, many=True, pass_in='data')
    def post(self, update_info, format=None):

        updated = []
        errored = []

        for hospital_info in update_info:
            hospital_id = hospital_info['hospital_id'].id
            disease_slots = hospital_info['diseases']
            for disease_slot in disease_slots:
                disease_id = disease_slot['disease_id'].id
                date_slots = disease_slot['date_slots']
                for date_slot in date_slots:
                    for t in TimeSlot.objects.filter(hospital_id=hospital_id, disease_id=disease_id):
                        quantity = t.default_availability
                        timeslot_id = t.timeslot_id
                        try:
                            exist_timeslot = TimeSlot.objects.get(timeslot_id=timeslot_id)
                            change_type = date_slot['type']
                            assert change_type == Update.CHANGE_OPTION
                            # total_registered = SlotBind.objects.filter(timeslot_id=timeslot_id).count()
                            # assert_or_throw(
                            #     total_registered <= quantity,
                            #     InvalidArgumentException(
                            #         "Can't shrink availability of `{sid}` ({reg} registered) to {avail}".format(
                            #             sid=timeslot_id,
                            #             reg=total_registered,
                            #             avail=quantity,
                            #         )
                            #     )
                            # )
                            setattr(exist_timeslot, 'availability', quantity)
                            exist_timeslot.save()
                            updated.append(timeslot_id)
                        except Exception as e:
                            errored.append({
                                'time_slot': timeslot_id,
                                'error': type(e).__name__,
                                'detail': str(e)
                            })

        return JsonResponse({
            'updated': updated,
            'error': errored
        })

urlpatterns = slot_module.urlpatterns

