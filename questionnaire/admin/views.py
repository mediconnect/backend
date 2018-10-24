#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest framework

from rest_framework.views import APIView
from rest_framework import routers
from rest_framework.response import Response

from django.urls import path

from .serializers import QuestionnaireUpdateSerializer,\
    QuestionUpdateSerializer,\
    ChoiceUpdateSerializer

from questionnaire.models import Question,\
    Questionnaire,\
    Choice

from atlas.permissions import TransPermission,\
    SupPermission


class UpdateQuestionnaire(APIView):

    permission_classes = [SupPermission, TransPermission, ]

    def post(self, request, format=None):

        questionnaire_id = request.data['questionnaire_id']
        questionnaire = Questionnaire.objects.get(questionnaire_id=questionnaire_id)

        updated_fields = {
            k:v for k,v in request.data.itmes()
        }

        for attr, value in updated_fields.items():
            setattr(questionnaire, attr, value)

        questionnaire.save()

        return Response(
            {'update_fields':list(updated_fields.keys())},
            status=200
        )


class UpdateQuestion(APIView):

    permission_classes = [SupPermission, TransPermission, ]

    def post(self, request, format=None):

        question_id = request.data['question_id']
        question = Question.objects.get(question_id=question_id)

        updated_fields = {
            k:v for k,v in request.data.itmes()
        }

        for attr, value in updated_fields.items():
            setattr(question, attr, value)

        question.save()

        return Response(
            {'update_fields':list(updated_fields.keys())},
            status=200
        )


class UpdateChoice(APIView):

    permission_classes = [SupPermission, TransPermission, ]

    def post(self, request, format=None):

        choice_id = request.data['choice_id']
        choice = Questionnaire.objects.get(choice_id=choice_id)

        updated_fields = {
            k:v for k,v in request.data.itmes()
        }

        for attr, value in updated_fields.items():
            setattr(choice, attr, value)

        choice.save()

        return Response(
            {'update_fields':list(updated_fields.keys())},
            status=200
        )


urlpatterns = [
    path('questionnaire/manage/',
         UpdateQuestionnaire.as_view(),
         name='manage-questionnaire'),

    path('question/manage/',
         UpdateQuestion.as_view(),
         name='manage-question'),

    path('choice/manage/',
         UpdateChoice.as_view(),
         name='manage-choice')
]
