from django.http import JsonResponse, HttpResponse
from atlas.guarantor import use_serializer, any_exception_throws_400
from atlas.locator import AModule
from rest_framework.views import APIView
from .serializers import CompleteQuestionnaireSerializer, CreateQuestionnaireSerializer, \
    QuestionnaireSerializer, RenderQuestionnaireSerializer, AnswerQuestionnaireSerializer
from .models import Questionnaire
from reservation.models import Reservation
from datetime import datetime
from rest_framework.parsers import JSONParser

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
        new_questionnaire = Questionnaire.objects.create(**serializer.data)
        return JsonResponse({'rid': new_questionnaire.id})

@questionnaire_module.route(r"(?<qid>.+?)/update", name="questionnaire_update")
class Update(APIView):

    @any_exception_throws_400
    @use_serializer(Serializer=CompleteQuestionnaireSerializer)
    def post(self, serializer, qid, format=None):
        questionnaire = Questionnaire.objects.get(id=qid)

        updated_fields = serializer.data

        for attr, value in updated_fields.items():
            setattr(questionnaire, attr, value)

        questionnaire.save()
        return JsonResponse({'updated_fields': list(serializer.data.keys())})


@questionnaire_module.route(r"(?<qid>.+?)/info", name="questionnaire_get")
class GetQuestionnaireInfo(APIView):

    @any_exception_throws_400
    def get(self, request, resid, format=None):
        questionnaire = Questionnaire.objects.get(id=qid)

        return JsonResponse(QuestionnaireSerializer(questionnaire).data)


@questionnaire_module.route(r"(?<qid>.+?)/commit", name="questionnaire_commit")
class Commit(APIView):

    @any_exception_throws_400
    def post(self, request, qid, format=None):
        questionnaire = Questionnaire.objects.get(id=qid)
        questionnaire.commit_at = datetime.now()
        questionnaire.save()

        return HttpResponse(status=204)


@questionnaire_module.route(r"?<qid>.+?/render", name = "questionnaire_render")
class Render(APIView):
    # TODO: Figuring out the token for tmp link validation
    @any_exception_throws_400
    def get(self,request,qid,resid,format=None):
        questionnaire = Questionnaire.objects.get(id=qid)
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
        serializer = RenderQuestionnaireSerializer(reseid= resid, questions_dict=question_dic)
        return serializer.data

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