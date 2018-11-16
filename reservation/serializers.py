from rest_framework import serializers
from atlas.creator import create_optional_field_serializer

from .models import Reservation
from customer.models import Customer
from patient.models import Patient
from hospital.models import Hospital
from disease.models import Disease
from slot.models.timeslot import TimeSlot


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = (
            "res_id", "user_id", "patient_id", "hospital_id", "disease_id",
            "ctime", "commit_at"
        )

        _on_commit_finalize_fields = ("timeslot", )


CompleteReservationSerializer = create_optional_field_serializer(ReservationSerializer)


class CreateReservationSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    patient_id = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    hospital_id = serializers.PrimaryKeyRelatedField(queryset=Hospital.objects.all())
    disease_id = serializers.PrimaryKeyRelatedField(queryset=Disease.objects.all())
    timeslot = serializers.PrimaryKeyRelatedField(queryset=TimeSlot.objects.all())