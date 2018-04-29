from rest_framework import serializers
from .models import Slot
# from atlas.creator import create_optional_field_serializer


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'
        read_only_fields = ('res_id',)


class DateNumTupleSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    slots_to_add = serializers.IntegerField()
