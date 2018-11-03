from rest_framework import serializers

from questionnaire.models import Questionnaire, Question, Choice, Answer


class RenderQuestionnaireSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Questionnaire
        fields = ('__all__', 'token',)
        read_only_fields = ('__all__', 'token',)


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'


