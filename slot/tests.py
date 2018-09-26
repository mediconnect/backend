
import json
import uuid
from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models.slotbind import SlotBind
from .models.timeslot import TimeSlot
from atlas.creator import fetch_partial_dict
from backend.common_test import CommonSetup


class SlotnModuleTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.maxDiff = None
        dummy = self.dummy = CommonSetup(hospital=4, disease=1, customer=1, patient=1)
        self.hospital_ids = dummy.hospital
        self.disease_id = dummy.disease[0]
        self.timeslot_ids =  None

    def test_slot_publish(self):
        hospital_ids = self.hospital_ids

        payload = [
            {
                "hospital_id": hospital_ids[0],
                "diseases": [
                    {
                        "disease_id": self.disease_id,
                        "date_slots": [
                            {
                                "date": datetime(2018, 1, 1) + timedelta(days=dt*7),
                                "quantity": 5,
                                "type": "add"
                            }
                            for dt in range(7)
                        ]
                    }
                ]
            }
        ]

        create_slot_url = reverse("slot_publish_batch")
        response = self.client.post(create_slot_url, payload, format='json')
        resp_info = json.loads(response.content)

        self.assertEqual(resp_info['updated'], [])
        self.assertEqual(resp_info['error'], [])
        self.assertEqual(len(resp_info['created']), TimeSlot.objects.count())

        # test uuid5 generation and database writeback
        for slot_id in map(lambda i: TimeSlot.createID(hospital_ids[0], self.disease_id, 2018, i), range(1, 8)):
            slots = TimeSlot.objects.filter(timeslot_id=slot_id)
            self.assertEqual(slots.count(), 1)
            self.assertEqual(slots[0].availability, 5)

        payload = [
            {
                "hospital_id": hospital_ids[0],
                "diseases": [
                    {
                        "disease_id": self.disease_id,
                        "date_slots": [
                            {
                                "date": datetime(2018, 1, 1) + timedelta(days=4 * 7),
                                "quantity": 40,
                                "type": "change"
                            },{
                                "date": datetime(2018, 1, 1) + timedelta(days=5 * 7),
                                "quantity": 15,
                                "type": "add"
                            },
                        ]
                    }
                ]
            }
        ]

        response = self.client.post(create_slot_url, payload, format='json')
        resp_info = json.loads(response.content)
        self.assertEqual(resp_info['created'], [])
        self.assertEqual(len(resp_info['updated']), 2)
        self.assertEqual(resp_info['error'], [])

        slot_agg_url = "{uri}?when=20180104&hospital={hid}".format(
            uri=reverse("slot_get_availability"),
            hid=str(hospital_ids[0])
        )
        resp = self.client.get(slot_agg_url)
        resp_obj = json.loads(resp.content)
        self.assertEqual(len(resp_obj), 4)
        print(resp_obj)
        self.assertEqual(
            list(map(lambda o: o['availability'], sorted(resp_obj, key=lambda o: o['week_start']))),
            [5, 5, 40, 20]
        )

    def test_slot_reset(self):
        hospital_ids = self.hospital_ids
        self.test_slot_publish()

        payload = [
            {
                "hospital_id": hospital_ids[0],
                "diseases": [
                    {
                        "disease_id": self.disease_id,
                        "date_slots": [
                            {
                                "date": datetime(2018, 1, 1) + timedelta(days=dt * 7),
                                "type": "change",
                                "quantity":0
                            }
                            for dt in range(7)
                        ]
                    }
                ]
            }
        ]

        reset_slot_url = reverse("slot_reset_batch")
        response = self.client.post(reset_slot_url, payload, format='json')

        resp_info = json.loads(response.content)
        for t in resp_info['updated']:
            timeslot = TimeSlot.objects.get(timeslot_id = t)
            self.assertEqual(timeslot.availability,  timeslot.default_availability)
