from rest_framework.test import APITestCase,APIClient

from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Patient
from customer.models import Customer
import datetime
import json


class PatientTestCase(APITestCase):
    """ Test normal creating user procedural. """
    def setUp(self):
        self.client = APIClient()
        user = User(username='gooduser',email='demo4Customer@test.com', password=make_password('/.,Buz123'))
        user.save()
        self.customer = Customer(user=user)
        self.customer.save()
        hacker_user = User(username='baduser',email='badUser@test.com',password=make_password('/.UASIFs24'))
        hacker_user.save()
        self.hacker = Customer(user=hacker_user)
        self.hacker.save()
        self.client.force_login(self.customer.user)

    def test_create_patient(self):
        for i in range(3):

            payload = {
                'first_name':'demo%d'%i,
                'last_name':'patient%d'%i,
                'first_name_pinyin':'pin%d'%i,
                'last_name_pinyin':'yin%d'%i,
                'gender':'M',
                'birthdate':datetime.date.today(),
                'relationship':'self',
                'passport':'12345'
            }
            url = reverse('patient-list',kwargs={'customer_id':self.customer.id})
            response = self.client.post(url,payload,format='json')
            # print(response.content)
            self.assertEqual(response.status_code,201)
        # print(Patient.objects.filter(customer_id=self.customer.id))

    def test_normal_list(self):
        self.test_create_patient()
        url = reverse('patient-list',kwargs={'customer_id':self.customer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        print(json.loads(response.content))

    def test_illegal_list(self):
        self.test_create_patient()
        self.client.logout()
        self.client.force_login(self.hacker.user)
        url = reverse('patient-list',kwargs={'customer_id':self.customer.id})
        response =  self.client.get(url)
        self.assertEqual(response.status_code,403)
