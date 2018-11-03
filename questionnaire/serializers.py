from rest_framework import serializers
from .models import Questionnaire, Question, Choice, Answer
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


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('res_id','questionnaire_id','content','origin','translator','is_translated')


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
    A serializer to update Choice
    """
    content = serializers.CharField(max_length=200)

    class Meta:
        model = Choice
        fields = '__all__'
        read_only_fields = (
            'question_id'
        )


class AnswerUpdateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(max_length=500)

    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = (
            'res_id','questionnaire_id'
        )