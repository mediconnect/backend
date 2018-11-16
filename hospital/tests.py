from django.urls import reverse
from django.http.request import QueryDict

from rest_framework import status
from rest_framework.test import  APITestCase

import uuid

from atlas.comparer import APITestClient
from backend.common_test import CommonSetup


class HospitalModuleTest(APITestCase):
    def setUp(self):
        self.dummy = dummy = CommonSetup()
        self.client = APITestClient()
        self.client.force_login(user=self.dummy.supervisor)

    def test_create_hospital(self):
        url = reverse('hospital-list')
        for i in range(3):
            data = {
                'id': uuid.uuid4(),
                'name': 'demo_hospital{}'.format(i),
                'email':'demo{}@demo.com'.format(i),
                'overall_rank':i,
                'average_score':0.0,
                'review_number':10
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_query_hospitals(self):
        self.test_create_hospital()
        url = reverse('hospital-list',)
        data = {
            'name':'demo_hospital1',
            'order_by':'name&-email',
        }
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

