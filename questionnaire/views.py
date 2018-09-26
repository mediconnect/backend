
from atlas.permissions import SupPermission, TransPermission, ResPermission

from reservation.models import Reservation
from customer.models import  Customer
from .models import Questionnaire,Question, Choice
from .serializers import QuestionnaireSerializer, \
    QuestionSerializer, ChoiceSerializer

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.core.signing import Signer,TimestampSigner,BadSignature,SignatureExpired
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail

from datetime import datetime

signer = TimestampSigner()

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

            permission_classes = [TransPermission]

        else:
            permission_classes = [SupPermission]

        return [permission() for permission in permission_classes]

    def create(self,request, *args, **kwargs):

        serializer = QuestionnaireSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg': 'Created', 'id': serializer.data['id']}, status=201)

        else:
            return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        super(QuestionnaireViewSet, self).update(request,*args, **kwargs)
        pass


class CreateTmpLink(APIView):

    def post(self,serializer,request,qid,resid):
        # TODO: which HTTP method to use?
        token = signer.sign(qid+resid)
        reservation = Reservation.objects.get(id = resid)
        email = Customer.objects.get(id = reservation.customer).email
        link = get_current_site(request).domain + '/questionnaire/' + str(qid) + 'render/' \
                  + token[(str.find(token, ':')) + 1:]
        send_mail(
            '问卷',
            '请点击此链接填写医院问卷' + link,
            email,
            'gabrielwry@gmail.com',
            fail_silently=False,
        )
        return JsonResponse({'fields': list(serializer.data.keys())})

class Render(APIView):
    def get(self,request,qid,resid,token,format=None):
        questionnaire = Questionnaire.objects.get(id=qid)
        concat = str(int(qid) + int(resid)) + ":"  # restore the origin signature
        try:
            origin = signer.unsign(concat + token, max_age=24 * 60 * 60)  # valid for at most one day
            question_dic = {}
            with open(questionnaire.questions) as q:
                content = q.read()
                for each in content.split("|"):
                    if each != "":
                        str_ = each.split("/")  # split string on | and / to build the dic_
                        question_dic[int(str_[1])] = {
                            "question": str_[3],
                            "format": FORMAT_DIC[str_[5]],
                            "choices": str_[7:-1]
                        }
            serializer = RenderQuestionnaireSerializer(reseid=resid, questions_dict=question_dic)
            return serializer.data
        except  SignatureExpired as e:
            return JsonResponse({
                'error': type(e).__name__,
                'detail': str(e)
            }, status=401)

class Answer(APIView):

    @any_exception_throws_400
    def post(self,request,qid,resid,format=None):
        questionnaire = Questionnaire.objects.get(id=qid)
        reservation = Reservation.objects.get(id=resid)
        payload = JSONParser().parse(request)
        answer = payload['answer']
        answer_dict = {}
        # TODO: store answer as a File
        serializer = AnswerQuestionnaireSerializer(answer_dict=answer_dict,resid=resid)
        return serializer.data
