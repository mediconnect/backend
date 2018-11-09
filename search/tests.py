# -*- coding: utf-8 -*-
from django.test import TestCase
from django.urls import reverse
from disease.models import Disease
from hospital.models import Hospital
from rank.models import Rank
from rest_framework.test import APIClient
import json


class SearchTestCase(TestCase):
    url = reverse('search_hospital')

    def setUp(self):
        Disease.objects.all().delete()
        Hospital.objects.all().delete()
        Rank.objects.all().delete()
        disease = Disease.objects.create(name='精神', keyword='精神，精，神')
        hospital = Hospital.objects.create(name='aaa')
        Rank.objects.create(disease=disease, hospital=hospital)

    def test_normal_search(self):
        client = APIClient()
        response = client.get(self.url + '?query=精')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['disease']['id'], str(Disease.objects.get(name='精神').id))

        disease_data = [
            {'name': '一', 'keyword': '一，一一，一一一'},
            {'name': '二', 'keyword': '一，一一，一一一'},
            {'name': '三', 'keyword': '一，一一，一一一'},
        ]

        hospital_data = [
            {'name': 'a'},
            {'name': 'b'},
            {'name': 'c'},
        ]

        for disease_entry in disease_data:
            disease = Disease.objects.create(name=disease_entry['name'], keyword=disease_entry['keyword'])
            for i, hospital_entry in enumerate(hospital_data):
                hospital = Hospital.objects.create(name=hospital_entry['name'])
                Rank.objects.create(rank=i, disease=disease, hospital=hospital)

        response = client.get(self.url + '?query=一')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['hospitals']), 0)
        self.assertEqual(len(data['diseases']), 3)

        response = client.get(self.url + '?query=一一')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['hospitals']), 0)
        self.assertEqual(len(data['diseases']), 3)

        response = client.get(self.url + '?query=一一一')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['hospitals']), 0)
        self.assertEqual(len(data['diseases']), 3)

        hospitals_url = reverse('search_hospital_by_disease')
        for disease_entry in disease_data:
            response = client.get(hospitals_url + '?id=' + str(Disease.objects.get(name=disease_entry['name']).id))
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.content)
            self.assertEqual(len(data['hospitals']), 3)
            self.assertEqual(data['disease']['id'], str(Disease.objects.get(name=disease_entry['name']).id))
