from rest_framework import serializers
from .models import Info, InfoReview, LikeInfo


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__'


class InfoReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoReview
        fields = '__all__'


class LikeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeInfo
        fields = '__all__'
