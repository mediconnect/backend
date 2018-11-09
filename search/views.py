# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from django.http import JsonResponse
from disease.models import Disease
# from rank.models import Rank
from info.models import Info


class Search(APIView):
    def get(self, request, format=None):
        query = request.query_params.get('query')
        all_diseases = Disease.objects.all()
        candidates = []

        # find exact match word. check if the user input contains keyword and then
        # check if it is exact match
        for disease in all_diseases:
            # split according to unicode chinese letter
            keywords = set(disease.keyword.split(u'\uff0c'))
            for keyword in keywords:
                if query in keyword:
                    candidates.append(disease)
                    break

        # leave candidates as all diseases if nothing found
        candidates = all_diseases if len(candidates) == 0 else candidates

        if len(candidates) > 1:
            diseases = []
            infos = []
            for disease in candidates:
                diseases.append({'id':disease.id,
                                 'name':disease.name,
                                 'keyword':disease.keyword})
                infos.extend(i.id for i in Info.objects.filter(disease=disease))
            return JsonResponse({
                'hospitals': [],
                'diseases': diseases,
                'infos':infos
            }, status=200)

        if len(candidates) <= 0:
            return JsonResponse({
                'hospitals': [],
                'diseases': [{'id': disease.id, 'name': disease.name, 'keyword': disease.keyword}
                             for disease in all_diseases],
                'info_ids': [i.id for i in Info.objects.all]
            }, status=200)

        hospitals = [r.hospital for r in Info.objects.filter(disease=candidates[0]).order_by('rank')]
        disease = candidates[0]

        return JsonResponse({
            'disease': {'id': disease.id, 'name': disease.name, 'keyword': disease.keyword},
            'hospitals': [{'id': hospital.id, 'name': hospital.name, 'introduction': hospital.introduction}
                          for hospital in hospitals],
            'infos':[i.id for i in Info.objects.filter(disease=disease) if i.hospital in hospitals]
        }, status=200)


class HospitalByDisease(APIView):
    def get(self, request, format=None):
        disease_id = request.query_params.get('id')
        disease = Disease.objects.get(id=disease_id)
        hospitals = [r.hospital for r in Info.objects.filter(disease=disease).order_by('rank')]
        return JsonResponse({
            'disease': {'id': disease.id, 'name': disease.name, 'keyword': disease.keyword},
            'hospitals': [{'id': hospital.id, 'name': hospital.name, 'introduction': hospital.introduction}
                          for hospital in hospitals],
            'infos':[i.id for i in Info.objects.filter(disease=disease) if i.hospital in hospitals]
        }, status=200)
