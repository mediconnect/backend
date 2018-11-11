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

            data = {
                'email': 'register%d@test.com' %i,
                'password': '/.,Buz123',
                'confirmed_password': '/.,Buz123',
                'first_name': 'user%d' %i,
                'last_name': 'create%d' %i,
                'role': i
            }
            url = reverse('staff-user-list')
            request = self.client.post(url,data,format='json')
            self.assertEqual(request.status_code,201)

        self.client.logout()


class StaffLoginTestCase(APITestCase):

    def setUp(self):

        create_user = CreateUserTestCase()
        create_user.setUp()
        create_user.test_create_user()
        self.client = APIClient()

    def testLogin(self):
        for i in range(1,3):
            data = {
                'email': 'register%d@test.com' % i,
                'password': '/.,Buz123',
            }
            user = User.objects.get(email=data['email'])
            url = reverse('staff-login')
            response = self.client.post(url,data,format='json')
            self.assertEqual(response.status_code,200)
            self.assertIsNotNone(response.cookies)

    def test_normal_log_out(self):
        self.testLogin()
        response = self.client.post(reverse('customer_logout'),{},format='json')
        self.assertEqual(response.status_code,200)
        self.assertNotIn('csrftoken',response.cookies)
        # self.assertRedirects(body,reverse('search_hospital'),200)
