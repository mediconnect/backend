from django.urls import reverse
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.test import APITestCase,APIClient

from backend.common_test import CommonSetup
from atlas.comparer import APITestClient
from ..models import Reservation
from hospital.models import Hospital
from disease.models import Disease
from reservation.models import Reservation
from customer.models import User,Customer
from patient.models import Patient
from slot.models.timeslot import TimeSlot
from staff.models.supervisor import Supervisor

import json
import uuid
from datetime import datetime, timedelta


class UpdateReservationTest(APITestCase):

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
        user = User.objects.create_user(email='demo4manage@test.com',
                                        username='demo4manage@test.com',
                                        password='/.,Buz123')
        user.save()
        supervisor = Supervisor(user=user)
        supervisor.save()
        self.client.force_login(user)

    def testLegalUpdate(self):
        update_url = reverse('manage-reservation')
        validate_url = reverse('validate-operation')
        reservation = Reservation.objects.get(res_id =self.res_id)
        auth_data = {
            'password':'/.,Buz123'
        }
        update_data = {
            'res_id':self.res_id,
            'status':reservation.status+1,
            'trans_status':reservation.trans_status+1,
        }
        auth_data['update_data'] = update_data
        auth_response = self.client.post(validate_url,auth_data,format='json')
        self.assertEqual(auth_response.status_code,202)
        update_response = self.client.post(update_url,update_data,format='json')
        self.assertEqual(update_response.status_code,200)

    def testIllegalUpdate(self):
        update_url = reverse('manage-reservation')
        validate_url = reverse('validate-operation')
        reservation = Reservation.objects.get(res_id =self.res_id)
        auth_data = {
            'password':'/.,Buz1234'
        }
        update_data = {
            'res_id':self.res_id,
            'status':reservation.status+1,
            'trans_status':reservation.trans_status+1,
        }
        auth_data['update_data'] = update_data
        auth_response = self.client.post(validate_url,auth_data,format='json')
        self.assertEqual(auth_response.status_code,403)

