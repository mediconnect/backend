from rest_framework import serializers
from .models import Questionnaire, Question, Choice
from staff.models.translator import Translator
from atlas.creator import create_optional_field_serializer


class QuestionnaireSerializer(serializers.ModelSerializer):
    confirm = serializers.BooleanField(default = False)

    class Meta:
        model = Questionnaire
        fields = ('__all__','confirm',)

    def validate(self,data):
        hospital_id = data['hospital_id']
        disease_id = data['disease_id']
        category = data['category']
        translator_id = data['translator_id']
        confirm = data['confirm']

        if confirm:
            return data

        q = Questionnaire.objects.filter(
            hospital_id = hospital_id,
            disease_id = disease_id,
            category = category
        )

        if q.exists():

            if q.is_translated:

                raise serializers.ValidationError(
                    {'Warning':'Do you wish to overwrite a translated questionnaire ?'}
                )

            elif not q.is_translated and q.translator:

                raise serializers.ValidationError(
                    {'Warning': 'A translator is working on this questionnaire.\n'
                                ' Do you really want to upload a new one ?'},

                )
            else:

                if Translator.objects.get(id = translator_id).role == 2:
                    raise serializers.ValidationError(
                        {'Error': 'Please resign a E2C translator to this task.'}
                    )

                return data


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('questionnaire_id',)


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = '__all__'
        read_only_fields = ('question_id',)

