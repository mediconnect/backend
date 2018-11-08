from rest_framework import serializers
from .models import Hospital, HospitalReview,LikeHospital


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class HospitalReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalReview
        fields = '__all__'


class LikeHospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeHospital
        fields = '__all__'
