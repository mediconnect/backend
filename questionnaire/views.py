from atlas.signer import signer
from atlas.permissions import SupPermission, TransPermission, ResPermission

from reservation.models import Reservation
from customer.models import Customer
from .models import Questionnaire,Question, Choice, Answer
from .serializers import QuestionnaireSerializer, \
    QuestionSerializer, ChoiceSerializer,AnswerSerializer,\
    QuestionnaireUpdateSerializer, QuestionUpdateSerializer, ChoiceUpdateSerializer, AnswerUpdateSerializer

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse
from django.urls import path
from rest_framework import routers

from datetime import datetime


FORMAT_DIC={
    '0':'单选',
    '1':'多选',
    '2':'简答'
}


class QuestionnaireViewSet(ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

    def get_permissions(self):

        if self.action == 'update':
            self.permission_classes = [SupPermission,TransPermission]

        else:
            self.permission_classes = [SupPermission]

        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = QuestionnaireSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            q = serializer.save()
            return Response({'msg': 'Created', 'id': q.id}, status=201)

        else:
            return Response(serializer.errors, status=400)


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # def get_permissions(self):
    #
    #     if self.action == 'update':
    #         self.permission_classes = [TransPermission]
    #
    #     else:
    #         self.permission_classes = [TransPermission, SupPermission]
    #
    #     return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):

        serializer = QuestionSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            q = serializer.save()
            return Response({'msg': 'Created', 'id': q.id}, status=201)

        else:
            return Response(serializer.errors, status=400)


class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    # def get_permissions(self):
    #
    #     if self.action == 'update':
    #         self.permission_classes = [TransPermission]
    #
    #     else:
    #         self.permission_classes = [TransPermission, SupPermission]
    #
    #     return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):

        serializer = ChoiceSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Created', 'id': serializer.data['id']}, status=201)

        else:
            return Response(serializer.errors, status=400)


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    # def get_permissions(self):
    #
    #     if self.action == 'update':
    #         self.permission_classes = [TransPermission]
    #
    #     else:
    #         self.permission_classes = [TransPermission, SupPermission]
    #
    #     return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):

        serializer = AnswerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Created', 'id': serializer.data['id']}, status=201)

        else:
            return Response(serializer.errors, status=400)


class CreateTmpLink(APIView):

    def post(self,request):
        qid = request.data['id']
        resid = request.data['res_id']
        token = signer.sign(str(qid)+resid)
        reservation = Reservation.objects.get(res_id=resid)
        user_id = reservation.user_id.id
        link = get_current_site(request).domain + '/questionnaire/admin/?token=' \
               + token[(str.find(token, ':')) + 1:]
        # errors = send_mail(
        #     '问卷',
        #     '请点击此链接填写医院问卷' + link,
        #     email,
        #     'gabrielwry@gmail.com',
        #     fail_silently=False,
        # )
        return Response({'content':link,'user_id':user_id},status=200)


class UpdateQuestionnaire(APIView):

    # permission_classes = [SupPermission, TransPermission, ]

    def put(self, request, format=None):

        serializer = QuestionnaireUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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

    # permission_classes = [SupPermission, TransPermission, ]

    def put(self, request, format=None):
        serializer = QuestionUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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

    def put(self, request, format=None):
        serializer = ChoiceUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            choice_id = request.data['choice_id']
            choice = Choice.objects.get(choice_id=choice_id)

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


class UpdateAnswer(APIView):

    # permission_classes = [SupPermission, TransPermission, ]

    def put(self, request, format=None):
        serializer = AnswerUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            answer_id = request.data['answer_id']
            answer = Answer.objects.get(answer_id=answer_id)

            updated_fields = {
                k:v for k,v in request.data.itmes()
            }

            for attr, value in updated_fields.items():
                setattr(answer, attr, value)

            answer.save()

            return Response(
                {'update_fields':list(updated_fields.keys())},
                status=200
            )


router = routers.DefaultRouter()
router.register(r'admin', QuestionnaireViewSet)
router.register(r'question/admin',QuestionViewSet)
router.register(r'choice/admin',ChoiceViewSet)
router.register(r'answer/admin',AnswerViewSet)

urlpatterns = router.urls +\
    [
        path(r'manage/createlink/',
          CreateTmpLink.as_view(),
          name='create-link'),

        path(r'manage/',
             UpdateQuestionnaire.as_view(),
             name='manage-questionnaire'),

        path(r'question/manage/',
             UpdateQuestion.as_view(),
             name='manage-question'),

        path(r'choice/manage/',
             UpdateChoice.as_view(),
             name='manage-choice'),

        path(r'answer/',
             UpdateAnswer.as_view(),
             name='manage-answer')
    ]
