from django.urls import reverse
from django.http import QueryDict
from rest_framework.test import APITestCase,APIClient
from rest_framework import status

from .models import Questionnaire,Question,Choice
from staff.models.supervisor import Supervisor
from staff.models.translator import Translator
from reservation.models import Reservation
from hospital.models import Hospital
from patient.models import Patient
from disease.models import Disease
from customer.models import Customer
from slot.models.timeslot import TimeSlot

from atlas.comparer import APITestClient
from backend.common_test import CommonSetup
from datetime import datetime, timedelta

import json
import uuid


class CreateQuestionnaireTest(APITestCase):

    def setUp(self):
        self.client = APITestClient()
        dummy = self.dummy = CommonSetup(hospital=1,disease=1,customer=1,patient=1)
        self.hospital_id = dummy.hospital[0]
        self.disease_id = dummy.disease[0]
        self.translator_id = Translator.objects.get(
            user_id=dummy.translator.id).id
        payload = [
            {
                "hospital_id": self.hospital_id,
                "diseases": [
                    {
                        "disease_id": self.disease_id,
                        "date_slots": [
                            {
                                "date": datetime(2018, 1, 1) + timedelta(days=dt * 7),
                                "quantity": 1,
                                "type": "add"
                            }
                            for dt in range(2)
                        ]
                    }
                ]
            }
        ]

        resp_info = self.client.json(method="POST", call_name="slot_publish_batch", data=payload)

        self.timeslot_ids = list(map(uuid.UUID, resp_info['created']))
        res = Reservation(
            **{
            'res_id':uuid.uuid4(),
            'user_id': Customer.objects.get(id=self.dummy.customer[0]),
            'patient_id': Patient.objects.get(id=self.dummy.patient[0]),
            'hospital_id': Hospital.objects.get(id=self.hospital_id),
            'disease_id': Disease.objects.get(id=self.disease_id),
            'timeslot': TimeSlot.objects.get(timeslot_id=self.timeslot_ids[0])})
        res.save()
        self.res_id = res.res_id

    def test_create_questionnaire(self):

        """
        Test create questionnaire
        """
        self.client.force_login(user=Supervisor.objects.get(user=self.dummy.supervisor).user)
        url = reverse('questionnaire-list')

        data = {
            'hospital':self.hospital_id,
            'disease':self.disease_id,
            'category':'blah',
            'translator':self.translator_id,
            'origin':open('Murphy.txt','r')
        }
        qd = QueryDict('',mutable=True)
        qd.update(data)
        response = self.client.post(url,qd,format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.questionnaire_id = json.loads(response.content)['id']
        self.client.logout()

    def test_create_question(self):
        """
        Test create question
        """
        self.test_create_questionnaire()
        self.client.force_login(user=Translator.objects.get(user=self.dummy.translator).user)
        url = reverse('question-list',kwargs={'questionnaire_id':self.questionnaire_id})
        data = {
            'questionnaire_id': self.questionnaire_id,
            'format': 1,
            'content': 'Who is your daddy?'
        }
        response = self.client.post(url, data)
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.question_id = json.loads(response.content)['id']

    def test_create_choice(self):
        """
        Test create choice
        """
        self.test_create_questionnaire()
        self.test_create_question()
        self.client.force_login(user=Translator.objects.get(user=self.dummy.translator).user)
        url = reverse('choice-list',kwargs={'question_id':self.question_id,
                                            'questionnaire_id':self.questionnaire_id})
        data = {
            'question_id': self.question_id,

            'content': 'Who is your daddy?'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tmp_link(self):
        """
        Test create temporary link to customer
        """
        self.test_create_questionnaire()
        self.test_create_question()
        self.test_create_choice()
        url = reverse('create-link',kwargs={'questionnaire_id':self.questionnaire_id})
        data = {
            'id':self.questionnaire_id,
            'res_id':self.res_id
        }
        response = self.client.post(url, data)
        self.token = json.loads(response.content)['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_render(self):
        self.test_create_questionnaire()
        self.test_create_question()
        self.test_create_choice()
        self.test_create_tmp_link()
        url = reverse('render-questionnaire',kwargs={'token':self.token})
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['questionnaire_id'],self.questionnaire_id)
