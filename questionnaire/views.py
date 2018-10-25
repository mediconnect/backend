from atlas.signer import signer
from atlas.permissions import SupPermission, TransPermission, ResPermission

from reservation.models import Reservation
from customer.models import Customer
from .models import Questionnaire,Question, Choice
from .serializers import QuestionnaireSerializer, \
    QuestionSerializer, ChoiceSerializer,\
    QuestionnaireUpdateSerializer, QuestionUpdateSerializer, ChoiceUpdateSerializer

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
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

    def update(self, request, *args, **kwargs):
        super(QuestionnaireViewSet, self).update(request,*args, **kwargs)
        pass


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

    def update(self, request, *args, **kwargs):
        super(QuestionViewSet, self).update(request,*args, **kwargs)
        pass


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

    def update(self, request, *args, **kwargs):
        super(ChoiceViewSet, self).update(request,*args, **kwargs)
        pass


class CreateTmpLink(APIView):

    def post(self,request):
        qid = request.data['qid']
        resid = request.data['resid']
        token = signer.sign(str(qid)+resid)
        reservation = Reservation.objects.get(res_id=resid)
        email = Customer.objects.get(id=reservation.customer).email
        link = get_current_site(request).domain + '/questionnaire/admin/?token=' \
               + token[(str.find(token, ':')) + 1:]
        errors = send_mail(
            '问卷',
            '请点击此链接填写医院问卷' + link,
            email,
            'gabrielwry@gmail.com',
            fail_silently=False,
        )
        return Response({'errors':errors,
                         'link':link,
                         'email':email},status=200)


class UpdateQuestionnaire(APIView):

    permission_classes = [SupPermission, TransPermission, ]

    def post(self, request, format=None):

        serializer = QuestionUpdateSerializer(data=request.data)
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

    permission_classes = [SupPermission, TransPermission, ]

    def post(self, request, format=None):
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

    def post(self, request, format=None):
        serializer = ChoiceUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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


router = routers.SimpleRouter()
router.register(r'questionnaire/admin', QuestionnaireViewSet)
router.register(r'question/admin',QuestionViewSet)
router.register(r'choice/admin',ChoiceViewSet)
urlpatterns = router.urls +\
    [
        path('questionnaire/send_link/',
          CreateTmpLink.as_view(),
          name='send-link'),

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
