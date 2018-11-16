from django.urls import reverse
import json
from customer.models import Customer
from rest_framework.test import APITestCase,APIClient
from backend.common_test import CommonSetup


# Create your tests here.
class InfoModuleTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        dummy = self.dummy = CommonSetup(hospital=2, disease=2, customer=1)
        self.hospitals = dummy.hospital
        self.diseases = dummy.disease
        self.customer = dummy.customer[0]
        self.infos = []
        self.like_infos = []
        customer = Customer.objects.get(id=self.customer)
        self.client.force_login(customer.user)

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
                self.infos.append(json.loads(response.content)['id'])

    def test_query_info(self):
        self.test_create_info()
        url = reverse('info-list')+'?ordering=rank,-price'
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)
        # print(json.loads(response.content))

    def test_like_info(self):
        self.test_create_info()
        url = reverse('like-info-list',kwargs={'customer_id':self.customer})
        for info in self.infos:
            data = {
                'info':info,
            }
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code,201)
            self.like_infos.append(json.loads(response.content)['id'])

    def test_unlike_info(self):
        self.test_like_info()

        for like_info in self.like_infos:
            url = reverse('like-info-detail',kwargs={'customer_id':self.customer,
                                                     'pk':like_info})
            response = self.client.delete(url,format='json')
            self.assertEqual(response.status_code, 204)