from django.urls import reverse
from django.http import QueryDict
from rest_framework.test import APITestCase,APIClient
from rest_framework import status

from .models import Document
from hospital.models import Hospital
from disease.models import Disease
from reservation.models import Reservation
from customer.models import User,Customer
from patient.models import Patient
from slot.models.timeslot import TimeSlot

from atlas.comparer import APITestCaseExtend, APITestClient
from backend.common_test import CommonSetup

import uuid
from datetime import datetime, timedelta

class UploadFileTest(APITestCase):
    def setUp(self):
        self.client = APITestClient()
        dummy = self.dummy = CommonSetup(hospital=1,disease=1,customer=1,patient=1)
        self.hospital_id = dummy.hospital[0]
        self.disease_id = dummy.disease[0]

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


    def test_create_document(self):

        """
        Ensure that we can create document
        """
        self.client = APIClient()
        self.client.force_login(user=Customer.objects.get(id=self.dummy.customer[0]).user)
        url = reverse('document-list')

        data = {
            'file':open('Murphy.txt'),
            'type':'2',
            'resid':self.res_id,
            'obsolete':True,
            'description':'Sth',
        }
        qd = QueryDict('',mutable=True)
        qd.update(data)
        response = self.client.post(url,qd,format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)

