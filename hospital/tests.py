from django.urls import reverse
from django.http.request import QueryDict
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase
import uuid

from staff.models.supervisor import Supervisor,User
from customer.models import Customer

class HospitalModuleTest(APITestCase):

    def test_create_hospital_as_supervisor(self):
        """
        Ensure that we can create a hospital
        """
        user = User(email='demo4Hospital@test.com',password=make_password('/.,Buz123'))
        user.save()
        supervisor = Supervisor(user=user)
        supervisor.save()
        self.client.force_login(supervisor.user)

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
        self.client.logout()

    def test_create_hospital_as_customer(self):
        """
        Ensure that we can create a hospital
        """
        user = User(email='register1@test.com',password=make_password('/.,Buz123'))
        user.save()
        customer = Customer(user=user)
        customer.save()
        self.client.force_login(customer.user)

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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()



    def test_query_hospitals(self):
        self.test_create_hospital_as_supervisor()
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

