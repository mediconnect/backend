from rest_framework.views import APIView
from django.http import JsonResponse
from disease.models import Disease
from rank.models import Rank


class Search(APIView):
    def get(self, request, format=None):
        query = request.query_params.get('query')
        all_diseases = Disease.objects.all()
        candidates, exact_match = [], False

        # find exact match word. check if the user input contains keyword and then
        # check if it is exact match
        for disease in all_diseases:
            # split according to unicode chinese letter
            keywords = set(disease.keyword.split(u'\uff0c'))
            if query in keywords:
                exact_match, candidates = True, [disease]
                break
            for keyword in keywords:
                if keyword in query:
                    candidates.append(disease)

        # leave candidates as all diseases if nothing found
        candidates = all_diseases if len(candidates) == 0 else candidates

        if not exact_match:
            return JsonResponse({
                'hospitals': [],
                'diseases': [{'id': disease.id, 'name': disease.name, 'keyword': disease.keyword}
                             for disease in candidates]
            }, status=200)

        hospitals = [r.hospital for r in Rank.objects.filter(disease=candidates[0]).order_by('rank')]
        return JsonResponse({
            'hospitals': [{'name': hospital.name, 'introduction': hospital.introduction} for hospital in hospitals],
        }, status=200)


class HospitalByDisease(APIView):
    def get(self, request, format=None):
        disease_id = request.query_params.get('id')
        disease = Disease.objects.get(id=disease_id)
        hospitals = [r.hospital for r in Rank.objects.filter(disease=disease).order_by('rank')]
        return JsonResponse({
            'hospitals': [{'name': hospital.name, 'introduction': hospital.introduction} for hospital in hospitals],
        }, status=200)
