from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule
from rest_framework.views import APIView
from .serializers import SlotSerializer, TimeSlotAggInfoSerializer, OneTimeSlotUpdateSerializer
from .serializers import DateNumTupleSerializer as Update
from .models import TimeSlot, SlotBind
from .utils import date_to_weeknum, weeknum_to_date
from datetime import datetime, timedelta
import uuid

slot_module = AModule()


# Admin only: create a batch of slots
@slot_module.route("batch/create", name="slot_publish_batch")
class CreateOrUpdateList(APIView):

    @any_exception_throws_400
    @use_serializer(OneTimeSlotUpdateSerializer, many=True, pass_in='data')
    def post(self, update_info, format=None):
        created = []
        updated = []
        errored = []

        for hospital_info in update_info:
            hospital_id = hospital_info['hospital_id']
            disease_slots = hospital_info['diseases']
            for disease_slot in disease_slots:
                disease_id = disease_slot['disease_id']
                date_slots = disease_slot['date_slots']
                for date_slot in date_slots:
                    year, weeknum = date_to_weeknum(date_slot['date'])
                    timeslot_id = TimeSlot.createID(hospital_id, disease_id, year, weeknum)
                    quantity = date_slot['quantity']
                    try:
                        exist_timeslot = TimeSlot.objects.get(timeslot_id=timeslot_id)
                        change_type = date_slot['type']
                        if change_type == Update.CHANGE_OPTION:
                            assert SlotBind.objects.filter(timeslot_id=timeslot_id).count() < quantity, "Already more researvation!"
                            setattr(exist_timeslot, 'availability', quantity)
                        elif change_type == Update.ADD_OPTION:
                            setattr(exist_timeslot, 'availability', exist_timeslot.availability + quantity)
                        exist_timeslot.save()
                        updated.append(timeslot_id)
                    except ObjectDoesNotExist:
                        created.append(TimeSlot(
                            timeslot_id=timeslot_id,
                            hospital_id=hospital_id,
                            disease_id=disease_id,
                            slot_year=year,
                            slot_weeknum=weeknum,
                            availability=quantity
                        ))
                    except Exception as e:
                        errored.append({
                            'time_slot': timeslot_id,
                            'error': type(e).__name__,
                            'detail': str(e)
                        })

        if len(created):
            TimeSlot.objects.bulk_create(created)

        return JsonResponse({
            'created': list(map(lambda o: o.timeslot_id, created)),
            'updated': updated,
            'error': errored
        })


@slot_module.route("availability", name="slot_get_availability")
class GetSlotAvailability(APIView):

    # @any_exception_throws_400
    def get(self, request, format=None):
        args = request.query_params
        query_set = {}

        # on supervisor privilege can see more ("vision")
        # default 4 weeks from today
        if 'when' in args:
            now = datetime.strptime(args['when'], "%Y%m%d").date()
        else:
            now = datetime.now().date()

        now_yr, now_week, now_day = now.isocalendar()

        if 'hospital' in args:
            query_set['hospital_id'] = uuid.UUID(args['hospital'])

        if 'disease' in args:
            query_set['disease_id'] = args['disease']

        assert len(query_set.keys()), "Either hospital or disease need to be specified!"

        timeslots = TimeSlot.objects.filter(**query_set)
        slots_to_show = filter(
            lambda obj: -2 <= (weeknum_to_date(obj.slot_year, obj.slot_weeknum) - now).days <= 28,
            timeslots
        )

        return JsonResponse([
            {
                'hospital': slot.hospital_id,
                'disease': slot.disease_id,
                'week_start': weeknum_to_date(slot.slot_year, slot.slot_weeknum),
                'availability': slot.availability - SlotBind.objects.filter(timeslot_id=slot.timeslot_id).count()
            }
            for slot in slots_to_show
        ], safe=False)


urlpatterns = slot_module.urlpatterns
