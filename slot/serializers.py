from rest_framework import serializers
from .models import TimeSlot, SlotBind
# from atlas.creator import create_optional_field_serializer


# TimeSlot Read related
class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'


# TimeSlot Aggregated level information
class TimeSlotAggInfoSerializer(serializers.Serializer):
    hospital_id = serializers.UUIDField()
    disease_id = serializers.IntegerField()
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
    disease_id = serializers.IntegerField()
    date_slots = DateNumTupleSerializer(many=True)


class OneTimeSlotUpdateSerializer(serializers.Serializer):
    hospital_id = serializers.UUIDField()
    diseases = DiseaseDateSlotSerializer(many=True)


