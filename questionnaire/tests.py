from django.urls import reverse
from django.http import QueryDict
from rest_framework.test import APITestCase,APIClient
from rest_framework import status

from .models import Questionnaire,Question,Choice
from staff.models.supervisor import Supervisor
from staff.models.translator import Translator

from atlas.comparer import APITestClient
from backend.common_test import CommonSetup
from datetime import datetime, timedelta

import json

class CreateQuestionnaireTest(APITestCase):

    def setUp(self):
        self.client = APITestClient()
        dummy = self.dummy = CommonSetup(hospital=1,disease=1,customer=1,patient=1)
        self.hospital_id = dummy.hospital[0]
        self.disease_id = dummy.disease[0]
        self.translator_id = Translator.objects.get(
            user_id=dummy.translator.id).id

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
        url = reverse('question-list')
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
        url = reverse('choice-list')
        data = {
            'question_id': self.question_id,

            'content': 'Who is your daddy?'
        }
        response = self.client.post(url, data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
