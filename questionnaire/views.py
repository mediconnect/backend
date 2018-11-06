from atlas.signer import signer
from atlas.permissions import SupPermission, TransPermission, ResPermission

from reservation.models import Reservation
from .models import Questionnaire,Question, Choice, Answer
from .serializers import QuestionnaireSerializer, \
    QuestionSerializer, ChoiceSerializer,AnswerSerializer

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import routers, filters
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.contrib.sites.shortcuts import get_current_site
from django.urls import path, re_path
from django_filters.rest_framework import DjangoFilterBackend

FORMAT_DIC={
    '0':'单选',
    '1':'多选',
    '2':'简答'
}


class QuestionnaireViewSet(ModelViewSet):
    serializer_class = QuestionnaireSerializer
    queryset = Questionnaire.objects.all()
    filter_backends = (filters.OrderingFilter,DjangoFilterBackend)
    filter_fields = ('hospital__name','disease__name','category','is_translated','translator__user')
    ordering_fields = '__all__'

    # def get_permissions(self):
    #
    #     if self.action == 'update':
    #         self.permission_classes = [SupPermission,TransPermission]
    #
    #     else:
    #         self.permission_classes = [SupPermission]
    #
    #     return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = QuestionnaireSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            q = serializer.save()
            return Response({'msg': 'Created', 'id': q.id}, status=201)

        else:
            return Response(serializer.errors, status=400)


class QuestionViewSet(ModelViewSet):

    serializer_class = QuestionSerializer
    filter_backends = (filters.OrderingFilter,DjangoFilterBackend)
    filter_fields = '__all__'
    ordering_fields = '__all__'

    def get_queryset(self):
        questionnaire_id = self.kwargs['questionnaire_id']
        return Question.objects.filter(questionnaire_id=questionnaire_id)

    # def get_permissions(self):
    #
    #     if self.action == 'update':
    #         self.permission_classes = [TransPermission]
    #
    #     else:
    #         self.permission_classes = [TransPermission, SupPermission]
    #
    #     return [permission() for permission in self.permission_classes]

    def create(self, request,*args, questionnaire_id=None, **kwargs):
        data = request.data.copy()
        data['questionnaire'] = questionnaire_id
        serializer = QuestionSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            q = serializer.save()
            return Response({'msg': 'Created', 'id': q.id}, status=201)

        else:
            return Response(serializer.errors, status=400)


class ChoiceViewSet(ModelViewSet):
    serializer_class = ChoiceSerializer
    filter_backends = (filters.OrderingFilter,DjangoFilterBackend,)
    filter_fields = '__all__'
    ordering_fields = '__all__'

    def get_queryset(self):
        question_id = self.kwargs['question_id']
        return Choice.objects.filter(question_id=question_id)

    # def get_permissions(self):
    #
    #     if self.action == 'update':
    #         self.permission_classes = [TransPermission]
    #
    #     else:
    #         self.permission_classes = [TransPermission, SupPermission]
    #
    #     return [permission() for permission in self.permission_classes]

    def create(self, request, *args, question_id=None,**kwargs):
        data = request.data.copy()
        data['question'] = question_id
        serializer = ChoiceSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Created', 'id': serializer.data['id']}, status=201)

        else:
            return Response(serializer.errors, status=400)


class AnswerViewSet(ModelViewSet):
    serializer_class = AnswerSerializer
    filter_backends = (filters.OrderingFilter,DjangoFilterBackend)
    filter_fields = ('reservation','questionnaire','is_translated','translator',)
    ordering_fields = '__all__'

    def get_queryset(self):
        res_id = self.kwargs['res_id']
        return Answer.objects.filter(reservation_id=res_id)
    # def get_permissions(self):
    #
    #     if self.action == 'update':
    #         self.permission_classes = [TransPermission]
    #
    #     else:
    #         self.permission_classes = [TransPermission, SupPermission]
    #
    #     return [permission() for permission in self.permission_classes]

    def create(self, request,*args, res_id=None, **kwargs, ):
        data = request.data.copy()
        data['res_id'] = res_id
        serializer = AnswerSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Created', 'id': serializer.data['id']}, status=201)

        else:
            return Response(serializer.errors, status=400)


class ListAllQuestions(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (filters.OrderingFilter,DjangoFilterBackend)
    filter_fields = '__all__'
    ordering_fields = '__all__'


class ListAllChoices(ListAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = (filters.OrderingFilter,DjangoFilterBackend)
    filter_fields = '__all__'
    ordering_fields = '__all__'


class ListAllAnswers(ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = (filters.OrderingFilter,DjangoFilterBackend)
    filter_fields = ('reservation','questionnaire','is_translated','translator',)
    ordering_fields = '__all__'


class CreateTmpLink(APIView):

    def post(self,request,*args,questionnaire_id,**kwargs):
        qid = questionnaire_id
        res_id = request.data['res_id']
        token = signer.sign(str(qid))
        reservation = Reservation.objects.get(res_id=res_id)
        user_id = reservation.user_id.id
        link = get_current_site(request).domain + '/api/questionnaire/' + token[(str.find(token, ':')) + 1:]
        # errors = send_mail(
        #     '问卷',
        #     '请点击此链接填写医院问卷' + link,
        #     email,
        #     'gabrielwry@gmail.com',
        #     fail_silently=False,
        # )
        return Response({'link':link,
                         'token':token,
                         'user_id':user_id,
                         'questionnaire_id':qid,
                         'res_id':res_id},status=200)


class RenderTmpLink(APIView):

    def get(self,request,*args, token, **kwargs):
        try:
            qid = signer.unsign(token,max_age=24)
            return Response({'questionnaire_id':qid},status=200)
        except Exception as e:
            return Response({'error':str(e)},status=400)


router = routers.DefaultRouter()
router.register(r'admin',
                QuestionnaireViewSet,
                base_name='questionnaire')

router.register(r'admin/(?P<questionnaire_id>[^/.]+)/question',
                QuestionViewSet,
                base_name='question')

router.register(r'admin/(?P<questionnaire_id>[^/.]+)/question/(?P<question_id>[^/.]+)/choice',
                ChoiceViewSet,
                base_name='choice')

router.register(r'reservation/(?P<res_id>[^/.]+)/answer',
                AnswerViewSet,
                base_name='answer')

urlpatterns = router.urls +\
    [
        re_path(r'admin/(?P<questionnaire_id>[^/.]+)/create_link',
                CreateTmpLink.as_view(),
                name='create-link'),

        path('questions',
             ListAllQuestions.as_view(),
             name='list-all-questions'),

        path('choices',
             ListAllChoices.as_view(),
             name='list-all-choices'),

        path('answers',
             ListAllAnswers.as_view(),
             name='list-all-answers'),

        re_path(r'(?P<token>[^/.]+)',
                RenderTmpLink.as_view(),
                name='render-questionnaire')
    ]
