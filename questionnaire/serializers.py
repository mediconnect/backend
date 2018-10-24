from rest_framework import serializers
from .models import Questionnaire, Question, Choice
from staff.models.translator import Translator


class QuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questionnaire
        fields = ('hospital','disease','category','origin','translator','is_translated')

    def validate(self,data):
        hospital = data['hospital']
        disease = data['disease']
        category = data['category']
        origin = data['origin']
        translator = data['translator']

        q = Questionnaire.objects.filter(
            hospital_id=hospital,
            disease_id=disease,
            category=category,
            origin=origin,
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
                if Translator.objects.get(user=translator.user).role == 2:
                    raise serializers.ValidationError(
                        {'Error': 'Please resign a E2C translator to this task.'}
                    )
        data['is_translated'] = False
        return data


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = '__all__'

