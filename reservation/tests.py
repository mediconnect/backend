from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json
import uuid
from datetime import datetime, timedelta
from .models import Reservation
from atlas.comparer import APITestCaseExtend

# Create your tests here.
class ReservationModuleTest(APITestCaseExtend):
    def setUp(self):
        self.client = APIClient()
        self.maxDiff = None
        self.hospital_id = uuid.uuid4()

        payload = [
            {
                "hospital_id": self.hospital_id,
                "diseases": [
                    {
                        "disease_id": 1,
                        "date_slots": [
                            {
                                "date": datetime(2018, 1, 1) + timedelta(days=dt*7),
                                "quantity": 1,
                                "type": "add"
                            }
                            for dt in range(2)
                        ]
                    }
                ]
            }
        ]

        create_slot_url = reverse("slot_publish_batch")
        response = self.client.post(create_slot_url, payload, format='json')
        resp_info = json.loads(response.content)

        self.timeslot_ids = list(map(uuid.UUID, resp_info['created']))


    def test_all_workflows(self):
        resv_init_sample = {
            'user_id': uuid.uuid4(),
            'patient_id': 1,
            'hospital_id': self.hospital_id,
            'disease_id': 1,
            'timeslot_id': self.timeslot_ids[0],
        }

        # Test create
        create_resv_url = reverse("reservation_init")
        response = self.client.put(create_resv_url, resv_init_sample, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 1)

        # Test get and create result
        resvid = json.loads(response.content)['rid']

        get_resv_url = reverse("reservation_get", kwargs={'resid': resvid})
        response = self.client.get(get_resv_url)
        self.assertEqual(response.status_code, 200)
        response_obj = json.loads(response.content)
        self.assertJSONIntersectEqual(resv_init_sample, response_obj)
        self.assertIsNotNone(response_obj['ctime'])
        self.assertIsNone(response_obj['commit_at'])
        self.assertJSONIntersectEqual(response_obj, resv_init_sample)

        commit_resv_url = reverse("reservation_commit", kwargs={'resid': resvid})
        update_resv_url = reverse("reservation_update", kwargs={'resid': resvid})

        # test empty commit failure
        self.assertEqual(self.client.post(commit_resv_url).status_code, 400)

        # test update field
        extra_fields_sample = {
            "first_hospital": "Beijing Hexie Hospital",
            "first_doctor_name": "Crab River",
            "first_doctor_contact": "+86 13802332333",
        }
        response = self.client.post(update_resv_url, data=extra_fields_sample)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(json.loads(response.content)['updated_fields']), set(extra_fields_sample))

        response_obj = json.loads(self.client.get(get_resv_url).content)

        self.assertJSONIntersectEqual(response_obj, dict(resv_init_sample, **extra_fields_sample))

        # test empty commit success
        response = self.client.post(commit_resv_url)
        self.assertEqual(response.status_code, 204)

        response_obj = json.loads(self.client.get(get_resv_url).content)
        self.assertIsNotNone(response_obj['commit_at'])

        overwrite_sample = {
            "first_doctor_name": "Dr. He, Xie",
            "timeslot": self.timeslot_ids[1],
        }

        # test update failure
        self.assertEqual(self.client.post(update_resv_url, data=overwrite_sample).status_code, 400)

        # test update success
        del overwrite_sample['timeslot']
        response = self.client.post(update_resv_url, data=overwrite_sample)
        self.assertEqual(response.status_code, 200)

        response_obj = json.loads(self.client.get(get_resv_url).content)
        self.assertJSONIntersectEqual(response_obj, dict(extra_fields_sample, **overwrite_sample))


    def test_insufficient_slot(self):
        place_taker_1 = {
            'user_id': uuid.uuid4(),
            'patient_id': 1,
            'hospital_id': self.hospital_id,
            'disease_id': 1,
            'timeslot_id': self.timeslot_ids[0],
        }

        place_taker_2 = {
            'user_id': uuid.uuid4(),
            'patient_id': 1,
            'hospital_id': self.hospital_id,
            'disease_id': 1,
            'timeslot_id': self.timeslot_ids[1],
        }

        # setup
        create_resv_url = reverse("reservation_init")
        response = self.client.put(create_resv_url, place_taker_1, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.client.put(create_resv_url, place_taker_2, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 2)
        rid2 = json.loads(response.content)['rid']

        # add one more
        response = self.client.put(create_resv_url, place_taker_1, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "InsufficientSpaceException")

        update_resv_url = reverse("reservation_update", kwargs={'resid': rid2})

        # update to full time slot should fail and keep current slot
        response = self.client.post(update_resv_url, data={'timeslot': self.timeslot_ids[0]})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], "InsufficientSpaceException")
        self.assertEqual(Reservation.objects.get(res_id=rid2).timeslot_id, self.timeslot_ids[1])

        self.client.post(
            reverse("slot_publish_batch"),
            [
                {
                    "hospital_id": self.hospital_id,
                    "diseases": [
                        {
                            "disease_id": 1,
                            "date_slots": [
                                {
                                    "date": datetime(2018, 1, 1),
                                    "quantity": 1,
                                    "type": "add"
                                }
                                for dt in range(2)
                            ]
                        }
                    ]
                }
            ],
            format='json'
        )
        response = self.client.post(update_resv_url, data={'timeslot': self.timeslot_ids[0]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.get(res_id=rid2).timeslot_id, self.timeslot_ids[0])
