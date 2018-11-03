#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rest framework

from rest_framework.views import APIView
from rest_framework import routers
from rest_framework.response import Response

from django.urls import path

from .serializers import RenderQuestionnaireSerializer,\
    AnswerSerializer

from questionnaire.models import Question,\
    Questionnaire,\
    Choice,\
    Answer

from atlas.permissions import TransPermission,\
    SupPermission
from atlas.signer import signer, SignatureExpired


class RenderQuestionnaire(APIView):

    def get(self,request,format=None):
        serializer = RenderQuestionnaireSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = request.query_paramter['token']
            qid = request.data['qid']
            res_id = request.data['res_id']
            questionnaire = Questionnaire.objects.get(id=qid)
            concat = str(int(qid) + int(res_id)) + ":"  # restore the origin signature
            try:
                error = signer.unsign(concat + token, max_age=24 * 60 * 60)  # valid for at most one day
                questions = list(Question.objects.filter(questionnaire=questionnaire).all())
                q_dict = {}
                for q in questions:
                    q_dict[q.id] = (list(Choice.objects.filter(question=q)))
                return Response(
                    {'questionnaire': questionnaire.id,
                     'question_dict': q_dict},
                    status=200
                )

            except SignatureExpired as e:
                return Response({
                    'error': type(e).__name__,
                    'detail': str(e)
                }, status=403)


class SubmitAnswer(APIView):

    def create(self,request,format=None):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            answer = serializer.save()
            return Response({
                'admin':answer.id,
                'msg':'submitted'
            },status=201)
        else:
            return Response(serializer.errors, status=400)


urlpatterns = [
    path('questionnaire/render/',
         RenderQuestionnaire.as_view(),
         name='render-questionnaire'),

    path('questionnaire/admin/',
         SubmitAnswer.as_view(),
         name='submit-admin'),
]
