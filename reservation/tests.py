from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import json
import uuid
from datetime import datetime, timedelta
from .models import Reservation
from atlas.creator import fetch_partial_dict, process_dict_value

# Create your tests here.
class ReservationModuleTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
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
        print(self.timeslot_ids)

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
        # print(json.loads(response.content))
        self.assertEqual(response.status_code, 200)
        response_obj = json.loads(response.content)
        self.assertEqual(
            process_dict_value(resv_init_sample, lambda v: str(v) if),
            fetch_partial_dict(response_obj, resv_init_sample.keys())
        )
        self.assertIsNotNone(response_obj['ctime'])
        self.assertIsNone(response_obj['commit_at'])
        self.assertEqual(fetch_partial_dict(response_obj, resv_init_sample.keys()), resv_init_sample)

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

        self.assertEqual(
            fetch_partial_dict(response_obj, set(resv_init_sample.keys()) | set(extra_fields_sample.keys())),
            dict(resv_init_sample, **extra_fields_sample)
        )

        # test empty commit success
        response = self.client.post(commit_resv_url)
        self.assertEqual(response.status_code, 204)

        response_obj = json.loads(self.client.get(get_resv_url).content)
        self.assertIsNotNone(response_obj['commit_at'])

        overwrite_sample = {
            "first_doctor_name": "Dr. He, Xie",
            "timeslot_id": self.timeslot_ids[1],
        }

        # test update failure
        self.assertEqual(self.client.post(update_resv_url, data=overwrite_sample).status_code, 400)

        # test update success
        del overwrite_sample['slot_id']
        response = self.client.post(update_resv_url, data=overwrite_sample)
        self.assertEqual(response.status_code, 200)

        response_obj = json.loads(self.client.get(get_resv_url).content)
        self.assertEqual(
            fetch_partial_dict(response_obj, set(resv_init_sample.keys()) | set(extra_fields_sample.keys())),
            dict(resv_init_sample, **dict(extra_fields_sample, **overwrite_sample))
        )
