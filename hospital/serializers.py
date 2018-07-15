from rest_framework import serializers
from .models import Hospital, HospitalReview,LikeHospital
from atlas.creator import create_optional_field_serializer


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'
        read_only_fields =('average_score','review_number',)


class HospitalReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalReview
        fields = '__all__'


class LikeHospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeHospital
        fields = '__all__'
