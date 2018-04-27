from rest_framework import serializers
from .models import Questionnaire
from atlas.creator import create_optional_field_serializer


class QuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = '__all__'
        read_only_fields = (
            "id", "hospital_id", "disease_id", "category", "is_translated", "translator_id",
            "origin_pdf","questions", "ctime", "commit_at"
        )
        _on_commit_finalize_fields = ("origin_pdf","questions", )


CompleteQuestionnaireSerializer = create_optional_field_serializer(QuestionnaireSerializer)


class CreateQuestionnaireSerializer(serializers.ModelSerializer):
    """
    Create Questionnaire
    """

    class Meta:
        model = Questionnaire
        fields = ('hospital_id','disease_id','category')


class RenderQuestionnaireSerializer(serializers.Serializer):
    questions_dict = serializers.DictField()
    reservation_id = serializers.IntegerField()

class AnswerQuestionnaireSerializer(serializers.Serializer):
    answer_dict = serializers.DictField()
    reservation_id = serializers.IntegerField()