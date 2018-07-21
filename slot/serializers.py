from rest_framework import serializers
from .models.timeslot import TimeSlot
from .models.slotbind import SlotBind
from hospital.models import Hospital
from disease.models import Disease
# from atlas.creator import create_optional_field_serializer


# TimeSlot Read related
class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


# TimeSlot Aggregated level information
class TimeSlotAggInfoSerializer(serializers.Serializer):
    hospital = serializers.PrimaryKeyRelatedField(queryset=Hospital.objects.all())
    disease = serializers.PrimaryKeyRelatedField(queryset=Disease.objects.all())
    time_slot = serializers.DateTimeField()
    availability = serializers.IntegerField()


# TimeSlot update related
class DateNumTupleSerializer(serializers.Serializer):
    ADD_OPTION = 'add'
    CHANGE_OPTION = 'change'

    date = serializers.DateTimeField()
    quantity = serializers.IntegerField()
    type = serializers.ChoiceField(choices=(ADD_OPTION, CHANGE_OPTION))


class DiseaseDateSlotSerializer(serializers.Serializer):
    disease_id = serializers.PrimaryKeyRelatedField(queryset=Disease.objects.all())
    date_slots = DateNumTupleSerializer(many=True)


class OneTimeSlotUpdateSerializer(serializers.Serializer):
    hospital_id = serializers.PrimaryKeyRelatedField(queryset=Hospital.objects.all())
    diseases = DiseaseDateSlotSerializer(many=True)


