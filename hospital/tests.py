from django.urls import reverse
from django.http.request import QueryDict
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase
import json
import uuid

from .models import Hospital

class HospitalModuleTest(APITestCase):

    def test_create_hospital(self):
        """
        Ensure that we can create a hospital
        """
        url = reverse('hospital-list')
        data = {
            'id': uuid.uuid4(),
            'name': 'demo_hospital',
            'email':'demo@demo.com',
            'overall_rank':1,
            'average_score':0.0,
            'review_number':10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_query_hospitals(self):
        self.test_create_hospital()
        self.test_create_hospital()
        url = reverse('hospital-list')
        data = {
            'query' : 'name=demo_hospital&email=demo@demo.com'
        }
        query = QueryDict(data['query']).dict()
        response = self.client.get(url,data,format='json')

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        for each in response.data:
            for k,v in query.items():
                self.assertEqual(each.get(k),v)