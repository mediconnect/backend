from rest_framework import serializers
from ..models.timeslot import TimeSlot


class SlotAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSlot
        fields = '__all__'
        read_only_fields = ('time_slot_id','hospital','disease',)