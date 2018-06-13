
from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule
from atlas.permissions import SupPermission, TransPermission, ResPermission

from .serializers import CompleteQuestionnaireSerializer, CreateQuestionnaireSerializer, CreateQuestionnaireLinkSerializer, \
    QuestionnaireSerializer, RenderQuestionnaireSerializer, AnswerQuestionnaireSerializer
from .models import Questionnaire
from reservation.models import Reservation
from customer.models import  Customer
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.core.signing import Signer,TimestampSigner,BadSignature,SignatureExpired
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail

signer = TimestampSigner()
questionnaire_module = AModule()

FORMAT_DIC={
    '0':'单选',
    '1':'多选',
    '2':'简答'
}

@questionnaire_module.route("create", name="questionnaire_init")
class InitialCreate(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=CreateQuestionnaireSerializer)
    def put(self, serializer, format=None):
        print(**serializer.data)
        new_questionnaire = Questionnaire.objects.create(**serializer.data)
        return JsonResponse({'qid': new_questionnaire.id})

@questionnaire_module.route(r"(?<qid>.+?)/update", name="questionnaire_update")
class Update(APIView):

    @any_exception_throws_400
    @permission_classes((IsAuthenticated, SupPermission))
    @use_serializer(Serializer=CompleteQuestionnaireSerializer)
    def post(self, serializer, qid, format=None):
        questionnaire = Questionnaire.objects.get(id=qid)

        updated_fields = serializer.data

        for attr, value in updated_fields.items():
            setattr(questionnaire, attr, value)

        questionnaire.save()
        return JsonResponse({'updated_fields': list(serializer.data.keys())})


@questionnaire_module.route(r"(?<qid>.+?)/info", name="questionnaire_get")
@permission_classes((IsAuthenticated, SupPermission))
class GetQuestionnaireInfo(APIView):

    @any_exception_throws_400
    def get(self, request, resid, format=None):
        hospital_id = Reservation.objects.get(id = resid).hospital
        disease_id = Reservation.objects.get(id = resid).disease
        questionnaire = Questionnaire.objects.get(hospital = hospital_id, disease = disease_id)

        return JsonResponse(QuestionnaireSerializer(questionnaire).data)


@questionnaire_module.route(r"(?<qid>.+?)/commit", name="questionnaire_commit")
class Commit(APIView):

    @any_exception_throws_400
    def post(self, request, qid, format=None):
        questionnaire = Questionnaire.objects.get(id=qid)
        questionnaire.commit_at = datetime.now()
        questionnaire.save()

        return HttpResponse(status=204)

@questionnaire_module.route(r"(?<qid>.+?)/createtmplink/", name="questionnaire_createTmpLink")
class CreateTmpLink(APIView):

    @any_exception_throws_400
    @permission_classes((IsAuthenticated, SupPermission))
    @use_serializer(Serializer=CreateQuestionnaireLinkSerializer)
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

@questionnaire_module.route(r"?<qid>.+?/render/?<token>.+?", name = "questionnaire_render")
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


@questionnaire_module.route(r"?<qid>.+?/answer", name = "questionnaire_answer")
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

urlpatterns = questionnaire_module.urlpatterns