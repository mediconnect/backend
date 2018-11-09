from django.urls import reverse
import json
from rest_framework.test import APITestCase,APIClient
from backend.common_test import CommonSetup


# Create your tests here.
class InfoModuleTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        dummy = self.dummy = CommonSetup(hospital=2, disease=2)
        self.hospitals = dummy.hospital
        self.diseases = dummy.disease

    def test_create_info(self):
        url = reverse('info-list')
        i = 0
        for h in self.hospitals:
            for d in self.diseases:
                # print(h,d)
                i+=1
                data = {
                    'hospital':h,
                    'disease': d,
                    'rank':i,
                    'deposit':1000*(i),
                    'full_price':10000*i,
                }
                response = self.client.post(url,data,format='json')
                self.assertEqual(response.status_code,201)

    def test_query_info(self):
        self.test_create_info()
        url = reverse('info-list')+'?ordering=rank,-price'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        # print(json.loads(response.content))
