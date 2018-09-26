from rest_framework import serializers
from ..models.timeslot import TimeSlot
from hospital.models import Hospital
from disease.models import Disease
from ..serializers import DiseaseDateSlotSerializer


class PeriodicallySlotUpdateSerializer(serializers.Serializer):

    hospital_id = serializers.PrimaryKeyRelatedField(queryset=Hospital.objects.all())
    diseases = DiseaseDateSlotSerializer(many=True)