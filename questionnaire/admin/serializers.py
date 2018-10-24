from rest_framework import serializers

from questionnaire.models import Questionnaire, Question, Choice


class QuestionnaireUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer to update status of a questionnaire
    """
    translator_id = serializers.UUIDField()
    is_translated = serializers.BooleanField()
    origin = serializers.FileField()
    translated = serializers.FileField

    class Meta:
        model = Questionnaire
        fields = '__all__'
        read_only_fields = (
            'hospital_id', 'disease_id', 'category',
        )


class QuestionUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer to update Questions
    """
    format = serializers.IntegerField()
    content = serializers.CharField(max_length=200)

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = (
            'questionnaire_id'
        )


class ChoiceUpdateSerializer(serializers.ModelSerializer):
    """
    A serializer to update Answer
    """
    content = serializers.CharField(max_length=200)

    class Meta:
        model = Choice
        fields = '__all__'
        read_only_fields = (
            'question_id'
        )
