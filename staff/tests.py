from rest_framework.test import APITestCase,APIClient

from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models.supervisor import Supervisor


class CreateUserTestCase(APITestCase):
    """ Test normal creating user procedural. """
    def setUp(self):
        self.client = APIClient()
        user = User(email='demo4Staff@test.com', password=make_password('/.,Buz123'))
        user.save()
        supervisor = Supervisor(user=user)
        supervisor.save()
        self.client.force_login(supervisor.user)

    def test_create_user(self):

        for i in range(3):

            payload = {
                'email': 'register%d@test.com' %i,
                'password': '/.,Buz123',
                'confirmed_password': '/.,Buz123',
                'first_name': 'user%d' %i,
                'last_name': 'create%d' %i,
                'role': i
            }

            if payload['role'] == 0:
                # Customer creation requires two additional fields
                url = reverse('customer_register')
                payload['password_confirmation'] = payload['confirmed_password']
                customer = {
                    'tel': 'N/A',
                    'address': 'N/A'
                }
                data = {
                    'auth': payload,
                    'customer': customer,
                    'role':0
                }
                request = self.client.post(url, data, format='json')
                print(request.content)
                self.assertEqual(request.status_code, 200)
            else:
                url = reverse('user-list')
                data = payload
                request = self.client.post(url,data,format='json')
                print(request.content)
                self.assertEqual(request.status_code,201)

        self.client.logout()


class StaffLoginTestCase(APITestCase):

    def setUp(self):

        creat_user = CreateUserTestCase()
        creat_user.setUp()
        creat_user.test_create_user()
        self.client = APIClient()

    def testLogin(self):
        for i in range(1,3):
            data = {
                'email': 'register%d@test.com' % i,
                'password': '/.,Buz123',
            }
            user = User.objects.get(email=data['email'])
            url = reverse('staff-login')
            request = self.client.post(url,data,format='json')
            if i == 0:
                pass
            self.assertEqual(request.status_code,200)
